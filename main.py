from extractor import *
import random

material_info = None
production = None

numberOfWeeksAhead = 2
numberOfHoursAhead = 24*7*numberOfWeeksAhead

changeOverToSameProductP1 = 3
changeOverToSameProductP2 = 3
changeOverToSameProductP3 = 3

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
# night shift : 15:40 - 12:45
# day shift : 7:40 - 15:00
def main():

    production, material_info = generate_material_and_jobs()
    preferred_sequence = generate_cleaning_times()
    print(material_info)
    print(production[['Order', 'Material Number', 'machine_number','start_date', 'year' ,'starthour','endhour']])
    print(production.columns)
    
    print(get_changeovertime(preferred_sequence,4008134,3006507))
    print(get_changeovertime(preferred_sequence,3004436,3006465))
    print(get_changeovertime(preferred_sequence,4103894,3006465))

    isConverged = False
    # main simulation loop
    while not isConverged:


if __name__ == "__main__":
    main()