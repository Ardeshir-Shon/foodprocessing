import pandas as pd

def generate_material_and_jobs(file_production_name="Actual production.XLSX", 
        file_material_name="Routing Timings.XLSX"):
    
    # Read the production file
    production = pd.read_excel("data/"+file_production_name)
    # Filter the production file
    production = production[["Order","Material Number","MRP controller","Basic start date"]]

    # Read the material file
    material = pd.read_excel("data/"+file_material_name)
    # Filter the material file
    material = material[["Material", "Operation short text", "StdVal1","StdVal2"]]
    material = material[material["Operation short text"] == "Phase 5 Packing"]
    
    print(production.head())
    print(material.head())
    production_plan = {}
    # for index, row in production.iterrows():
    #     production_plan[row["Material"]] = row["Quantity"]
    material_info = {} 
    print(file_production_name, file_material_name)
    print("Extracted data from csv file")

    return production_plan, material_info