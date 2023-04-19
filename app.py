# TODO: flask routing
import sys
import json
from dataModel import DataModel
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def carbonCost():
    data = json.loads(request.data.decode("utf-8"))
    print(data['input'])
    # [['Biodiesel (kWh)', 'Fuel oil (liter)', 'Tap water', 'Chloroacetic acid, C2H3ClO2'], ['ounces', 100], [100, 'car']]
    dataModel = DataModel()
    holder = dataModel.main(data['input'])
    return holder


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
