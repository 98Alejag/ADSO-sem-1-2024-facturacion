from flask import render_template, request, flash, redirect, url_for, jsonify
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
            usuario_almacenar = Usuarios(tipo_usuario, nombre, tipo_de_documento, numero_documento, telefono, fecha_nacimiento, direccion, correo)
            nombre_repetido = Usuarios.traer_usuario_por_nombre(nombre)
            documento_repetido = Usuarios.traer_usuario_por_numero_documento(numero_documento)
            if nombre_repetido:
                return render_template('formulario_usuarios.html'
                                       , titulo='Crear Usuario'
                                       , errorNombre = "El nombre no se puede repetir"
                                       , usuario_almacenar = usuario_almacenar)
            if documento_repetido:
                return render_template('formulario_usuarios.html'
                                       , titulo='Crear Usuario'
                                       , errorNumero = "El número del documento no se puede repetir"
                                       , usuario_almacenar = usuario_almacenar)
            try:
                Usuarios.crear_usuario(usuario_almacenar)
                flash('Nuevo usuario creado')
            except: 
                return render_template('lista_usuarios.html',titulo='Error conexión a la base de datos') 
        return render_template('formulario_usuarios.html', titulo='Crear Usuario')

    @app.route('/delete_usuario', methods=['POST'])
    def delete_usuario():
        id = request.form.get('id')
        try:
            eliminado = Usuarios.delete_usuario(id)
            if eliminado:
                flash('Usuario eliminado exitosamente')
            else:
                flash('Usuario no encontrado')
        except:
            flash('Error al eliminar el usuario')
        return redirect(url_for('lista_usuarios'))
    
    @app.route('/edit_usuario/<id>', methods=['POST', 'GET'])
    def edit_usuario(id):
        usuario = Usuarios.obtener_usuario_por_id(id)
        if request.method == 'POST':
            new_tipo_usuario = request.form.get('tipo_usuario')
            new_nombre = request.form.get('nombre')
            new_tipo_de_documento = request.form.get('tipo_de_documento')
            new_numero_documento = request.form.get('numero_documento')
            new_telefono = request.form.get('telefono')
            new_fecha_nacimiento = datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d').date()
            new_direccion = request.form.get('direccion')
            new_correo = request.form.get('correo')
            nombre_repetido = Usuarios.traer_usuario_por_nombre(new_nombre)
            documento_repetido = Usuarios.traer_usuario_por_numero_documento(new_numero_documento)
            if nombre_repetido and nombre_repetido.id != usuario.id:
                return render_template('edit_usuario.html'
                                       , titulo='Editar Usuario'
                                       , errorNombre = "El nombre no se puede repetir"
                                       , usuario = usuario)
            if documento_repetido and documento_repetido.id != usuario.id:
                return render_template('edit_usuario.html'
                                       , titulo='Editar Usuario'
                                       , errorNumero = "El número del documento no se puede repetir"
                                       , usuario = usuario)
            usuario_editado = Usuarios.edit_usuario(id, new_tipo_usuario, new_nombre, new_tipo_de_documento, new_numero_documento, 
                                                    new_telefono, new_fecha_nacimiento, new_direccion, new_correo)
            if usuario_editado:
                flash('Usuario editado exitosamente')
                usuarios = Usuarios.traer_usuarios()
                return render_template('lista_usuarios.html', titulo='Ver usuarios', usuarios = usuarios)
        return render_template('edit_usuario.html', titulo="Editar usuario", usuario=usuario)
    
    @app.route('/consultar_cliente_por_nombre/<nombre>')
    def consultar_cliente_por_nombre(nombre):
        cliente = Usuarios.obtener_cliente_por_nombre(nombre)
        return cliente
