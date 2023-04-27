import json

from flask import Flask, request
from typing import List

from dataModel import DataModel
from shippingCost import ShippingCost

app = Flask(__name__)

dataModel = DataModel()

@app.route('/', methods=['POST'])
def carbonCost():
    print(request.data)
    if not request.data:
        return "bad request", 400

    data = json.loads(request.data.decode("utf-8"))

    if 'materials' not in data or 'weight' not in data or 'delivery' not in data:
        return "bad request", 400

    materials : List[str] = data['materials']
    weight = data['weight'] # {amount, measurement}
    delivery = data['delivery'] # {zipCode}
    holder = dataModel.main(materials, weight, delivery)
    holder['shippingCost'] = ShippingCost(delivery['zipCode'], 1).CO2OffsetPrice

    return json.JSONEncoder().encode(holder)


@ app.route('/bulk', methods=['POST'])
def carbonBulkCost():
    if not request.data:
        return "bad request", 400

    data = json.loads(request.data.decode("utf-8"))

    for item in data['items']:
        if 'materials' not in item or 'weight' not in item:
            return "bad request", 400

    if 'delivery' not in data:
        return "bad request", 400

    holder = dataModel.mainBulk(data['items'], data['delivery'])
    holder['shippingCost'] = ShippingCost(data['delivery']['zipCode'], len(data['items'])).CO2OffsetPrice

    return holder


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
