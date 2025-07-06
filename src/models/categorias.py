from sqlalchemy import Column, Integer, String
from src.models import session, Base 

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
    
    @staticmethod
    def delete_categoria(categoria_id):
        categoria = session.query(Categorias).filter_by(id=categoria_id).first()
        if categoria:
            session.delete(categoria)
            session.commit()
            return True
        return False
    
    # def editar_categoria()
    #     categoria = session.query.get(id)
    #     categoria = Categorias.     