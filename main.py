from extractor import *

material_info = None
production = None
preferred_sequence = None

def main():

    production, material_info = generate_material_and_jobs()
    preferred_sequence = generate_cleaning_times()
    
    print(material_info)
    print(production.head())
    print(preferred_sequence)

if __name__ == "__main__":
    main()