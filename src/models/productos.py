from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import session, Base
from src.models.categorias import Categorias 
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

    def traer_producto_por_descripcion(descripcion):
        producto = session.query(Productos).filter(Productos.descripcion == descripcion).first()
        return producto
       
    def traer_producto_por_codigo(codigo):
        producto = session.query(Productos).filter(Productos.codigo == codigo).first()
        return producto
    
    def delete_producto(producto_id):  
        producto = session.query(Productos).filter_by(id=producto_id).first()
        if producto:
            session.delete(producto)
            session.commit()
            return True
        return False    