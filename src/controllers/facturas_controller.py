from flask import render_template, request, redirect
from flask_controller import FlaskController 
from src.models.facturas import Facturas
from src.models.productos import Productos
from src.models.usuarios import Usuarios
from src.app import app 

class FacturasController(FlaskController):
    @app.route('/lista_facturacion')
    def lista_facturacion():
        facturas = Facturas.traer_facturas()
        return render_template('lista_facturacion.html', titulo='Facturas', facturas = facturas) 


    @app.route('/formulario_facturacion', methods=['GET', 'POST'])
    def formulario_facturacion():
        productos = Productos.traer_productos()
        usuarios = Usuarios.traer_usuarios()
        nuevo_id = Facturas.generar_id_factura()
        if request.method == 'POST':
            id_factura = request.form.get('id_factura')
            fecha = request.form.get('fecha')
            cliente = request.form.get('cliente')            
            numero_documento = request.form.get('numero_documento')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')
            correo = request.form.get('correo')
            vendedor = request.form.get('vendedor')
            producto = request.form.get('producto')
            cantidad = request.form.get('cantidad')
            precio = request.form.get('precio')
            total = request.form.get('total')
            factura = Facturas(id_factura, fecha, cliente, numero_documento, telefono, direccion, correo, vendedor, producto, cantidad, precio, total)
            Facturas.crear_factura(factura)
            return redirect('/lista_facturacion')

        return render_template('formulario_facturacion.html', titulo='Nueva Factura', productos=productos, usuarios = usuarios, 
                            nuevo_id=nuevo_id)


    

