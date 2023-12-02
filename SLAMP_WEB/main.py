from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BRYAN:CADETE4507@localhost:3306/diccionario'
db = SQLAlchemy(app)

class Dictionary(db.Model):
    __tablename__ = "dictionary"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), unique=True, nullable=False)
    meaning = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    words = Dictionary.query.all()
    return render_template('index.html', words=words)


@app.route('/add', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        word = request.form['word']
        meaning = request.form['meaning']
        new_word = Dictionary(word=word, meaning=meaning)
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit_word():
    existing_word = None

    if request.method == 'POST':
        word_to_edit = request.form['word_to_edit']
        existing_word = Dictionary.query.filter_by(word=word_to_edit).first()

    words = Dictionary.query.all()

    if request.method == 'POST':
        return render_template('edit.html', existing_word=existing_word, words=words, editing=True)
    else:
        return render_template('edit.html', existing_word=existing_word, words=words, editing=False)

@app.route('/save_edit', methods=['POST'])
def save_edit():
    existing_word_id = request.form['existing_word_id']
    new_word = request.form['new_word']
    new_meaning = request.form['new_meaning']

    existing_word = Dictionary.query.get(existing_word_id)

    if existing_word:
        existing_word.word = new_word
        existing_word.meaning = new_meaning
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return "Error: La palabra a editar no fue encontrada en la base de datos."



# app.py

@app.route('/delete', methods=['GET', 'POST'])
def delete_word():
    if request.method == 'POST':
        word_id_to_delete = request.form.get('word_to_delete')

        if not word_id_to_delete:
            return "Error: No se proporcionó un ID de palabra para eliminar."

        word = Dictionary.query.get(word_id_to_delete)

        if word:
            db.session.delete(word)
            db.session.commit()
            return redirect(url_for('home'))  
        else:
            return "Error: La palabra a eliminar no fue encontrada en la base de datos."

    return render_template('delete.html', words=Dictionary.query.all())



@app.route('/list')
def list_words():
    words = Dictionary.query.all()
    return render_template('lista.html', words=words)

@app.route('/search', methods=['GET', 'POST'])
def search_word():
    words = Dictionary.query.all()
    selected_word = None
    meaning = None

    if request.method == 'POST':
        selected_word_id = request.form['selected_word']
        selected_word = Dictionary.query.get(selected_word_id)

        if selected_word:
            meaning = selected_word.meaning

    return render_template('search.html', words=words, selected_word=selected_word, meaning=meaning)

@app.route('/exit')
def exit_app():
    return "¡Hasta luego!"
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)


