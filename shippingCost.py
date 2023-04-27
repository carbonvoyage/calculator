from enum import Enum


class LivingArea(Enum):
    ''' area : avg miles per stop '''
    rural = 4  # TODO: define more encompassing nums
    suburban = 2
    urban = 1

    def __str__(self):
        return f'For a(n) {self.name} community, Amazon drives an average \
            of {self.value} mile(s) per stop.'


# kg of carbon emissions per 1 mile by Amazon Car :  https://www.cars-data.com/en/mercedes-benz-sprinter/co2-emissions
CO2kgPerMileDriven = .32888
# $ to offset 1kg : https://www.mercycorps.org/blog/how-much-offset-your-carbon
pricePerCO2kg = .02


def predictCO2OffsetPrice(livingArea: Enum, numProducts: int):
    return pricePerCO2kg*CO2kgPerMileDriven*livingArea.value*numProducts


if __name__ == '__main__':
    print(predictCO2OffsetPrice(LivingArea.urban, 2))
