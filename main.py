from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi import HTTPException
app = FastAPI()


# # Home Route
@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI"}


# # about page
# @app.get("/about")
# def about():
#     return {"message":"This is about page"}

# # Users page
# @app.get("/users")
# def users():
#     return {"message":"This is User page"}

# users route
# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     return {"user_id":user_id}

# query Params(Parameter)
# @app.get("/users")
# def get_users(name: str = None):
#     return {"name":name}

# @app.get("/products")
# def get_items(limit: int = 10):
#     return {"limit":limit}

# @app.get("/items")
# def get_items(name: str = None, price: int= 0):
#     return {
#         "name": name,
#         "price":price
#         }
# @app.post("/add-products")
# # def add_products(name:str,price:int):
# def add_products(products:dict):
#     return {
#         "message":"Product added",
#         "data":products
#         # "name":name, "price":price
#     }

# Pydantic
class Products(BaseModel):
    name: str
    price: int


@app.post("/add-products")
# def add_products(name:str,price:int):
def add_products(products: Products):
    return {
        "message": "Product added",
        "data": products,
        # "name":name, "price":price
    }


# class User(BaseModel):
#     name:str
#     age:int
#     email:str

# @app.post("/create-user")
# def create_user(user:User):
#     return {
#         "message":"user created successfully",
#         "data":user
#     }

# nested pydantic models
# data is in the form of nested
from typing import List


class Country(BaseModel):
    name: str


class Address(BaseModel):
    city: str
    pincode: int
    country: Country


class Hobby(BaseModel):
    name: str


class User(BaseModel):
    name: str
    age: int
    email: str
    address: Address
    hobby: List[Hobby]


@app.post("/create-user")
def create_user(user: User):
    return {"message": "user created successfully", "data": user}


# ......................................


# status code -> codes that tell the client whether an API request succeeded or failed.

# 200 - OK - Successfully retrieved data.
# 201 - Created - Successfully created a new resource.
# 202 - Accepted - Request accepted for processing.
# 204 - No Content - Request succeeded, but there is no response body.
# 400 - Bad Request - The request is invalid.
# 401 - Unauthorized - Authentication is required or invalid.
# 403 - Forbidden - You don't have permission to access the resource.
# 404 - Not Found - The requested resource doesn't exist.
# 405 - Method Not Allowed - The HTTP method isn't supported for that endpoint.
# 409 - Conflict - The request conflicts with existing data, such as a duplicate ID.
# 422 - Unprocessable Content - The request data failed validation.
# 429 - Too Many Requests - Too many requests were sent in a given period.
# 500 - Internal Server Error - An unexpected server-side error occurred.
# 502 - Bad Gateway - A server acting as a gateway received an invalid response.
# 503 - Service Unavailable - The server is temporarily unavailable.

# status_code: Defines the normal response status
# HTTPException: Handles errors such as 404, 409, and 403.
# 200 Ok- fast API automatically returns it


# crud app - Movie Watchlist API
movies = []

class Director(BaseModel):
    name: str
    country: str


class Movie(BaseModel):
    id: int
    title: str
    year: int
    rating: int
    isWatched: bool
    director: Director


@app.post("/add-movies", status_code=status.HTTP_201_CREATED)
# def func(parameter:class(model))
def add_movies(movie: Movie):
    for exesting_movie in movies:
        if exesting_movie.id == movie.id:
            raise HTTPException(
                status_code=409, 
                detail="movie with this ID is already exists"
            )
    # append()-> Python list method used to add a new item to the end of a list.
    movies.append(movie)
    return {
        "message": "Movie added succesfully", 
        "data": movie
            }

# get all movies
@app.get("/movies")
def get_movies():
    if not movies:
        return {"message": "Movie not found", "data": []}
    return {"message": "Movie found succesfully", "data": movies}

# Query parameters
# get all movies which is watched
@app.get("/movies")
def get_movies(isWatched:bool | None = None):
    if isWatched is None:
        return movies
    return [
        movie for movie in movies
        if movie.isWatched == isWatched
        ]
        
    
# get single movie
@app.get("/movies/{movie_id}")
def get_movies_id(movie_id: int):
    for movie in movies:
        if movie.id == movie_id:
            return movie
        raise HTTPException(
            status_code=404, 
            detail="Movie not found"
            )

# update movies(put)
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: Movie):
    for index, movie in enumerate(movies):
        if movie.id == movie_id:
            movies[index] = updated_movie
            return {"message": "movie updated successfully", "data": updated_movie}
    return {"error": "movie not found"}


# delete movies
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for movie in movies:
        if movie.id == movie_id:
            movies.remove(movie)
            return {"message": "movie deleted successfully", "data": movie}
    return {"error": "movie not found"}


# response models
# frontend only see the those data stored in response models
class User(BaseModel):
    name:str
    age:int 
    password: str

class UserResponse(BaseModel):
    name:str
    age:int
    
@app.get("/user", response_model=UserResponse)
def get_user():
    return{
        "name":"don",
        "age":19,
        "password":"123456"
    }
    
# status code -> codes that tell the client whether an API request succeeded or failed.
# 200 - OK - Successfully retrieved data.
# 201 - Created - Successfully created a new resource.
# 202 - Accepted - Request accepted for processing.
# 204 - No Content - Request succeeded, but there is no response body.
# 400 - Bad Request - The request is invalid.
# 401 - Unauthorized - Authentication is required or invalid.
# 403 - Forbidden - You don't have permission to access the resource.
# 404 - Not Found - The requested resource doesn't exist.
# 405 - Method Not Allowed - The HTTP method isn't supported for that endpoint.
# 409 - Conflict - The request conflicts with existing data, such as a duplicate ID.
# 422 - Unprocessable Content - The request data failed validation.
# 429 - Too Many Requests - Too many requests were sent in a given period.
# 500 - Internal Server Error - An unexpected server-side error occurred.
# 502 - Bad Gateway - A server acting as a gateway received an invalid response.
# 503 - Service Unavailable - The server is temporarily unavailable.

# status_code: Defines the normal response status
# HTTPException: Handles errors such as 404, 409, and 403.
# 200 Ok- fast API automatically returns it



