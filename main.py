from fastapi import FastAPI

app = FastAPI()

# # Home Route
@app.get("/")
def home():
    return{"message":"Welcome to the FastAPI"}

# # about page
# @app.get("/about")
# def about():
#     return {"message":"This is about page"}

# # Users page
# @app.get("/users")
# def users():
#     return {"message":"This is User page"}

#users route
# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     return {"user_id":user_id}

#query Params(Parameter)
@app.get("/users")
def get_users(name: str = None):
    return {"name":name}

@app.get("/products")
def get_items(limit: int = 10):
    return {"limit":limit}

@app.get("/items")
def get_items(name: str = None, price: int= 0):
    return {
        "name": name,
        "price":price
        }
# @app.post("/add-products")
# # def add_products(name:str,price:int):
# def add_products(products:dict):
#     return {
#         "message":"Product added",
#         "data":products
#         # "name":name, "price":price
#     }
    
# Pydantic
from pydantic import BaseModel

class Products(BaseModel):
    name:str
    price:int

@app.post("/add-products")
# def add_products(name:str,price:int):
def add_products(products:Products):
    return {
        "message":"Product added",
        "data":products
        # "name":name, "price":price
    }
     
