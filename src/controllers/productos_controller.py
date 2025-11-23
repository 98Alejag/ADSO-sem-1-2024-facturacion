from flask import render_template, request, flash, redirect, url_for, jsonify 
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
            codigo_repetido = Productos.traer_producto_por_codigo(codigo)
            if producto_repetido:
                return render_template('formulario_producto.html'
                                    ,titulo='Crear un producto'
                                    ,errorProducto = "La descripción no se puede repetir"
                                    ,categorias = categorias
                                    ,producto_almacenar = producto_almacenar)
            if codigo_repetido:
                return render_template('formulario_producto.html'
                                    ,titulo='Crear un producto'
                                    ,errorCodigo = "El código no se puede repetir"
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
        except:
            flash('Error al eliminar el producto')
        return redirect(url_for('lista_productos'))

    @app.route('/edit_producto/<id>', methods=['GET', 'POST'])
    def edit_producto(id):
        categorias = Categorias.traer_categorias() 
        producto = Productos.obtener_producto_por_id(id)
        if request.method == 'POST':
            new_codigo = request.form.get('codigo')
            new_descripcion = request.form.get('descripcion')
            new_valor_unitario = request.form.get('valor_unitario')
            new_cantidad_inventario = request.form.get('cantidad_inventario') 
            new_unidad_medida = request.form.get('unidad_medida')
            new_categoria = request.form.get('categoria')
            producto_repetido =  Productos.traer_producto_por_descripcion(new_descripcion)
            codigo_repetido = Productos.traer_producto_por_codigo(new_codigo)            
            if producto_repetido and producto_repetido.id != producto.id:
                return render_template('edit_producto.html'
                                    ,titulo='Ver productos'
                                    ,errorProducto = "La descripción no se puede repetir"
                                    ,categorias = categorias
                                    ,producto = producto)
            if codigo_repetido and codigo_repetido.id != producto.id:
                return render_template('edit_producto.html'
                                    ,titulo='Ver productos'
                                    ,errorCodigo = "El código no se puede repetir"
                                    ,categorias = categorias
                                    ,producto = producto)
            producto_editado = Productos.edit_producto( id, new_codigo, new_descripcion, new_valor_unitario, new_unidad_medida
                      , new_cantidad_inventario, new_categoria)
            if producto_editado:
                flash('Producto editado exitosamente')
                productos=Productos.traer_productos()
                return render_template('lista_productos.html',titulo='Ver productos', productos=productos)
        return render_template('edit_producto.html', titulo="Editar Producto", producto=producto, categorias=categorias)
    
    @app.route('/get_precio/<descripcion>')
    def get_precio(descripcion):
        producto = Productos.traer_producto_por_descripcion(descripcion)
        if producto:
            precio_formateado = "{:.2f}".format(producto.valor_unitario)
            return jsonify({'precio': precio_formateado})
        return jsonify({'precio': "0.00"})