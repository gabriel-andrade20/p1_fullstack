from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Pedido, Item, Produto, Cupom
from app.schemas import PedidoCreate, PedidoOut
from typing import List

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoOut, status_code=201)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    pedido = Pedido(cliente_nome=dados.cliente_nome)

    if dados.cupom_codigo:
        cupom = db.query(Cupom).filter(
            Cupom.codigo == dados.cupom_codigo,
            Cupom.ativo == True
        ).first()
        if not cupom:
            raise HTTPException(status_code=400, detail="Cupom inválido ou inativo")
        pedido.cupom_id = cupom.id

    db.add(pedido)
    db.flush()

    total = 0.0

    for item_data in dados.itens:
        produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto {item_data.produto_id} não encontrado")
        if produto.estoque < item_data.quantidade:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {produto.nome}")

        produto.estoque -= item_data.quantidade

        item = Item(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=item_data.quantidade,
            preco_unitario=produto.preco
        )
        db.add(item)
        total += produto.preco * item_data.quantidade

    if dados.cupom_codigo and pedido.cupom_id:
        cupom = db.query(Cupom).filter(Cupom.id == pedido.cupom_id).first()
        total -= total * (cupom.desconto / 100)

    pedido.total = round(total, 2)
    db.commit()
    db.refresh(pedido)
    return pedido


@router.get("/", response_model=List[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()


@router.get("/{pedido_id}", response_model=PedidoOut)
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.patch("/{pedido_id}/fechar", response_model=PedidoOut)
def fechar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.status == "fechado":
        raise HTTPException(status_code=400, detail="Pedido já está fechado")
    pedido.status = "fechado"
    db.commit()
    db.refresh(pedido)
    return pedido
