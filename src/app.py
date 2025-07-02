from flask import Flask, render_template, request, redirect, jsonify  
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Date
from sqlalchemy.orm import sessionmaker, declarative_base     
from datetime import datetime
import pymysql  
# from flask import jsonify 

app = Flask (__name__)

if __name__ == '__main__':
    app.run(debug=True)

engine = create_engine("mysql+pymysql://root@localhost/factura243?charset=utf8mb4")

connection = engine.connect()

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()
Base.metadata.bind = engine


@app.route('/')
def index():
    return render_template('index.html', titulo='Bienvenido a la aplicación de facturación')

@app.route('/lista_productos')
def lista_productos():
    try:
        productos = Productos.traer_productos()
        return render_template('lista_productos.html',titulo='Ver productos', productos = productos)
    except: 
        return render_template('lista_productos.html',titulo='Error conexión a la base de datos')

@app.route('/formulario_producto', methods=['GET','POST'])
def formulario_producto():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        descripcion = request.form.get('descripcion')
        producto =  session.query(Productos).filter(Productos.descripcion == descripcion).first()
        if producto:
            return render_template('formulario_producto.html',titulo='Error:producto repetido')
        valor_unitario = request.form.get('valor_unitario')
        cantidad_inventario = request.form.get('cantidad_inventario')        
        unidad_medida = request.form.get('unidad_medida')
        categoria = request.form.get('categoria')
        producto = Productos(codigo,descripcion,valor_unitario,unidad_medida,cantidad_inventario,categoria)
        
        try:
            Productos.crear_producto(producto)
        except: 
            return render_template('formulario_producto.html', titulo= 'Error al registrar en la base de datos')
        print("Entro por POST")
        print(codigo)
    categorias = Categorias.traer_categorias() 
    return render_template('formulario_producto.html', titulo= 'Crear Producto', categorias = categorias)


@app.route('/lista_facturacion')
def lista_facturacion():
    facturas = Facturas.traer_facturas()
    return render_template('lista_facturacion.html', titulo='Listado de Facturas', facturas = facturas) 

# @app.route('/formulario_facturacion', methods=['GET','POST'])
# def formulario_facturacion():
#     if request.method == 'POST':
#         id_factura = request.form.get('id_factura')
#         fecha = request.form.get('fecha')
#         cliente = request.form.get('cliente')
#         vendedor = request.form.get('vendedor')
#         producto = request.form.get('producto')
#         cantidad = request.form.get('cantidad')
#         factura = Facturas(id_factura, fecha, cliente, vendedor, producto, cantidad)
#     productos = Productos.traer_productos()
#     return render_template('formulario_facturacion.html', titulo='Crear Factura', productos = productos) 

@app.route('/formulario_facturacion', methods=['GET', 'POST'])
def formulario_facturacion():
    if request.method == 'POST':
         id_factura = request.form.get('id_factura')
         fecha = request.form.get('fecha')
         cliente = request.form.get('cliente')
         vendedor = request.form.get('vendedor')
         producto = request.form.get('producto')
         cantidad = request.form.get('cantidad')
         precio = request.form.get('precio')
         total = request.form.get('total')

         factura = Facturas(id_factura, fecha, cliente, vendedor, producto, cantidad, precio, total)
         session.add(factura)
         session.commit()
         return redirect('/lista_facturacion')

    productos = Productos.traer_productos()
    usuarios = Usuarios.traer_usuarios()
    nuevo_id = generar_id_factura()
    return render_template('formulario_facturacion.html', titulo='Crear Factura', productos=productos, usuarios = usuarios, 
                           nuevo_id=nuevo_id)


def generar_id_factura():
    ultima_factura = session.query(Facturas).order_by(Facturas.id_factura.desc()).first()
    if ultima_factura and ultima_factura.id_factura.startswith("INVOICE"):
        numero = int(ultima_factura.id_factura.replace("INVOICE", ""))
        nuevo_numero = numero + 1
    else:
        nuevo_numero = 1
    return f"INVOICE{nuevo_numero:03d}"


