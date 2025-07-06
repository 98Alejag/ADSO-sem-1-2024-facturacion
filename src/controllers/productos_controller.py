from flask import render_template, request, flash, redirect, url_for 
from flask_controller import FlaskController 
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.app import app   
    
app.secret_key = 'mysecretkey'

class ProductosContorller(FlaskController):
    @app.route('/lista_productos')
    def lista_productos():
        try:
            productos = Productos.traer_productos()
            return render_template('lista_productos.html',titulo='Ver productos', productos = productos)
        except: 
            return render_template('lista_productos.html',titulo='Error conexión a la base de datos')

    @app.route('/formulario_producto', methods=['GET','POST'])
    def formulario_producto():
        categorias = Categorias.traer_categorias() 
        if request.method == 'POST':
            codigo = request.form.get('codigo')
            descripcion = request.form.get('descripcion')
            valor_unitario = request.form.get('valor_unitario')
            cantidad_inventario = request.form.get('cantidad_inventario') 
            unidad_medida = request.form.get('unidad_medida')
            categoria = request.form.get('categoria')
            producto_almacenar = Productos(codigo,descripcion,valor_unitario,unidad_medida,cantidad_inventario,categoria)        
            producto_repetido =  Productos.traer_producto_por_descripcion(descripcion)
            if producto_repetido:
                return render_template('formulario_producto.html'
                                    ,titulo='Crear un producto'
                                    ,errorProducto = "La descripción no se puede repetir"
                                    ,categorias = categorias
                                    ,producto_almacenar = producto_almacenar)
            try:
                Productos.crear_producto(producto_almacenar)
                flash('Producto agregado')
            except:            
                return render_template('formulario_producto.html',titulo='Error al registrar en la base de datos',categorias = categorias) 
        return render_template('formulario_producto.html',titulo='Crear un producto',categorias = categorias)

    
@app.route('/delete_producto', methods=['POST'])
def delete_producto():
    id = request.form.get('id')
    try:
        eliminado = Productos.delete_producto(id)
        if eliminado:
            flash('Producto eliminado exitosamente')
        else:
            flash('Producto no encontrado')
    except Exception as e:
        flash(f'Error al eliminar el producto: {str(e)}')
    return redirect(url_for('lista_productos'))

    
