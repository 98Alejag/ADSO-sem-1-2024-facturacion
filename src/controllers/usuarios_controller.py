from flask import render_template, request, flash, redirect, url_for
from flask_controller import FlaskController 
from src.models.usuarios import Usuarios
from datetime import datetime
from src.app import app 

app.secret_key = 'mysecretkey'

class UsuariosController(FlaskController):
    @app.route('/lista_usuarios')
    def lista_usuarios():
        try:
            usuarios = Usuarios.traer_usuarios()
            return render_template('lista_usuarios.html', titulo='Ver usuarios', usuarios = usuarios)
        except:
            return render_template('lista_usuarios.html',titulo='Error conexión a la base de datos')

    @app.route('/formulario_usuarios', methods=['GET','POST'])
    def formulario_usuarios():
        if request.method =='POST':
            tipo_usuario = request.form.get('tipo_usuario')
            nombre = request.form.get('nombre')
            tipo_de_documento = request.form.get('tipo_de_documento')
            numero_documento = request.form.get('numero_documento')
            telefono = request.form.get('telefono')
            fecha_nacimiento = datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d').date()
            direccion = request.form.get('direccion')
            correo = request.form.get('correo')
            usuario = Usuarios(tipo_usuario, nombre, tipo_de_documento, numero_documento, telefono, fecha_nacimiento, direccion, correo)
            Usuarios.crear_usuario(usuario)
            flash('Nuevo usuario creado')
        usuarios = Usuarios.traer_usuarios()
        return render_template('formulario_usuarios.html', titulo='Crear Usuario', usuarios = usuarios)

@app.route('/delete_usuario', methods=['POST'])
def delete_usuario():
    id = request.form.get('id')
    try:
        eliminado = Usuarios.delete_usuario(id)
        if eliminado:
            flash('Usuario eliminado exitosamente')
        else:
            flash('Usuario no encontrado')
    except Exception as e:
        flash(f'Error al eliminar el usuario: {str(e)}')
    return redirect(url_for('lista_usuarios'))
