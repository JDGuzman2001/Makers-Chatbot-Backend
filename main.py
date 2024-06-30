from openai import OpenAI
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
import json

client = OpenAI(
    api_key="sk-proj-o7Oba9cOUJYCoJybKBt3T3BlbkFJjdaEwl5WQIH5gNe6FnKK"
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)



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
    print(pregunta)
    pregunta_texto = pregunta.get("pregunta")
    print(pregunta_texto)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or any other suitable model
        messages=[
            # {"role": "system", "content": f"You are a helpful assistant. Provide the response in JSON format with the key: 'data', no line breaks, do not continue with the response. Use the inventary delimited by triple quotes. Inventory:```{inventory}```"},
            {"role": "system",
             "content": f"You are a useful assistant. Provide the answer in string format, structure your response so that it seems like a natural conversation., without line breaks, do not continue with the answer. Use the inventory delimited by triple quotes Inventory:```{inventory}`` `"},
            {"role": "user", "content": pregunta_texto}
        ],
        temperature=0,
        max_tokens=150  # Adjust as needed
    )

    # answer = response.choices[0].text.strip()  # Get the text content
    answer_json = response.choices[0].message.content  # Access the JSON content
    # answer_dict = json.loads(answer_json)  # Convert it to a dictionary
    # # extracted_answer = answer_dict["data"]  # Extract the "answer" key
    #
    # print(answer_dict)
    # return answer_dict
    return answer_json
    print(answer_json)





if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
