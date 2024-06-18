from flask import Flask, request, render_template, redirect
import pickle
import base64

app = Flask(__name__, template_folder='templates')
real_flag = ''


with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


class Recipe:
    def __init__(self, name, recipe):
        self.name = name
        self.recipe = recipe


@app.route('/')
def index():
    return redirect('/recipe', code=302)


@app.route('/recipe', methods=['POST'])
def create_recipe():
    if request.method == 'POST':
        name = request.form.get('name')
        recipe = request.form.get('recipe')
        if name and recipe:
            recipe = Recipe(name, recipe)
            dumped = base64.b64encode(pickle.dumps(recipe)).decode()
            return redirect(f"/recipe?recipe={dumped}", code=302)
    return render_template('index.html')


@app.route('/recipe', methods=['GET'])
def get_recipe():
    recipe = request.args.get('recipe')
    if recipe:
        try:
            recipe_obj = pickle.loads(base64.b64decode(recipe))
            return render_template('recipe.html', recipe=recipe_obj, dumped=recipe)
        except pickle.UnpicklingError as e:
            return f"Error loading recipe: {str(e)}", 400

    return render_template('index.html')


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'


if __name__ == '__main__':
    app.run()
