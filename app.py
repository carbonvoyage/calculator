import json
from dataModel import DataModel
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def carbonCost():
    data = json.loads(request.data.decode("utf-8"))
    dataModel = DataModel()
    holder = dataModel.main(data['input'])

    return holder


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
