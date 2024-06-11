from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import EnergyManager

app = FastAPI()
energyManager = EnergyManager()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/energyUsage/user/{user_email}/frequency/{frequency}")
async def read_item(user_email: str, frequency: str):
    try:
        device = await energyManager.authenticate(user_email)
        if not device:
            raise HTTPException(status_code=404, detail="User not found or device not authenticated")
        
        energyValues = await energyManager.showEnergyData(device, frequency)

        response =  {"energy_usage": energyValues}
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
