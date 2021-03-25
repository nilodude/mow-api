from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

from matlab_interface import MatlabInterface

app = FastAPI()


class Item(BaseModel):

    name: str

    price: float

    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/")
def start_matlab():
    matlab = MatlabInterface()
    matlab.run_script()
    return {"result: "}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):

    return {"item_name": item.name, "item_id": item_id}
