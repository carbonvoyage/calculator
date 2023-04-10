import sys
import json
from dataModel import DataModel
from flask import Flask
from flask import request
app = Flask(__name__)
# b'{\r\n    "input": ["materials": ["Biodiesel (kWh)", "Fuel oil (liter)", "Tap water", "Chloroacetic acid, C2H3ClO2"], "weight": ["ounces",100], [100, "car"]]\r\n}'
# {'input': [['Biodiesel (kWh)', 'Fuel oil (liter)', 'Tap water', 'Chloroacetic acid, C2H3ClO2'], ['ounces', 100], [100, 'car']]}
# {'input': [['Biodiesel (kWh)', 'Fuel oil (liter)', 'Tap water', 'Chloroacetic acid, C2H3ClO2'], ['ounces', 100], [100, 'car']]}
@app.route('/', methods = ['POST'])
def carbonCost():
    
    print(json.loads(request.data.decode("utf-8") ))
    data = json.loads(request.data.decode("utf-8") )
    print(data['input'])
    # [['Biodiesel (kWh)', 'Fuel oil (liter)', 'Tap water', 'Chloroacetic acid, C2H3ClO2'], ['ounces', 100], [100, 'car']]
    dataModel = DataModel()
    holder = dataModel.main(data['input'])
    return holder
    # return 'Hello, World!'

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
