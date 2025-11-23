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
    
    def traer_usuario_por_nombre(nombre):
        usuario = session.query(Usuarios).filter(Usuarios.nombre == nombre).first()
        return usuario
    
    def traer_usuario_por_numero_documento(numero_documento):
        usuario = session.query(Usuarios).filter(Usuarios.numero_documento == numero_documento).first()
        return usuario
    
    def obtener_usuario_por_id(usuario_id):
        return session.query(Usuarios).get(usuario_id)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def obtener_cliente_por_nombre(nombre):
        usuario = session.query(Usuarios).filter(Usuarios.nombre == nombre).first()
        return usuario.as_dict()

    def edit_usuario(usuario_id, new_tipo_usuario, new_nombre, new_tipo_de_documento, new_numero_documento, 
                                                    new_telefono, new_fecha_nacimiento, new_direccion, new_correo):
        usuario = session.query(Usuarios).get(usuario_id)
        if usuario:
            usuario.tipo_usuario = new_tipo_usuario
            usuario.nombre = new_nombre 
            usuario.tipo_de_documento = new_tipo_de_documento
            usuario.numero_documento = new_numero_documento
            usuario.telefono = new_telefono 
            usuario.fecha_nacimiento = new_fecha_nacimiento
            usuario.direccion = new_direccion
            usuario.correo = new_correo
            session.commit()
        return usuario

    def delete_usuario(usuario_id):  
        usuario = session.query(Usuarios).filter_by(id=usuario_id).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            return True
        return False  
    
