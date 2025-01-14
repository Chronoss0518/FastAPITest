from typing import Union
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from base.db_base import TableData

from db import PostgreSQL

app = FastAPI()

db = PostgreSQL("ip_address","dbname","username","password")

@app.get("/")
def read_root():
    obj = dict()
    obj["Hello"] = "World"
    return JSONResponse(content=obj)

@app.get("/get_user_list")
def read_user_list():
    return JSONResponse(content=db.get_user_list())

@app.get("/get_user/{id}")
def read_user(id: int):
    #user_table_desc = db.get_user_table_desk()
    user_list = db.get_user_table_where_id(id)
    
    res = {}
    if user_list != None:
        user_list = list(user_list)
        if len(user_list) > 0:
            #for num in range(len(user_table_desc)):
                #res[user_table_desc[num]] = user_list[0][num] 
            return JSONResponse(content=user_list[0])
    return JSONResponse(content={})

@app.get("/get_user_table")
def read_user_table():
    user_list = db.get_user_table()
    return JSONResponse(content=user_list)

@app.get("/get_table_list")
def read_user_table():
    user_list = db.get_table_list()
    return JSONResponse(content=user_list)

@app.get("/get_user_desc")
def read_user_table():
    data = db.get_table_structure_data("TestTable")
    return JSONResponse(content=data)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    obj = dict()
    obj["item_id"] = item_id
    obj["q"] = q
    return JSONResponse(content=obj)
