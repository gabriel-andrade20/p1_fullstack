import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base

engine_test = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)


def override_get_db():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_banco():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)


def test_criar_vendedor():
    response = client.post("/vendedores/", json={"nome": "João", "email": "joao@email.com"})
    assert response.status_code == 201
    assert response.json()["nome"] == "João"


def test_criar_produto():
    vendedor = client.post("/vendedores/", json={"nome": "Maria", "email": "maria@email.com"}).json()
    response = client.post("/produtos/", json={
        "nome": "Camiseta",
        "preco": 49.90,
        "estoque": 10,
        "vendedor_id": vendedor["id"]
    })
    assert response.status_code == 201
    assert response.json()["estoque"] == 10


def test_criar_pedido_e_baixar_estoque():
    vendedor = client.post("/vendedores/", json={"nome": "Ana", "email": "ana@email.com"}).json()
    produto = client.post("/produtos/", json={
        "nome": "Tênis",
        "preco": 199.90,
        "estoque": 5,
        "vendedor_id": vendedor["id"]
    }).json()

    response = client.post("/pedidos/", json={
        "cliente_nome": "Carlos",
        "itens": [{"produto_id": produto["id"], "quantidade": 2}]
    })

    assert response.status_code == 201
    assert response.json()["total"] == 399.80

    produto_atualizado = client.get(f"/produtos/{produto['id']}").json()
    assert produto_atualizado["estoque"] == 3


def test_pedido_com_cupom():
    vendedor = client.post("/vendedores/", json={"nome": "Beto", "email": "beto@email.com"}).json()
    produto = client.post("/produtos/", json={
        "nome": "Calça",
        "preco": 100.0,
        "estoque": 10,
        "vendedor_id": vendedor["id"]
    }).json()
    client.post("/cupons/", json={"codigo": "DESC10", "desconto": 10})

    response = client.post("/pedidos/", json={
        "cliente_nome": "Luana",
        "itens": [{"produto_id": produto["id"], "quantidade": 1}],
        "cupom_codigo": "DESC10"
    })

    assert response.status_code == 201
    assert response.json()["total"] == 90.0


def test_estoque_insuficiente():
    vendedor = client.post("/vendedores/", json={"nome": "Pedro", "email": "pedro@email.com"}).json()
    produto = client.post("/produtos/", json={
        "nome": "Meia",
        "preco": 15.0,
        "estoque": 1,
        "vendedor_id": vendedor["id"]
    }).json()

    response = client.post("/pedidos/", json={
        "cliente_nome": "Fernanda",
        "itens": [{"produto_id": produto["id"], "quantidade": 5}]
    })

    assert response.status_code == 400


def test_listar_pedidos():
    vendedor = client.post("/vendedores/", json={"nome": "Rafa", "email": "rafa@email.com"}).json()
    produto = client.post("/produtos/", json={
        "nome": "Boné",
        "preco": 30.0,
        "estoque": 5,
        "vendedor_id": vendedor["id"]
    }).json()
    client.post("/pedidos/", json={
        "cliente_nome": "Julia",
        "itens": [{"produto_id": produto["id"], "quantidade": 1}]
    })

    response = client.get("/pedidos/")
    assert response.status_code == 200
    assert len(response.json()) == 1
