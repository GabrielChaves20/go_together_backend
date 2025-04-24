from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import SessionLocal, engine
from models import Base, Cliente, Motorista

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana, senha_hash):
    return pwd_context.verify(senha_plana, senha_hash)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    email: str
    senha: str
    tipo: str

class ClienteCreate(BaseModel):
    email: str
    cpf: str
    telefone: str
    senha: str
    endereco: str
    foto_perfil: str

class MotoristaCreate(BaseModel):
    email: str
    cnh: str
    telefone: str
    crlv: str
    senha: str
    endereco: str
    foto_perfil: str

@app.post("/login/")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    if req.tipo == "cliente":
        user = db.query(Cliente).filter(Cliente.email == req.email).first()
    elif req.tipo == "motorista":
        user = db.query(Motorista).filter(Motorista.email == req.email).first()
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    if not user or not verificar_senha(req.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"message": "Login bem-sucedido", "id": user.id, "tipo": req.tipo}

@app.post("/cadastro/cliente/", status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(req: ClienteCreate, db: Session = Depends(get_db)):
    existente = db.query(Cliente).filter(Cliente.email == req.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado como cliente")

    novo = Cliente(
        email=req.email,
        cpf=req.cpf,
        telefone=req.telefone,
        senha=pwd_context.hash(req.senha),
        endereco=req.endereco,
        foto_perfil=req.foto_perfil
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"message": "Cliente cadastrado com sucesso", "id": novo.id}

@app.post("/cadastro/motorista/", status_code=status.HTTP_201_CREATED)
def cadastrar_motorista(req: MotoristaCreate, db: Session = Depends(get_db)):
    existente = db.query(Motorista).filter(Motorista.email == req.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado como motorista")

    novo = Motorista(
        email=req.email,
        cnh=req.cnh,
        telefone=req.telefone,
        crlv=req.crlv,
        senha=pwd_context.hash(req.senha),
        endereco=req.endereco,
        foto_perfil=req.foto_perfil
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"message": "Motorista cadastrado com sucesso", "id": novo.id}

class ViagemCreate(BaseModel):
    passageiro: str
    motorista: str
    data: str       # formato: "YYYY-MM-DD"
    horario: str    # formato: "HH:MM"
    valor: float

from models import Viagem

@app.post("/viagens/", status_code=status.HTTP_201_CREATED)
def criar_viagem(req: ViagemCreate, db: Session = Depends(get_db)):
    nova_viagem = Viagem(
        passageiro=req.passageiro,
        motorista=req.motorista,
        data=req.data,
        horario=req.horario,
        valor=req.valor
    )
    db.add(nova_viagem)
    db.commit()
    db.refresh(nova_viagem)
    return {"message": "Viagem criada com sucesso", "id": nova_viagem.id}

@app.get("/viagens/")
def listar_viagens(db: Session = Depends(get_db)):
    return db.query(Viagem).all()