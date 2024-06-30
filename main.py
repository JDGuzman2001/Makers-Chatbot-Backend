from openai import OpenAI
from fastapi import FastAPI, Request, Form
import json

client = OpenAI(
    api_key="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"
)


app = FastAPI()


with open("inventory.json", "r") as f:
    inventory = json.load(f)

@app.get("/inventory")
async def get_inventory():
    return inventory


@app.post("/inventory/add")
async def add_item(brand: str = Form(...), price: int = Form(...), quantity: int = Form(...)):
    new_item = {
        "brand": brand,
        "price": price,
        "quantity": quantity
    }
    inventory.append(new_item)

    with open("inventory.json", "w") as f:
        json.dump(inventory, f)

    return {"message": "Item added successfully", "item": new_item}


@app.delete("/inventory/delete")
async def delete_item(brand: str = Form(...)):
    global inventory
    inventory = [item for item in inventory if item["brand"] != brand]

    with open("inventory.json", "w") as f:
        json.dump(inventory, f)

    return {"message": "Item deleted successfully"}



@app.post("/chatbot")
async def get_response(request: Request):
    pregunta = await request.form()
    pregunta_texto = pregunta.get("pregunta")
    print(pregunta_texto)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or any other suitable model
        messages=[
            # {"role": "system", "content": f"You are a helpful assistant. Provide the response in JSON format with the key: 'data', no line breaks, do not continue with the response. Use the inventary delimited by triple quotes. Inventory:```{inventory}```"},
            {"role": "system",
             "content": f"You are a useful assistant. Provide the answer in JSON format with the key: 'data', without line breaks, do not continue with the answer. Be very specific with what they ask you, if they ask about `Brand` you return the brand, if they ask `Price` you return only the price, and if they ask for `Quantity` you return only the quantity. Use the inventory delimited by triple quotes Inventory:```{inventory}`` `"},
            {"role": "user", "content": pregunta_texto}
        ],
        temperature=0,
        max_tokens=150  # Adjust as needed
    )

    # answer = response.choices[0].text.strip()  # Get the text content
    answer_json = response.choices[0].message.content  # Access the JSON content
    answer_dict = json.loads(answer_json)  # Convert it to a dictionary
    # extracted_answer = answer_dict["data"]  # Extract the "answer" key

    print(answer_dict)
    return answer_dict



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
