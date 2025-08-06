from sqlalchemy import Column, String, Float, Date 
from src.models import session, Base 

class Facturas(Base):
    __tablename__ = "facturas"
    id_factura = Column(String(20), primary_key=True)
    fecha = Column(Date, nullable=False)
    cliente = Column(String(100), nullable=False)
    numero_documento = Column(String(20), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(100), nullable=False)
    correo = Column(String(50), nullable=False)
    vendedor = Column(String(100), nullable=False)
    producto = Column(String(100), nullable=False)
    cantidad = Column(Float(10,8), nullable=False)
    precio = Column(Float(10,8), nullable=False)
    total = Column(Float(10,8), nullable=False)

    def __init__(self, id_factura, fecha, cliente, numero_documento, telefono, direccion, correo, vendedor, producto, cantidad, precio, total):
        self.id_factura = id_factura
        self.fecha = fecha
        self.cliente = cliente
        self.numero_documento = numero_documento
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo
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
        facturas = session.query(Facturas).order_by(Facturas.id_factura)
        return facturas
        
    def generar_id_factura():
        ultima_factura = session.query(Facturas).order_by(Facturas.id_factura.desc()).first()
        if ultima_factura and ultima_factura.id_factura.startswith("INVOICE"):
            numero = int(ultima_factura.id_factura.replace("INVOICE", ""))
            nuevo_numero = numero + 1
        else:
            nuevo_numero = 1
        return f"INVOICE{nuevo_numero:04d}"
    

