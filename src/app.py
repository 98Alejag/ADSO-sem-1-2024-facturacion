from flask import Flask, render_template

app = Flask (__name__)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html', titulo='Bienvenido a la aplicación de facturación')

@app.route('/lista_productos')
def lista_productos():
    return render_template('lista_productos.html', titulo= 'Listado de Productos')

@app.route('/formulario_producto')
def formulario_producto():
    return render_template('formulario_producto.html', titulo= 'Crear Producto')

@app.route('/lista_facturacion')
def lista_facturacion():
    return render_template('lista_facturacion.html', titulo='Listado de Facturas') 

@app.route('/formulario_facturacion')
def formulario_facturacion():
    return render_template('formulario_facturacion.html', titulo='Crear Factura') 

@app.route('/lista_clientes')
def lista_clientes():
    return render_template('lista_clientes.html', titulo='Listado de Clientes')

@app.route('/formulario_clientes')
def formulario_clientes():
    return render_template('formulario_clientes.html', titulo='Crear Clientes')

@app.route('/lista_categoria')
def lista_categoria():
    return render_template('lista_categoria.html', titulo='Listado de Categorias')

@app.route('/formulario_categoria')
def formulario_categoria():
    return render_template('formulario_categoria.html', titulo='Crear Categoria')

@app.route('/lista_usuarios')
def lista_usuarios():
    return render_template('lista_usuarios.html', titulo='Listado de Usuarios')

@app.route('/formulario_usuarios')
def formulario_usuarios():
    return render_template('formulario_usuarios.html', titulo='Crear Usuario')