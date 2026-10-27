from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import date
from http import HTTPStatus
from uuid import uuid4


app = FastAPI()

class Gasto:
    def __init__(self, nome, valor, data):
        self.id: str = str(uuid4())
        self.nome = nome
        self.valor = valor
        self.data = data


class GastoEntrada(BaseModel):
    nome: str = Field(min_lenght=3)
    valor: float = Field(gt=0)
    data: date

class GastoSaida(GastoEntrada):
    id: str

gastos = []

@app.post("/gastos", status_code=HTTPStatus.CREATED)
def adicionar_gastos(gasto: GastoEntrada) -> GastoSaida:
    gasto = Gasto(gasto.nome, gasto.valor, gasto.data)
    gastos.append(gasto)
    return GastoSaida(id=gasto.id,nome=gasto.nome, valor=gasto.valor, data=gasto.data)


@app.get("/gastos")
def listar_gastos():
    return [{"ID": gasto.id ,"Nome": gasto.nome, "Valor": gasto.valor, "Data": gasto.data} for gasto in gastos]

@app.get("/gasto/{gasto_id}")
def obter_gasto(gasto_id:str):
    for gasto in gastos:
        if gasto.id == gasto_id:
            return GastoSaida(id=gasto.id,nome=gasto.nome, valor=gasto.valor, data=gasto.data)


adicionar_gastos(GastoEntrada(nome="Cinema", valor=50, data="2026-10-27"))
adicionar_gastos(GastoEntrada(nome="Jantar", valor=150, data="2026-10-27"))
adicionar_gastos(GastoEntrada(nome="Transporte", valor=250, data="2026-10-27"))