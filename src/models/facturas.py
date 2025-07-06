from sqlalchemy import Column, String, Float, Date 
from src.models import session, Base 

class Facturas(Base):
    __tablename__ = "facturas"
    id_factura = Column(String(20), primary_key=True)
    fecha = Column(Date, nullable=False)
    cliente = Column(String(100), nullable=False)
    vendedor = Column(String(100), nullable=False)
    producto = Column(String(100), nullable=False)
    cantidad = Column(Float(10,8), nullable=False)
    precio = Column(Float(10,8), nullable=False)
    total = Column(Float(10,8), nullable=False)

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
    
    # @staticmethod
    # def traer_precio_por_descripcion(cls, descripcion):    
    #     return session.query(cls).filter_by(descripcion=descripcion).first()
    
    # @staticmethod
    # def traer_producto_por_descripcion(cls, descripcion):
    #     return session.query(cls).filter_by(descripcion=descripcion).first()
    
    def generar_id_factura():
        ultima_factura = session.query(Facturas).order_by(Facturas.id_factura.desc()).first()
        if ultima_factura and ultima_factura.id_factura.startswith("INVOICE"):
            numero = int(ultima_factura.id_factura.replace("INVOICE", ""))
            nuevo_numero = numero + 1
        else:
            nuevo_numero = 1
        return f"INVOICE{nuevo_numero:04d}"
    
    @staticmethod
    def delete_factura(factura_id):
        factura = session.query(Facturas).filter_by(id_factura= factura_id).first()
        if factura:
            session.delete(factura)
            session.commit()
            return True
        return False

