from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    recipe_images = request.files.getlist('recipe_images[]')
    ingredient_images = request.files.getlist('ingredient_images[]')
    instruction_images = request.files.getlist('instruction_images[]')

    # Process each category of files as needed
    for file in recipe_images:
        print(file)
        # if file.filename != '':
        #     file.save(f"uploads/recipe_images/{file.filename}")

    for file in ingredient_images:
        print(file)
        # if file.filename != '':
            # file.save(f"uploads/ingredient_images/{file.filename}")

    for file in instruction_images:
        print(file)
        # if file.filename != '':
        #     file.save(f"uploads/instruction_images/{file.filename}")

    return 'Files uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
