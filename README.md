# Carbon Voyage:

## Features

-   See dataModel.py which is used to calculate the estimated carbon cost of producing a specific item. It takes in an array of materials used in the construction of the product and a weight.

-   See app.py for the calculations used for shipping your product as well as the callable api of the backend.

## Usage

`POST` to `/`:

```json
{
    "materials": [
        "Biodiesel (kWh)",
        "Fuel oil (liter)",
        "Tap water",
        "Chloroacetic acid, C2H3ClO2"
    ],
    "weight": {
        "amount": 1000,
        "measurment": "ounces"
    },
    "delivery": {
        "amount": 100,
        "measurment": "miles",
        "mode": "truck"
    }
}
```

Response:

```json
{
    "offsetCost": "$69.42"
}
```

`POST` to `/bulk`:

```json
{
    "items": [
        {
            "materials": [
                "Biodiesel (kWh)",
                "Fuel oil (liter)",
                "Tap water",
                "Chloroacetic acid, C2H3ClO2"
            ],
            "weight": {
                "amount": 1000,
                "measurment": "ounces"
            }
        },
        {
            "materials": ["Fuel oil (liter)", "Chloroacetic acid, C2H3ClO2"],
            "weight": {
                "amount": 500,
                "measurment": "ounces"
            }
        }
    ],
    "delivery": {
        "amount": 100,
        "measurment": "miles",
        "mode": "truck"
    }
}
```

Response:

```json
{
    "offsetCost": "$69.42"
}
```

## References

https://legacy.winnipeg.ca/finance/findata/matmgt/documents/2012/682-2012/682-2012_appendix_h-wstp_south_end_plant_process_selection_report/appendix%207.pdf
from: https://legacy.winnipeg.ca/matmgt/default.stm

```

```
