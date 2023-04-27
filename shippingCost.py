from enum import Enum
import numpy as np
import pandas as pd
from bisect import bisect_left

class LivingArea(Enum):
    ''' area : avg miles per stop '''
    rural = 4  # TODO: define more encompassing nums
    suburban = 2
    urban = 1

    def __str__(self):
        return f'For a(n) {self.name} community, Amazon drives an average of {self.value} mile(s) per stop.'


# kg of carbon emissions per 1 mile by Amazon Car :  https://www.cars-data.com/en/mercedes-benz-sprinter/co2-emissions
CO2kgPerMileDriven = .32888
# $ to offset 1kg : https://www.mercycorps.org/blog/how-much-offset-your-carbon
pricePerCO2kg = .02

popData = pd.read_csv("data/popData.csv", usecols=['ZipCode', 'Population', 'LivingArea'], converters={'ZipCode': str})
def determineLivingAreas():
    '''
        BE CAREFUL: Modifies the actual dataset.
    '''
    livingArea = []
    count = 0
    for row in popData.iterrows():
        if popData['Population'][row[0]] > 5000:
            livingArea.append('urban')
        elif popData['Population'][row[0]] < 2500:
            livingArea.append('rural')
        else:
            livingArea.append('suburban')
        if count%1000 == 0:
            print(count)
        count += 1
    popData['LivingArea'] = livingArea
    popData.to_csv('./data/popData.csv', index=False)

class ShippingCost:
    def __init__(self, zipCode, numProducts):
        self.livingArea = LivingArea[self.getLivingArea(zipCode)]
        self.CO2OffsetPrice = self.predictCO2OffsetPrice(self.livingArea, numProducts)

    def predictCO2OffsetPrice(self, livingArea: Enum, numProducts: int):
        return pricePerCO2kg*CO2kgPerMileDriven*livingArea.value*numProducts

    def getLivingArea(self, zipCode):
        index = bisect_left(popData['ZipCode'], zipCode)
        return popData['LivingArea'][index]

if __name__ == '__main__':
    shippingCost = ShippingCost('99820', 2)
    print(shippingCost.CO2OffsetPrice)