@app.route('/get_precio/<descripcion>')
def get_precio(descripcion):
    producto = session.query(Productos).filter_by(descripcion=descripcion).first()
    if producto:
        precio_formateado = "{:.2f}".format(producto.valor_unitario) 
        return jsonify({'precio': precio_formateado})
    return jsonify({'precio': "0.00"})


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
    usuarios = Usuarios.traer_usuarios()
    return render_template('formulario_usuarios.html', titulo='Crear Usuario', usuarios = usuarios)

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
    categorias = Categorias.traer_categorias()
    return render_template('formulario_categoria.html', titulo='Crear Categoría', categorias = categorias)

@app.route('/lista_usuarios1')
def lista_usuarios1():
    return render_template('lista_usuarios1.html', titulo='Listado de Usuarios1')

@app.route('/formulario_usuarios1')
def formulario_usuarios1():
    return render_template('formulario_usuarios1.html', titulo='Crear Usuario1')


class Productos(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    codigo = Column(String(9), unique=True, nullable=False)
    descripcion = Column(String(300), unique=True, nullable=False)
    valor_unitario = Column(Float(10,8))
    unidad_medida = Column(String(3), nullable=False)
    cantidad_stock = Column(Float(10,8))
    categoria = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    def __init__(self,codigo,descripcion,valor_unitario,unidad_medida,cantidad_stock,categoria):
        self.codigo = codigo
        self.descripcion = descripcion
        self.valor_unitario = valor_unitario
        self.unidad_medida = unidad_medida
        self.cantidad_stock = cantidad_stock
        self.categoria = categoria
    
    def crear_producto(producto):
        producto = session.add(producto)
        session.commit()
        return producto
    
    def traer_productos():
        productos = session.query(Productos).all()
        return productos 

class Categorias(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(300), unique=True, nullable=False)

    def __init__(self, nombre_categoria):
        self.nombre_categoria = nombre_categoria
    
    def crear_categoria(categoria):
        categoria = session.add(categoria)
        session.commit()
        return categoria

    def traer_categorias():
        categorias = session.query(Categorias).all()
        return categorias

class Usuarios(Base):
    __tablename__ = "Usuarios"
    id = Column(Integer, primary_key=True)
    tipo_usuario = Column(String(20), nullable=False)
    nombre = Column(String(50), nullable=False)
    tipo_de_documento = Column(String(25), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    direccion = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=False)


    def __init__(self,tipo_usuario, nombre, tipo_de_documento, numero_documento, telefono, fecha_nacimiento, direccion, correo):
        self.tipo_usuario = tipo_usuario
        self.nombre = nombre 
        self.tipo_de_documento = tipo_de_documento
        self.numero_documento = numero_documento
        self.telefono = telefono 
        self.fecha_nacimiento =fecha_nacimiento
        self.direccion = direccion
        self.correo = correo 
    
    def crear_usuario(usuario):
        usuario = session.add(usuario)
        session.commit()
        return usuario
   
    def traer_usuarios():
        usuarios = session.query(Usuarios).all()
        return usuarios

class Facturas(Base):
    __tablename__ = "facturas"
    id_factura = Column(String(20), primary_key=True)
    fecha = Column(Date)
    cliente = Column(String(100))
    vendedor = Column(String(100))
    producto = Column(String(100))
    cantidad = Column(Float(10,8))
    precio = Column(Float(10,8))
    total = Column(Float(10,8))

    def __init__(self, id_factura, fecha, cliente, vendedor, producto, cantidad, precio, total):
        self.id_factura = id_factura
        self.fecha = fecha
        self.cliente = cliente
        self.vendedor = vendedor
        self.producto = producto
        self.cantidad = cantidad
        self.precio = precio 
        self.total = total 

    def crear_factura(factura):
        factura = session.add(factura)
        session.commit()
        return factura
    
    def traer_facturas():
        facturas = session.query(Facturas).all()
        return facturas

Base.metadata.create_all(engine)