from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Vendedor
from app.schemas import VendedorCreate, VendedorOut
from typing import List

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.post("/", response_model=VendedorOut, status_code=201)
def criar_vendedor(dados: VendedorCreate, db: Session = Depends(get_db)):
    existente = db.query(Vendedor).filter(Vendedor.email == dados.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    vendedor = Vendedor(**dados.model_dump())
    db.add(vendedor)
    db.commit()
    db.refresh(vendedor)
    return vendedor


@router.get("/", response_model=List[VendedorOut])
def listar_vendedores(db: Session = Depends(get_db)):
    return db.query(Vendedor).all()
