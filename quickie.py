from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return 'No file part'
    
    print(request.files)

    files = request.files.getlist('files[]')

    for file in files:
        print(file)
        if file.filename == '':
            return 'No selected file'
        # You can save the file to your desired location or perform other actions here
        file.save(f"uploads/{file.filename}")

    return 'Files uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
