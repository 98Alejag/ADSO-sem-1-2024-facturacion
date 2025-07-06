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
            categoria = Categorias(nombre_categoria)
            Categorias.crear_categoria(categoria)
            flash('Categoría creada')
        categorias = Categorias.traer_categorias()
        return render_template('formulario_categoria.html', titulo='Crear Categoría', categorias = categorias)

    @app.route('/delete/<int:id>')
    def delete_categoria(id):
        try:
            eliminado = Categorias.delete_categoria(id)
            if eliminado:
                flash('Categoría eliminada exitosamente')
            else:
                flash('Categoría no encontrada')
        except Exception as e: 
            flash (f'Error al eliminar la categoría: {str(e)}')
        return render_template('lista_categoria.html', titulo='Ver categorías', categorias=Categorias.traer_categorias())

    # @app.route('/editar_categorias/<int:id>')
    # def edit_categorias(id):
