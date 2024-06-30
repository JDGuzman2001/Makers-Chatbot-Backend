# [{"brand": "Dell", "quantity": 50, "price": 800}, {"brand": "HP", "quantity": 40, "price": 750}, {"brand": "Lenovo", "quantity": 30, "price": 700}]
import uuid
import json

# JSON original
data = [
    {"brand": "Dell", "quantity": 50, "price": 800},
    {"brand": "HP", "quantity": 40, "price": 750},
    {"brand": "Lenovo", "quantity": 30, "price": 700}
]

# Función para agregar IDs
def add_uuid(json_data):
    for item in json_data:
        item['id'] = str(uuid.uuid4())
    return json_data

# Agregar IDs
data_with_uuid = add_uuid(data)

# Convertir a JSON
json_with_uuid = json.dumps(data_with_uuid, indent=2)


