from flask import render_template, request, flash 
from flask_controller import FlaskController
from src.models.categorias import Categorias
from src.app import app   

app.secret_key = 'mysecretkey'

class CategoriasController(FlaskController):
    @app.route('/lista_categoria')
    def lista_categoria():
        try:
            categorias = Categorias.traer_categorias()
            return render_template('lista_categoria.html', titulo='Ver categorías', categorias = categorias)
        except:
            return render_template('lista_categoria.html', titulo='Error de conexión a la base de datos')

    @app.route('/formulario_categoria', methods=['GET','POST'] )
    def formulario_categoria():
        if request.method == 'POST':
            nombre_categoria = request.form.get('nombre_categoria')
            categoria_almacenar = Categorias(nombre_categoria)
            categoria_repetida = Categorias.traer_categoria_por_nombre(nombre_categoria)
            if categoria_repetida:
                return render_template('formulario_categoria.html'
                                       , titulo='Crear Categoría'
                                       , errorNombre = "El nombre no se puede repetir"
                                       , categoria_almacenar = categoria_almacenar) 
            try:     
                Categorias.crear_categoria(categoria_almacenar)
                flash('Categoría creada')
            except:
                return render_template('formulario_categoria.html', titulo='Error al registrar en la base de datos')            
        return render_template('formulario_categoria.html', titulo='Crear Categoría')

    @app.route('/delete/<int:id>')
    def delete_categoria(id):
        try:
            eliminado = Categorias.delete_categoria(id)
            if eliminado:
                flash('Categoría eliminada exitosamente')
            else:
                flash('Categoría no encontrada')
        except: 
            flash ('Error al eliminar la categoría')
        return render_template('lista_categoria.html', titulo='Ver categorías', categorias=Categorias.traer_categorias())
    
    @app.route('/edit_categoria/<id>', methods=['GET', 'POST'])
    def edit_categoria(id):
        categoria = Categorias.obtener_categoria_por_id(id)
        if request.method == 'POST':
            nuevo_nombre = request.form.get('nombre_categoria')
            categoria_editada = Categorias.edit_categoria(id, nuevo_nombre)
            if categoria_editada:
                flash('Categoría editada exitosamente')
                return render_template('lista_categoria.html', titulo='Ver categorías', categorias=Categorias.traer_categorias())
        return render_template('edit_categoria.html', titulo='Editar Categoría', categoria=categoria)

    
