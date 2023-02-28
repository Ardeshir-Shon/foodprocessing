import pandas as pd
from functools import lru_cache

def generate_material_and_jobs(file_production_name="Actual production.XLSX", 
        file_material_name="Routing Timings.XLSX"):
    
    # Read the production file
    production = pd.read_excel("data/"+file_production_name)
    # Filter the production file
    production = production[["Order","Material Number","MRP controller","Basic start date"]]
    production.rename(columns={"Basic start date": "start_date"}, inplace=True)
    production.rename(columns={"MRP controller": "machine_number"}, inplace=True)

    # Read the material file
    material = pd.read_excel("data/"+file_material_name)
    # Filter the material file
    material = material[["Material", "Operation short text", "StdVal1","StdVal2"]]
    material = material[material["Operation short text"] == "Phase 5 Packing"]

    times = pd.to_datetime(production.start_date)
    
    production["year"] = times.dt.year
    production["week"] = times.dt.week
    production["day"] = times.dt.day
    production["dayofweek"] = times.dt.dayofweek
    production["dayofyear"] = times.dt.dayofyear
    production["starthour"] = (production.dayofyear-1) * 24 # start hour indexed in year
    production["end_date"] = times + pd.to_timedelta(6-times.dt.dayofweek, unit="d")
    production["end_dayofyear"] = pd.to_datetime(production.end_date).dt.dayofyear
    production["endhour"] = production.end_dayofyear * 24 # end hour indexed in year
    
    material_info = {} 

    for index, row in material.iterrows():
        material_info[row["Material"]] = max(row["StdVal1"],row["StdVal2"])
    
    # print(file_production_name, file_material_name)
    print("Extracted data from csv file ...")

    return production, material_info

def generate_cleaning_times(prefered_time="Their prefered sequence.xlsx"):
    cleaning_times = pd.read_excel("data/"+prefered_time)

    cleaning_times = cleaning_times[["Material"]]
    
    tempDict = cleaning_times.to_dict()

    out_cleaning_times = {v: k for k, v in tempDict['Material'].items()}

    return out_cleaning_times

@lru_cache(maxsize=None)
def get_cleaning_times(source,dest):
    try:
        cleaning_times = pd.read_excel("data/ModelData.xlsx",skiprows=2)
        cleaning_times = cleaning_times.drop(cleaning_times.columns[0], axis=1)
        cleaning_times.set_index("Material", inplace=True)
        return int(cleaning_times.loc[source,dest])
    except:
        return 40