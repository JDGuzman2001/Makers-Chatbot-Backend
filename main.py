from openai import OpenAI
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
import json
from inventory import json_with_uuid
from OpenAIKey import api_key
import uuid

client = OpenAI(
    api_key= api_key
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)





# Cargar el inventario al inicio
inventory = json.loads(json_with_uuid)

@app.get("/inventory")
async def get_inventory():
    global inventory
    return inventory


@app.post("/inventory/add")
async def add_item(brand: str = Form(...), price: int = Form(...), quantity: int = Form(...)):
    global inventory
    new_item = {
        "brand": brand,
        "price": price,
        "quantity": quantity,
        "id": str(uuid.uuid4())
    }
    inventory.append(new_item)

    return inventory

    # return {"message": "Item added successfully", "item": new_item}

@app.post("/inventory/update")
async def update_item(id: str = Form(...), brand: str = Form(...), price: int = Form(...), quantity: int = Form(...)):
    global inventory
    for item in inventory:
        if item["id"] == id:
            item["brand"] = brand
            item["price"] = price
            item["quantity"] = quantity
            return inventory
            # return {"message": "Item updated successfully", "item": item}



@app.delete("/inventory/delete")
async def delete_item(id: str = Form(...)):
    global inventory
    inventory = [item for item in inventory if item["id"] != id]

    return inventory

    # return {"message": "Item deleted successfully"}



@app.post("/chatbot")
async def get_response(request: Request):
    pregunta = await request.form()
    pregunta_texto = pregunta.get("pregunta")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You are a useful assistant. Provide the answer in string format, structure your response so that it seems like a natural conversation., without line breaks, do not continue with the answer. Use the inventory delimited by triple quotes Inventory:```{inventory}`` `"},
            {"role": "user", "content": pregunta_texto}
        ],
        temperature=0,
        max_tokens=150
    )

    answer_json = response.choices[0].message.content
    return answer_json






if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
