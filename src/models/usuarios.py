from sqlalchemy import Column, Integer, String, Date 
from src.models import session, Base

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
    
    @staticmethod
    def delete_usuario(usuario_id):  
        usuario = session.query(Usuarios).filter_by(id=usuario_id).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            return True
        return False  
