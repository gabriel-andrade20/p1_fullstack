from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Vendedor(Base):
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    produtos = relationship("Produto", back_populates="vendedor")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"), nullable=False)
    vendedor = relationship("Vendedor", back_populates="produtos")
    itens = relationship("Item", back_populates="produto")


class Cupom(Base):
    __tablename__ = "cupons"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    desconto = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)
    pedidos = relationship("Pedido", back_populates="cupom")


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String, nullable=False)
    status = Column(String, default="aberto")
    total = Column(Float, default=0.0)
    criado_em = Column(DateTime, default=datetime.utcnow)
    cupom_id = Column(Integer, ForeignKey("cupons.id"), nullable=True)
    cupom = relationship("Cupom", back_populates="pedidos")
    itens = relationship("Item", back_populates="pedido")


class Item(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")
