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
lbPerKg = 0.45359237
kWhperKg = 2.69542
LperKg = 1.47  # liters
tonnePerKg = 0.001
m3PerKg = 0.001  # meters cubed

# kg of carbon emissions per 1 mile by Amazon Car :  https://www.cars-data.com/en/mercedes-benz-sprinter/co2-emissions
CO2kgPerMileDriven = .32888
# $ to offset 1kg : https://www.mercycorps.org/blog/how-much-offset-your-carbon
pricePerCO2kg = .02

rawData_df = pd.read_csv("WinnipegData.csv", usecols=['Category 3',
                                                      'Title',
                                                      'Unit',
                                                      'Emission Factor',
                                                      'Uncertainty'])


def getLowestFactors(materials):
    materialEmissionFactors = {}

    # Get the lowest factor for each material
    for material in materials:
        material = material.lower()
        materialFactor = math.inf
        for index, row in rawData_df.iterrows():
            if material in row['Category 3'].lower() or material in row['Title'].lower():
                # Convert units to kg
                match row['Unit']:
                    case 'lb':
                        row['Emission Factor'] = row['Emission Factor'] * lbPerKg
                    case 'kwh':
                        row['Emission Factor'] = row['Emission Factor'] * kWhperKg
                    case 'L':
                        row['Emission Factor'] = row['Emission Factor'] * LperKg
                    case 'tonne':
                        row['Emission Factor'] = row['Emission Factor'] * tonnePerKg
                    case 'ton':
                        row['Emission Factor'] = row['Emission Factor'] * tonnePerKg
                    case 'm3':
                        row['Emission Factor'] = row['Emission Factor'] * m3PerKg

                # Replace emisssion factor if it is lower
                if float(row['Emission Factor']) < materialFactor:
                    materialFactor = row['Emission Factor']
        materialEmissionFactors[material] = materialFactor

    # If the item is not found, tack the lowest emission factor to it
    for item in materialEmissionFactors:
        if materialEmissionFactors[item] == math.inf:
            materialEmissionFactors[item] = min(
                materialEmissionFactors.values())

    return materialEmissionFactors


def getTotalCarbonOutput(materials, weight):
    totalCarbonOutput = 0
    proportion = weight/len(materials)
    lowestFactors = getLowestFactors(materials)

    for material in lowestFactors:
        totalCarbonOutput += float(lowestFactors[material]) * proportion
    return totalCarbonOutput  # in kg


def getCarbonOffsetPrice(materials, weight, delivery):
    carbonOutput = getTotalCarbonOutput(materials, weight) * pricePerCO2kg
    return carbonOutput
    # (distance, method) = delivery


def main(input):
    # input = {materials: [wood, aluminum, plastic], weight : 15kg, TODO: delivery: (distance, method)}

    return f'${getCarbonOffsetPrice(input[0], input[1], input[2]):.2f}'


if __name__ == '__main__':
    print(
        main([['Biodiesel (kWh)', 'Fuel oil (liter)', 'Tap water', 'Chloroacetic acid, C2H3ClO2'], 100, (100, 'car')]))
    print(rawData_df)
