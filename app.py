from flask import Flask, render_template, request, redirect
import openai

app = Flask(__name__)

todos = []
generated_steps = {}

openai.api_key = "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"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo = request.form.get('todo')
        todos.append(todo)

    return render_template('index.html', todos=enumerate(todos), generated_steps=generated_steps)

@app.route('/generate-steps/<int:todo_id>', methods=['GET'])
def generate_steps(todo_id):
    todo = todos[todo_id]
    response = openai.Completion.create(engine="text-davinci-003", prompt=f"{todo}", max_tokens=60)
    generated_steps[todo_id] = response.choices[0].text.strip()
    return redirect('/')

@app.route('/delete-todo/<int:todo_id>', methods=['GET'])
def delete(todo_id):
    todos.pop(todo_id)
    if todo_id in generated_steps:
        generated_steps.pop(todo_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)