import pandas as pd
import math

# ([wood, aluminum, plastic], (weight in kg))

# TODO: 
# goal 1 -> given a list of materials get the ammount of carbon for each (assume all kg and all materials = weight) //DONE
# goal 2 -> calculate monetary value of carbon output //DONE -> double check
# goal 3 -> convert units
# goal 4 -> merge carbon outputs of delivery + materials
# goal 5 -> calculate confidence interval
# goal 5 -> make a REST API
# goal 6 -> account for edge cases (materials not in database, materials with multiple factors, etc.), more complicated/nuanced calculations

# Conversions:
# step 1: (Amazon mass unit) -> kg
# step 2 (optional): (kg) -> listed dataset unit
# step 3: (listed unit) -> kg carbon

# For step 2: (_kg -> _listed unit)
#          example: 1kg -> 2.7 kwh

# https://carbonfund.org/calculation-methods/#:~:text=We%20calculate%20emissions%20from%20electricity,0.371%20kgs%20CO2e%20per%20kWh).
# 1 lb = 0.45359237 kg
# 1 kg = 2.69542 kwh CO2
# 1 kg = 1 kg
# 1 kg = 1.47 L (liters)
# 1 kg = 0.001 tonne
# 1 kg = 0.001 m3

rawData_df = pd.read_csv("WinnipegData.csv", usecols= ['Category 3', 'Title', 'Unit', 'Emission Factor', 'Uncertainty'])

def getLowestFactor(materials):
    materialEmissionFactors = {}

    # Get the lowest factor for each material
    for material in materials:
        materialFactor = math.inf
        for index, row in rawData_df.iterrows():
            if material.lower() in row['Category 3'].lower() or material.lower() in row['Title'].lower():
                if float(row['Emission Factor']) < materialFactor:
                    materialFactor = row['Emission Factor']
        materialEmissionFactors[material] = materialFactor
    
    # If the item is not found, tack the lowest emission factor to it
    for item in materialEmissionFactors:
        if materialEmissionFactors[item] == math.inf:
            materialEmissionFactors[item] = min(materialEmissionFactors.values())

    return materialEmissionFactors
                
def getCarbonOutputs(materials, weight):
    totalCarbonOutput = 0
    proportion = weight/len(materials)
    lowestFactors = getLowestFactor(materials)

    for material in lowestFactors:
        totalCarbonOutput += float(lowestFactors[material]) * proportion
    return totalCarbonOutput

def getCarbonOffsetPrice(materials, weight):
    return getCarbonOutputs(materials, weight) * .01 

def main(input):
    #{[wood, aluminum, plastic], (weight in kg)}
    return getCarbonOffsetPrice(input[0], input[1])


print(main([['wood', 'aluminum', 'plastic'], 100]))
print(rawData_df)