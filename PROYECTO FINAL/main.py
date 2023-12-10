#main
import pymongo
from bson import Binary
import base64
import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import boto3
from ImageHandler import ImageHandler

app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BRYAN:CADETE4507@localhost:3306/lenguajes'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '3.1415abcA'

class Idioma(db.Model):
    __tablename__ = "idioma"
    id = db.Column(db.Integer, primary_key=True)
    palabra = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(32), nullable=False)

app.config['MONGO_URI'] = 'mongodb://localhost:27018'
image_handler = ImageHandler()

def get_user_credentials():
    user_entry = Usuario.query.get(1)
    if user_entry:
        return user_entry.usuario, user_entry.contrasena
    else:
        return None, None

def check_credentials(username, password):
    user_db, password_db = get_user_credentials()
    return username == user_db and password == password_db

def traductor(texto, code):
    target_language_code = code
    source_language_code = 'auto'
    translate = boto3.client('translate', region_name='us-east-1')
    response = translate.translate_text(
        Text=texto,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code)
    return response['TranslatedText']

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if check_credentials(username, password):
        session['username'] = username
        return redirect(url_for('root'))
    else:
        return redirect(url_for('menu'))
    

@app.route('/root', methods=['GET', 'POST'])
def root():
    all_images = image_handler.get_all_images_base64()
    current_image_index = int(request.args.get('index', 0))
    current_image = all_images[current_image_index] if all_images and 0 <= current_image_index < len(all_images) else None
    idiomas = Idioma.query.all()
    palabra_original = "HELLO WORLD !"
    palabra_traducida = None
    if request.method == 'POST':
        idioma_code = request.form['idioma_code']
        palabra_traducida = traductor(palabra_original, idioma_code)
    return render_template('root.html', idiomas=idiomas, palabra_traducida=palabra_traducida, palabra_original=palabra_original, current_image=current_image, current_image_index=current_image_index)


#devuelve 1 imagen random de la base de datos    
def one_image():
    all_images = image_handler.get_all_images_base64()
    if all_images:
        random_index = random.randint(0, len(all_images) - 1)
        return all_images[random_index]
    else:
        return None
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    all_images = image_handler.get_all_images_base64()
    current_image_index = int(request.args.get('index', 0))
    current_image = one_image() if all_images else None
    idiomas = Idioma.query.all()
    palabra_original = "HELLO WORLD !"
    palabra_traducida = None
    if request.method == 'POST':
        idioma_code = request.form['idioma_code']
        palabra_traducida = traductor(palabra_original, idioma_code)
    return render_template('index.html', idiomas=idiomas, palabra_traducida=palabra_traducida, palabra_original=palabra_original, current_image=current_image, current_image_index=current_image_index)

@app.route('/')
def home():
    return render_template('login.html')



#funciones root--------------------------------------------------------------------------------------------------------------
@app.route('/add_language', methods=['POST'])
def add_language():
    if request.method == 'POST':
        palabra = request.form['palabra']
        code = request.form['code']
        new_language = Idioma(palabra=palabra, code=code)
        db.session.add(new_language)
        db.session.commit()
        return redirect(url_for('root'))
    return render_template('root.html')
@app.route('/delete_language', methods=['POST'])
def delete_language():
    idioma_code = request.form.get('idioma_code')
    idioma = Idioma.query.filter_by(code=idioma_code).first()
    if idioma:
        try:
            db.session.delete(idioma)
            db.session.commit()
            return redirect(url_for('root'))
        except:
            return 'Hubo un problema al intentar eliminar el idioma.'
    else:
        return 'No se encontró el idioma con el código proporcionado.'
@app.route('/add_img', methods=['POST'])
def add_img():
    if 'image' in request.files:
        image = request.files['image']
        image_handler.insert_image(image)
    return redirect(url_for('root'))
@app.route('/delete_image', methods=['POST'])
def delete_image():
    image_id = int(request.form.get('image_id'))
    image_index = int(request.form.get('image_index', 0))
    deleted_count = image_handler.delete_image_by_id(image_id)
    if deleted_count > 0:
        print(f'Imagen eliminada exitosamente.')
    else:
        print(f'La imagen no se encontró o hubo un error al eliminarla. ID: {image_id}')
    return redirect(url_for('root', index=image_index))




if __name__ == '__main__':
    app.run(debug=True)


