from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class VendedorCreate(BaseModel):
    nome: str
    email: str


class VendedorOut(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True


class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    estoque: int
    vendedor_id: int


class ProdutoOut(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int
    vendedor_id: int

    class Config:
        from_attributes = True


class CupomCreate(BaseModel):
    codigo: str
    desconto: float


class CupomOut(BaseModel):
    id: int
    codigo: str
    desconto: float
    ativo: bool

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    produto_id: int
    quantidade: int


class ItemOut(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    cliente_nome: str
    itens: List[ItemCreate]
    cupom_codigo: Optional[str] = None


class PedidoOut(BaseModel):
    id: int
    cliente_nome: str
    status: str
    total: float
    criado_em: datetime
    itens: List[ItemOut]

    class Config:
        from_attributes = True
