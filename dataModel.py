import pandas as pd
import math
'''
TODO:
 goal 1: given a list of materials get the ammount of carbon for each, assume all kg and all materials = weight/len(materials) DONE
 goal 2: calculate monetary value of carbon output DONE -> double check -> DONE
 goal 3: convert units DONE
 goal 4: merge carbon outputs of delivery + materials
 goal 5: calculate confidence interval
 goal 5: make a REST API
 goal 6: account for edge cases (materials not in database, materials with multiple factors, etc.), more complicated/nuanced calculations

 Conversions:
  step 1: (Amazon mass unit) -> kg
  step 2 (optional): (kg) -> listed dataset unit
  step 3: (listed unit) -> kg carbon

  For step 2: (_kg -> _listed unit)
        example: 1kg -> 2.7 kwh
'''

# https://carbonfund.org/calculation-methods/#:~:text=We%20calculate%20emissions%20from%20electricity,0.371%20kgs%20CO2e%20per%20kWh).
kgPerLb = 0.45359237  # pounds
kgPerkWh = 0.371  # kilowatt hours
kgPerL = 0.85  # liters
kgPerTon = 907.185  # tons
kgPerTonne = 1000  # tonnes
kgPerM3 = 1000  # meters cubed
kgPerG = 0.001  # grams
kgPerOz = 0.0283495  # ounces

kWhperKg = 2.69542  # kilowatt hours
LperKg = 1.47  # liters
tonnePerKg = 0.001
m3PerKg = 0.001  # meters cubed
gPerKg = 1000  # grams
ozPerKg = 35.274  # ounces

# kg of carbon emissions per 1 mile by Amazon Car :  https://www.cars-data.com/en/mercedes-benz-sprinter/co2-emissions
CO2kgPerMileDriven = .32888
# $ to offset 1kg : https://www.mercycorps.org/blog/how-much-offset-your-carbon
pricePerCO2kg = .02

rawData_df = pd.read_csv("data/WinnipegData.csv",
                         usecols=['Category 3',
                                  'Title',
                                  'Unit',
                                  'Emission Factor',
                                  'Uncertainty'])


class DataModel:
    def convertToKg(self, measurement, amount):
        measurement = measurement.lower()
        match measurement:
            case 'lb':
                amount = amount * kgPerLb
            case 'lbs':
                amount = amount * kgPerLb
            case 'pound':
                amount = amount * kgPerLb
            case 'pounds':
                amount = amount * kgPerLb
            case 'kwh':
                amount = amount * kgPerkWh
            case 'l':
                amount = amount * kgPerL
            case 'liter':
                amount = amount * kgPerL
            case 'liters':
                amount = amount * kgPerL
            case 'litre':
                amount = amount * kgPerL
            case 'litres':
                amount = amount * kgPerL
            case 'tonne':
                amount = amount * kgPerTonne
            case 'ton':
                amount = amount * kgPerTon
            case 'm3':
                amount = amount * kgPerM3
            case 'g':
                amount = amount * kgPerG
            case 'gram':
                amount = amount * kgPerG
            case 'oz':
                amount = amount * kgPerOz
            case 'ounces':
                amount = amount * kgPerOz
            case 'kg':
                pass
            case _:
                print("Unaccounted for measurement", measurement)
        return amount

    def getLowestFactors(self, materials):
        materialEmissionFactors = {}

        # Get the lowest factor for each material
        for material in materials:
            material = material.lower()
            materialFactor = math.inf
            for _, row in rawData_df.iterrows():
                if material in row['Category 3'].lower() \
                        or material in row['Title'].lower():
                    # Convert measurements to kg
                    row['Emission Factor'] = self.convertToKg(
                        row['Unit'], row['Emission Factor'])

                    # Replace emisssion factor if it is lower
                    if float(row['Emission Factor']) <= materialFactor:
                        materialFactor = float(row['Emission Factor'])
                        materialEmissionFactors[material] = materialFactor

        # If the item is not found, tack the lowest emission factor to it
        for material in materials:
            if material not in materialEmissionFactors:
                if len(materialEmissionFactors) > 0:
                    materialEmissionFactors[material] = (
                        sum(materialEmissionFactors.values())
                        / len(materialEmissionFactors))
                else:
                    print(f'{material} not found.')
                    commonEmmissionFactor = 1.2  # random number
                    materialEmissionFactors[material] = commonEmmissionFactor

        return materialEmissionFactors

    def getTotalCarbonOutput(self, materials, weight):
        if len(materials) == 0:
            return 0
        totalCarbonOutput = 0

        weight = self.convertToKg(weight['measurment'], weight['amount'])
        proportion = weight/len(materials)
        lowestFactors = self.getLowestFactors(materials)

        for material in lowestFactors:
            totalCarbonOutput += float(lowestFactors[material]) * proportion
        return totalCarbonOutput  # in kg

    def getCarbonOffsetPrice(self, materials, weight, delivery):
        carbonOutput = self.getTotalCarbonOutput(
            materials, weight) * pricePerCO2kg
        return carbonOutput
        # TODO: (distance, method) = delivery

    def main(self, materials, weight, delivery):
        # input = {materials: [wood, aluminum, plastic], weight : ('kg', 15)
        # TODO: delivery: (distance, method)}

        return {
            "offsetCost":
                f'${self.getCarbonOffsetPrice(materials, weight, delivery):.2f}'
        }

    def mainBulk(self, items, delivery):
        offsetCosts = [self.main(item['materials'],
                                 item['weight'], delivery) for item in items]
        totalCost = 0
        for cost in offsetCosts:
            totalCost += float(cost['offsetCost'][1:])

        return {"offsetCost": f'${totalCost:.2f}'}


if __name__ == '__main__':
    dataModel = DataModel()
    print(
        dataModel.main([
            ['Biodiesel (kWh)', 'Fuel oil (liter)', 'Tap water',
             'Chloroacetic acid, C2H3ClO2'],
            ('pounds', 100), (100, 'car')
        ]))
