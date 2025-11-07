'''
GET, POST, PUT, DELETE methods Status codes JSON responses
uvicorn day1:app --reload
from pydantic import BaseModel

'''
from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel
from fastapi import HTTPException, status


app = FastAPI()

#🧠 1️⃣ Basic GET – return simple message
@app.get('/')
def home():
    return f"This is homepage"

# 🔹 2️⃣ GET with path parameter
@app.get('/hello/{name}')
def say_hello(name:str):
    return {"response":f"Hello, {name}"}

# 🔹 3️⃣ GET with query parameters
@app.get('/search')
def search(q:str, limit:int=10):
    return {"query":q,"limit":limit}

# 🔹 4 GET with optional query parameter from typing import Optional
@app.get("/search_opt")
def search_opt(name: Optional[str]=None):
    if name:
        return {"message": f"Hello, {name}!"}
    return {"message": "Hello, Guest!"}

#######POST################
#🧠 1️⃣ Basic POST — Send simple data
@app.post('/basic_post')
def basic_post():
    return f"This is basic post"

#🔹 2️⃣ POST with JSON body (dictionary)
@app.post('/create_item')
def create_item(item:dict):
    return {"response":"Item_created","data":item}
# 🔹 3️⃣ POST with data validation using Pydantic model
#import this -- from pydantic import BaseModel
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post('/Items')
def add_items(all_item:Item):
    return {"response":"Item added !!!","all Items":all_item}

#add multiple Items #import list from item
@app.post('/Items_multi')
def add_item_multi(all_item:List[Item]):
    return {"response":"Item added !!!","all Items":all_item}

#🧠 1️⃣ Basic PUT — Update a single field
@app.put("/update-message")
def update_message():
    return {"message": "PUT method called — data updated!"}

#🔹 2️⃣ PUT with Path Parameter — Update by ID PUT /items/2?new_name=Orange
items = {1: "Apple", 2: "Banana", 3: "Mango"}

@app.put("/items/{item_id}")
def update_item(item_id: int, new_name: str):
    if item_id not in items:
        return {"error": "Item not found!"}
    items[item_id] = new_name
    return {"message": "Item updated successfully!", "items": items}

#🔹 3️⃣ PUT with JSON body (using Pydantic model)
items = {
    1: {"name": "Apple", "price": 50, "in_stock": True},
    2: {"name": "Banana", "price": 30, "in_stock": True}
}

@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    if item_id not in items:
        return {"error": "Item not found!"}
    items[item_id] = updated_item.dict()
    return {"message": "Item updated successfully!", "updated_item": items[item_id]}

#🔹 4️⃣ PUT with Partial Update Logic (simulate PATCH-like behavior) {  "price": 60 }
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None

items = {
    1: {"name": "Apple", "price": 50, "in_stock": True},
    2: {"name": "Banana", "price": 30, "in_stock": True}
}

@app.put("/update/{item_id}")
def update_partial_item(item_id: int, item_update: ItemUpdate):
    if item_id not in items:
        return {"error": "Item not found!"}
    
    for field, value in item_update.dict(exclude_unset=True).items():
        items[item_id][field] = value
    
    return {"message": "Item partially updated!", "item": items[item_id]}

#🧠 1️⃣ Basic DELETE — simple message
@app.delete("/delete")
def delete_item():
    return {"message": "DELETE method called — item removed!"}

#🔹 2️⃣ DELETE by Path Parameter (Delete by ID) DELETE /items/2
items = {1: "Apple", 2: "Banana", 3: "Mango"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        return {"error": "Item not found!"}
    deleted = items.pop(item_id)
    return {"message": f"'{deleted}' deleted successfully!", "remaining_items": items}

#🔹 3️⃣ DELETE with Query Parameter (Delete by name) DELETE /delete-by-name?name=Apple
items = ["Apple", "Banana", "Mango", "Apple"]

@app.delete("/delete-by-name")
def delete_by_name(name: str):
    if name not in items:
        return {"error": f"'{name}' not found!"}
    while name in items:
        items.remove(name)
    return {"message": f"All '{name}' removed successfully!", "remaining_items": items}

#🔹 4️⃣ DELETE with Error Handling and Status Code
#from fastapi import HTTPException, status


items = {1: "Laptop", 2: "Mouse", 3: "Keyboard"}

@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int):
    if product_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    deleted_item = items.pop(product_id)
    return {"message": "Product deleted successfully!", "deleted": deleted_item}
