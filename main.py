from extractor import *
import random

material_info = None
production = None
# preferred_sequence = {}

changeovers = {}


#auto cache
def get_changeovertime(preferred_sequence,m1,m2):
    try:
        return changeovers[m1][m2]
    except:
        dist = abs(int(preferred_sequence[m1])-int(preferred_sequence[m2]))
        generatedTime = int(5+(dist*random.randint(10,14)/130))+1
        changeovers[m1] = {m2:generatedTime}
        changeovers[m2] = {m1:generatedTime}
        
        return generatedTime

def main():

    production, material_info = generate_material_and_jobs()
    preferred_sequence = generate_cleaning_times()
    
    print(get_changeovertime(preferred_sequence,4008134,3006507))
    print(get_changeovertime(preferred_sequence,3004436,3006465))
    print(get_changeovertime(preferred_sequence,4103894,3006465))

    # print(material_info)
    # print(production.head())
    # print(preferred_sequence)

if __name__ == "__main__":
    main()