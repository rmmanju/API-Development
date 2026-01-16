<<<<<<< HEAD
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/item={item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/item/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}   
@app.put("/item/{item_id}")
def update_item(item_id: int, name: str = None, price: float = None):
    return {"item_id": item_id, "name": name, "price": price}
=======
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/item={item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/item/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}   
    
>>>>>>> e85ad990d2492aed16c565ec2e65d266ac8cea21
