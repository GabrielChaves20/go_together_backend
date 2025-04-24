from sqlalchemy import Column, Integer, String, Float
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String)
    telefone = Column(String)
    senha = Column(String)
    endereco = Column(String)
    foto_perfil = Column(String)

class Motorista(Base):
    __tablename__ = "motoristas"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    cnh = Column(String)
    telefone = Column(String)
    crlv = Column(String)
    senha = Column(String)
    endereco = Column(String)
    foto_perfil = Column(String)

class Viagem(Base):
    __tablename__ = "viagens"
    id = Column(Integer, primary_key=True, index=True)
    passageiro = Column(String)
    motorista = Column(String)
    data = Column(String)
    horario = Column(String)
    valor = Column(Float)