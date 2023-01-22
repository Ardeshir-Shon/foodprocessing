from extractor import *
import random

# TODO: make line an object and have number of lines and variables dynamic
# TODO: make the changeover time dynamic
# TODO: reduce the computation complexity of the simulation

material_info = None
production = None

numberOfWeeksAhead = 2
numberOfHoursAhead = 24*7*numberOfWeeksAhead

changeOverToSameProductP1 = 3
changeOverToSameProductP2 = 3
changeOverToSameProductP3 = 3

one_week_in_minutes = 24*7*60
two_weeks_in_minutes = 24*60*14

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

def update_line_status(preferred_sequence ,line_sequence, line_order_pointer, line_current_status, line_current_order, line_operation_remaining_time , material_info):
    if line_order_pointer == len(line_sequence):
        return "idle", None, line_order_pointer, 0
    else:
        if line_current_status == "idle":
            line_order_pointer += 1
            line_current_order = line_sequence[line_order_pointer]
            line_current_status = "production"
            line_operation_remaining_time = material_info[line_current_order]
            return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time
        elif line_current_status == "production":
            line_operation_remaining_time -= 1
            if line_operation_remaining_time == 0:
                line_current_status = "changeover"
                line_operation_remaining_time = get_changeovertime(preferred_sequence, line_current_order, line_sequence[line_order_pointer+1])
                return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time
            else:
                return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time
        elif line_current_status == "changeover":
            line_operation_remaining_time -= 1
            if line_operation_remaining_time == 0:
                line_current_status = "idle"
            return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time

def simulate_production(production_filtered, material_info, preferred_sequence, porposed_sequence):
    total_changeover_time, unmet_binary_map , week_one_idle_minutes, week_two_idle_minutes = 0,[0]*len(porposed_sequence),0,0

    offset_time = min(production_filtered.starthour)
    
    production_filtered.set_index('Order', inplace=True)

    line_one_sequence = []
    line_two_sequence = []
    
    line_one_order_pointer = -1
    line_two_order_pointer = -1

    line_one_current_order = None
    line_two_current_order = None

    line_one_current_status = "idle"
    line_two_current_status = "idle" # idle, production , changeover

    line_one_operation_remaining_time = 0
    line_two_operation_remaining_time = 0
    
    for order in porposed_sequence:
        if production_filtered.iloc[order]['machine_number'] ==  'P10':
            line_one_sequence.append(order)
        elif production_filtered.iloc[order]['machine_number'] ==  'P20':
            line_two_sequence.append(order)

    
    
    for time in range(two_weeks_in_minutes):
        # is that day shift or night shift?
        # night shift : 15:40 - 00:45
        # day shift : 7:40 - 15:00
        if time % (24*60) <= 45 or (time % (24*60) >= 940  and time % (24*60) <= 1440):
            shift = 'night'
        elif time % (24*60) >= 460 and time % (24*60) <= 900:
            shift = 'day'
        
        # update the status of each line
        pre_one_status = line_one_current_status
        pre_two_status = line_two_current_status
        if shift == 'day':
                line_one_current_status, line_one_current_order, line_one_order_pointer , line_one_operation_remaining_time = update_line_status(preferred_sequence , line_one_sequence, line_one_order_pointer, line_one_current_status, line_one_current_order, line_one_operation_remaining_time , material_info)
                line_two_current_status, line_two_current_order, line_two_order_pointer , line_two_operation_remaining_time = update_line_status(preferred_sequence , line_two_sequence, line_two_order_pointer, line_two_current_status, line_two_current_order, line_two_operation_remaining_time , material_info)
        
        if shift == 'night':
                if porposed_sequence.index(line_one_current_order) > porposed_sequence.index(line_two_current_order):
                    line_two_current_status, line_two_current_order, line_two_order_pointer , line_two_operation_remaining_time = update_line_status(preferred_sequence , line_two_sequence, line_two_order_pointer, line_two_current_status, line_two_current_order, line_two_operation_remaining_time , material_info)
                else:
                    line_one_current_status, line_one_current_order, line_one_order_pointer , line_one_operation_remaining_time = update_line_status(preferred_sequence , line_one_sequence, line_one_order_pointer, line_one_current_status, line_one_current_order, line_one_operation_remaining_time , material_info)
        
        # update changeover time and unmet_binary_map and week_one_idle_hours and week_two_idle_hours variables
        if pre_one_status == "production" and line_one_current_status == "changeover":
            if production_filtered.iloc[line_one_current_order]['endhour'] - offset_time >= time: # order met
                unmet_binary_map[porposed_sequence.index(line_one_current_order)] = 1
        if pre_two_status == "production" and line_two_current_status == "changeover":
            if production_filtered.iloc[line_two_current_order]['endhour'] - offset_time >= time: # order met
                unmet_binary_map[porposed_sequence.index(line_two_current_order)] = 1
        
        if pre_one_status == "changeover" and line_one_current_status == "changeover":
            total_changeover_time += 1
        if pre_two_status == "changeover" and line_two_current_status == "changeover":
            total_changeover_time += 1
        
        if line_one_current_status == "idle":
            if time < one_week_in_minutes:
                week_one_idle_minutes += 1
            else:
                week_two_idle_minutes += 1
        if line_two_current_status == "idle":
            if time < one_week_in_minutes:
                week_one_idle_minutes += 1
            else:
                week_two_idle_minutes += 1

    return total_changeover_time, unmet_binary_map , week_one_idle_minutes, week_two_idle_minutes


def main():

    production, material_info = generate_material_and_jobs()
    preferred_sequence = generate_cleaning_times()
    print(material_info)
    print(production[['Order', 'Material Number', 'machine_number','start_date', 'year' ,'starthour','endhour']])
    print(production.columns)
    
    print(get_changeovertime(preferred_sequence,4008134,3006507))
    print(get_changeovertime(preferred_sequence,3004436,3006465))
    print(get_changeovertime(preferred_sequence,4103894,3006465))

    

if __name__ == "__main__":
    main()