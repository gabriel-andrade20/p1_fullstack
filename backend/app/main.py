from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routers import vendedores, produtos, cupons, pedidos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-commerce")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendedores.router)
app.include_router(produtos.router)
app.include_router(cupons.router)
app.include_router(pedidos.router)
