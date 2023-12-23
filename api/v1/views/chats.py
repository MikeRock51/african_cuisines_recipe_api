#!/usr/bin/env python3
"""RESTFUL API actions for bot chats"""

from models import storage
from models.roles import UserRole
from flask import jsonify, abort, request, g
from api.v1.views import app_views
from api.v1.utils import Utils, VError
from api.v1.utils.authWrapper import login_required
from models.user import User
from models.chat.chat import Chat
from models.chat.chatSession import ChatSession
from models.chat.chatProvider import getChatResponse
from flasgger.utils import swag_from
from os import path
from sqlalchemy.exc import IntegrityError

DOCS_DIR = path.dirname(__file__) + '/documentations/chats'


@app_views.route('/chat_sessions', methods=['POST'])
@swag_from(f'{DOCS_DIR}/post_chat_session.yml')
@login_required()
def createChatSession():
    """Creates a new chat session for the current user"""
    data = request.get_json()
    newSession = None

    try:
        newSession = storage.createChatSession(g.currentUser.id, data.get('topic'))
    except VError as ev:
        abort(ev.statusCode, description=str(ev))

    return jsonify({
        "status": "success",
        "message": "Chat session created successfully",
        "data": newSession
    }), 201

@app_views.route('/chat_sessions', methods=['PUT'])
@swag_from(f'{DOCS_DIR}/put_chat_session.yml')
@login_required()
def updateChatSession():
    """Updates a chat session based on sessionID"""
    requiredFields = ['topic', 'sessionID']
    data = Utils.getReqJSON(request, requiredFields)
    session = None

    try:
        session = storage.get(ChatSession, data['sessionID'])
        if not session:
            abort(404, description="Chat session not found")
        elif session.userID != g.currentUser.id:
            abort(401, description="You are not authorized to update this chat session")
        
        setattr(session, 'topic', data.get('topic'))
        session.save()
    except IntegrityError as i:
        abort(409, description="This session topic already exist")
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e)),
            "data:": None
        }), 509

    return jsonify({
        "status": "success",
        "message": "Chat session updated successfully",
        "data": session.toDict()
    })

@app_views.route('/chat_sessions', methods=['GET'])
@swag_from(f'{DOCS_DIR}/get_user_sessions.yml')
@login_required()
def getUserSessions():
    """Retrieves the authenticated user's chat sessions"""
    sessions = None
    try:
        sessions = storage.getUserSessions(g.currentUser.id)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e)),
            "data:": None
        }), 509

    return jsonify({
        "status": "success",
        "message": "Chat sessions retrieved successfully",
        "data": sessions
    })

@app_views.route('/chats/<sessionID>', methods=['GET'])
@swag_from(f'{DOCS_DIR}/get_chats.yml')
@login_required()
def getSessionChats(sessionID):
    """Retrieves the chat history of a chat session"""
    chats = None
    try:
        chats = storage.getChatHistory(sessionID, g.currentUser.id)
    except VError as e:
        abort(e.statusCode, description=str(e))

    return jsonify({
        "status": "success",
        "message": "Chat history retrieved successfully",
        "data": chats
    })

@app_views.route('/chat_sessions/<id>', methods=['DELETE'])
@swag_from(f'{DOCS_DIR}/delete_chat_session.yml')
@login_required()
def deleteChatSession(id):
    """Deletes a chat session based on sessionID"""
    session = storage.get(ChatSession, id)

    if not session:
        abort(404, description="Chat session not found!")

    privilegedRoles = [UserRole.admin, UserRole.moderator]
    if session.userID != g.currentUser.id and g.currentUser.role not in privilegedRoles:
        abort(401, description="You are not authorized to delete this session!")

    try:
        storage.delete(session)
    except VError as e:
        abort(e.statusCode, description=str(e))

    return jsonify({
        "status": "success",
        "message": "Chat session deleted successfully",
        "data": None
    })

@app_views.route('/chats', methods=['POST'])
@swag_from(f'{DOCS_DIR}/post_chats.yml')
@login_required()
def processChat():
    """Processes user chat and returns response from the chatbot"""
    requiredFields = ['content', 'sessionID']
    try:
        data = Utils.getReqJSON(request, requiredFields)
        chatData = {}

        for key, value in data.items():
            if key in requiredFields:
                chatData[key] = value

        chatData['userID'] = g.currentUser.id
        chatData['role'] = 'user'
        
        chatHistory = storage.getChatHistory(chatData['sessionID'], g.currentUser.id)
        if chatHistory == []:
            abort(400, description="Invalid chat session!")

        newChat = Chat(**chatData)
        chatHistory = [{'role': chat.get('role'), 'content': chat.get(
            'content')} for chat in chatHistory]
        chatData.pop("userID")
        chatData.pop("sessionID")
        chatHistory.append(chatData)

        chatResponse = None
        try:
            chatResponse = getChatResponse(chatHistory)
            chatResponse['userID'] = g.currentUser.id
            chatResponse['sessionID'] = data['sessionID']
            chatResponse = Chat(**chatResponse)
            newChat.save()
            chatResponse.save()
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "data": None
            }), 503
    except (ValueError) as e:
        return jsonify({
            "status": "error",
            "message": Utils.extractErrorMessage(str(e))
        }), 400

    return jsonify({
        "status": "success",
        "message": "Response generated successfully",
        "data": [
            newChat.toDict(),
            chatResponse.toDict()
        ]
    })
