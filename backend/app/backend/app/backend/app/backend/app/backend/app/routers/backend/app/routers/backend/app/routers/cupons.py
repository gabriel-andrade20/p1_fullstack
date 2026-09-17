from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Cupom
from app.schemas import CupomCreate, CupomOut
from typing import List

router = APIRouter(prefix="/cupons", tags=["Cupons"])


@router.post("/", response_model=CupomOut, status_code=201)
def criar_cupom(dados: CupomCreate, db: Session = Depends(get_db)):
    existente = db.query(Cupom).filter(Cupom.codigo == dados.codigo).first()
    if existente:
        raise HTTPException(status_code=400, detail="Código de cupom já existe")
    cupom = Cupom(**dados.model_dump())
    db.add(cupom)
    db.commit()
    db.refresh(cupom)
    return cupom


@router.get("/", response_model=List[CupomOut])
def listar_cupons(db: Session = Depends(get_db)):
    return db.query(Cupom).all()
