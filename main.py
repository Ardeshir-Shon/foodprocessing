from extractor import *
import random
import logging
import os

# TODO: make line an object and have number of lines and variables dynamic
# TODO: make the changeover time dynamic
# TODO: reduce the computation complexity of the simulation
# TODO: makke the nth week dynamic not related to the number of years

# if certain file exists, remove it
os.remove("log.txt") if os.path.exists("log.txt") else None
f = open("log.txt","a")

material_info = None
production = None

numberOfWeeksAhead = 2
numberOfHoursAhead = 24*7*numberOfWeeksAhead

# product to the same product changeover is a constant equal to 7 minutes
# line one and two setup times are 10 minutes and line three is 20 minutes
# setup time is from a product to the product prime

one_week_in_minutes = 24*7*60
two_weeks_in_minutes = 24*60*14

min_total_changeover_time, min_unmet_orders, min_idle_time = None, None, None
max_total_changeover_time, max_unmet_orders, max_idle_time = None, None, None

changeovers = {}

def get_product_production_line(product, production_filtered):
    if production_filtered[production_filtered["Material Number"]==product]['machine_number'] ==  'P10':
        return 1
    elif production_filtered[production_filtered["Material Number"]==product]['machine_number'] ==  'P20':
        return 2
    elif production_filtered[production_filtered["Material Number"]==product]['machine_number'] ==  'P30':
        return 3

#auto cache
def get_changeovertime(preferred_sequence,m1,m2):
    
    setup_time = 10
    if m1 == m2:
        return 7
    try:
        return changeovers[m1][m2] + setup_time
    except:
        try:
            dist = abs(int(preferred_sequence[m1])-int(preferred_sequence[m2]))
        except:
            dist = 10
        generatedTime = int(5+(dist*random.randint(10,14)/130))+1
        changeovers[m1] = {m2:generatedTime}
        changeovers[m2] = {m1:generatedTime}
        
        return setup_time + generatedTime

def update_line_status(preferred_sequence ,line_sequence, line_order_pointer, line_current_status, line_current_order, line_operation_remaining_time , material_info, production_filtered):
    if line_order_pointer == len(line_sequence):
        return "idle", None, line_order_pointer, 0
    else:
        if line_current_status == "idle":
            line_order_pointer += 1
            line_current_order = line_sequence[line_order_pointer]
            line_current_status = "production"
            line_operation_remaining_time = material_info[production_filtered.loc[line_current_order]["Material Number"]]
            # line_operation_remaining_time = material_info[line_current_order]
            return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time
        elif line_current_status == "production":
            line_operation_remaining_time -= 1
            if line_operation_remaining_time == 0:
                line_current_status = "changeover"
                next_order = line_sequence[line_order_pointer+1]
                line_operation_remaining_time = get_changeovertime(preferred_sequence, production_filtered.loc[line_current_order]["Material Number"], production_filtered.loc[next_order]["Material Number"])
                return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time
            else:
                return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time
        elif line_current_status == "changeover":
            line_operation_remaining_time -= 1
            if line_operation_remaining_time == 0:
                line_current_status = "idle"
            return line_current_status, line_current_order, line_order_pointer, line_operation_remaining_time

def simulate_production(production_filtered, material_info, preferred_sequence, porposed_sequence):
    total_changeover_time, unmet_binary_map , week_one_idle_minutes, week_two_idle_minutes = 0,[1]*len(porposed_sequence),0,0

    save_line_one_status = None
    save_line_two_status = None

    offset_time = min(production_filtered.starthour)

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
        if production_filtered.loc[order]['machine_number'] ==  'P10':
            line_one_sequence.append(order)
        elif production_filtered.loc[order]['machine_number'] ==  'P20':
            line_two_sequence.append(order)

    
    
    for time in range(two_weeks_in_minutes):
        # is that day shift or night shift?
        # night shift : 15:40 - 00:45
        # day shift : 7:40 - 15:00
        if time % (24*60) <= 45 or (time % (24*60) >= 940  and time % (24*60) <= 1440):
            shift = 'night'
        elif time % (24*60) >= 460 and time % (24*60) <= 900:
            shift = 'day'
        else:
            shift = 'off'
        
        # update the status of each line
        pre_one_status = line_one_current_status
        pre_two_status = line_two_current_status
        if shift == 'day':
                if line_one_current_status == "off":
                    line_one_current_status = save_line_one_status
                if line_two_current_status == "off":
                    line_two_current_status = save_line_two_status
                line_one_current_status, line_one_current_order, line_one_order_pointer , line_one_operation_remaining_time = update_line_status(preferred_sequence , line_one_sequence, line_one_order_pointer, line_one_current_status, line_one_current_order, line_one_operation_remaining_time , material_info, production_filtered)
                line_two_current_status, line_two_current_order, line_two_order_pointer , line_two_operation_remaining_time = update_line_status(preferred_sequence , line_two_sequence, line_two_order_pointer, line_two_current_status, line_two_current_order, line_two_operation_remaining_time , material_info, production_filtered)
        
        if shift == 'night': # fix idle time in night shift
                if line_one_current_status == "off":
                    line_one_current_status = save_line_one_status
                if line_two_current_status == "off":
                    line_two_current_status = save_line_two_status
                
                if line_one_current_order == None:
                    line_one_current_status, line_one_current_order, line_one_order_pointer , line_one_operation_remaining_time = update_line_status(preferred_sequence , line_one_sequence, line_one_order_pointer, line_one_current_status, line_one_current_order, line_one_operation_remaining_time , material_info, production_filtered)
                elif line_two_current_order == None or porposed_sequence.index(line_one_current_order) > porposed_sequence.index(line_two_current_order):
                    week_one_idle_minutes += 1
                    line_two_current_status, line_two_current_order, line_two_order_pointer , line_two_operation_remaining_time = update_line_status(preferred_sequence , line_two_sequence, line_two_order_pointer, line_two_current_status, line_two_current_order, line_two_operation_remaining_time , material_info, production_filtered)
                else:
                    week_two_idle_minutes += 1
                    line_one_current_status, line_one_current_order, line_one_order_pointer , line_one_operation_remaining_time = update_line_status(preferred_sequence , line_one_sequence, line_one_order_pointer, line_one_current_status, line_one_current_order, line_one_operation_remaining_time , material_info, production_filtered)
                # check may reach first if and last else
        if shift == 'off':
            if line_one_current_status != "off":
                save_line_one_status = line_one_current_status
                line_one_current_status = "off"
            if line_two_current_status != "off":
                save_line_two_status = line_two_current_status
                line_two_current_status = "off"
            line_one_current_status = 'off'
            line_two_current_status = 'off'

        # update changeover time and unmet_binary_map and week_one_idle_hours and week_two_idle_hours variables
        if pre_one_status == "production" and line_one_current_status == "changeover":
            if production_filtered.loc[line_one_current_order]['endhour'] - offset_time >= time: # order met
                unmet_binary_map[porposed_sequence.index(line_one_current_order)] = 0
        if pre_two_status == "production" and line_two_current_status == "changeover":
            if production_filtered.loc[line_two_current_order]['endhour'] - offset_time >= time: # order met
                unmet_binary_map[porposed_sequence.index(line_two_current_order)] = 0
        
        if pre_one_status == "changeover" and line_one_current_status == "changeover":
            total_changeover_time += 1
        if pre_two_status == "changeover" and line_two_current_status == "changeover":
            total_changeover_time += 1
        
        if line_one_current_status == "idle" or line_one_current_status == "off":
            if time < one_week_in_minutes:
                week_one_idle_minutes += 1
            else:
                week_two_idle_minutes += 1
        if line_two_current_status == "idle" or line_two_current_status == "off":
            if time < one_week_in_minutes:
                week_one_idle_minutes += 1
            else:
                week_two_idle_minutes += 1

    return total_changeover_time, unmet_binary_map , week_one_idle_minutes, week_two_idle_minutes

def calculate_fitness(production_filtered, material_info, preferred_sequence, porposed_sequence):
    global min_idle_time
    global min_total_changeover_time
    global min_unmet_orders
    global max_idle_time
    global max_total_changeover_time
    global max_unmet_orders
    
    global f

    f.writelines("Sequence: " + str(porposed_sequence)+"\n")

    total_changeover_time, unmet_binary_map , week_one_idle_minutes, week_two_idle_minutes = simulate_production(production_filtered, material_info, preferred_sequence, porposed_sequence)
    unmet_orders = sum(unmet_binary_map)
    # balance the fitness function between unmet orders and changeover time
    # find a metric to balance the weeks
    idle_time = week_one_idle_minutes + week_two_idle_minutes
    # TODO: normalize all three contributing criteria on fiteens before the summation
    if min_idle_time == None or min_total_changeover_time == None or min_unmet_orders == None or max_idle_time == None or max_total_changeover_time == None or max_unmet_orders == None:
            max_idle_time = idle_time
            max_total_changeover_time = total_changeover_time
            max_unmet_orders = unmet_orders
            min_total_changeover_time = total_changeover_time
            min_unmet_orders = unmet_orders
            min_idle_time = idle_time
            # fitness = total_changeover_time + unmet_orders + idle_time
            return 0
    # update min and max values in else
    else:
        if idle_time < min_idle_time:
            min_idle_time = idle_time
        if total_changeover_time < min_total_changeover_time:
            min_total_changeover_time = total_changeover_time
        if unmet_orders < min_unmet_orders:
            min_unmet_orders = unmet_orders
        if idle_time > max_idle_time:
            max_idle_time = idle_time
        if total_changeover_time > max_total_changeover_time:
            max_total_changeover_time = total_changeover_time
        if unmet_orders > max_unmet_orders:
            max_unmet_orders = unmet_orders
    
    try:
        fitness = (total_changeover_time - min_total_changeover_time)/(max_total_changeover_time - min_total_changeover_time) + (unmet_orders - min_unmet_orders)/(max_unmet_orders - min_unmet_orders)# + (idle_time - min_idle_time)/(max_idle_time - min_idle_time)
        fitness = 1/fitness
        # add a line to f to write the fitness value with detailed elements
        f.writelines(str(fitness) + ',' + str(total_changeover_time) + ',' + str(unmet_orders) + ',' + str(idle_time) + '\n')
        return fitness
    except:
        print("Error in calculate_fitness function")
        return 0

def generate_random_sequence(production_filtered):
    # generate a random sequence of orders for different lines then concat lists
    
    line_one_sequence = production_filtered[production_filtered['machine_number'] == 'P10'].index.tolist()
    line_two_sequence = production_filtered[production_filtered['machine_number'] == 'P20'].index.tolist()
    
    random.shuffle(line_one_sequence)
    random.shuffle(line_two_sequence)
    porposed_sequence = line_one_sequence + line_two_sequence
    return porposed_sequence

    # orders = production_filtered["Order"].tolist()
    # random.shuffle(orders)
    # return orders

def generate_random_population(production_filtered, population_size):
    population = []
    for i in range(population_size):
        porposed_sequence = generate_random_sequence(production_filtered)
        population.append(porposed_sequence)
    return population

def generate_next_generation(production_filtered, material_info, preferred_sequence, population, population_size, mutation_rate):
    print("Generating next generation...")
    fitness_map = {}
    for porposed_sequence in population:
        fitness_map[tuple(porposed_sequence)] = calculate_fitness(production_filtered, material_info, preferred_sequence, porposed_sequence)
    for k,v in fitness_map.items():
        print(len(k))
    sorted_fitness_map = sorted(fitness_map.items(), key=lambda x: x[1])
    sorted_population = [list(x[0]) for x in sorted_fitness_map]
    next_generation = sorted_population[:int(population_size*0.2)]
    for i in range(int(population_size*0.8)):
        parent1 = random.choice(sorted_population[:int(population_size*0.2)])
        parent2 = random.choice(sorted_population[:int(population_size*0.2)])
        child = crossover(parent1, parent2, production_filtered, material_info, preferred_sequence)
        if random.random() < mutation_rate:
            child = mutate(child)
        next_generation.append(child)
    return next_generation

def crossover(parent1, parent2, production_filtered, material_info, preferred_sequence):
    child = []
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    
    child = list(set(child)) # make it unique

    production_filtered_orders = production_filtered.index.values.tolist()#production_filtered["Order"].tolist()
    missing_elements = [element for element in production_filtered_orders if element not in child] 
    for element in missing_elements:
        child.append(element)
    total_changeover_time, unmet_binary_map , week_one_idle_minutes, week_two_idle_minutes = simulate_production(production_filtered, material_info, preferred_sequence, child)
    for i in range(len(unmet_binary_map)):
        if unmet_binary_map[i] == 1:
            item = child[i]
            child.pop(i)
            child.insert(int(i/2),item)
    return child



def mutate(child):
    index1 = random.randint(0, len(child)-1)
    index2 = random.randint(0, len(child)-1)
    child[index1], child[index2] = child[index2], child[index1]
    return child

def genetic_algorithm(production_filtered, material_info, preferred_sequence, population_size, mutation_rate, generations):
    f.writelines("Starting genetic algorithm with population size: " + str(population_size) + " mutation rate: " + str(mutation_rate) + " generations: " + str(generations)+"\n")

    population = generate_random_population(production_filtered, population_size)
    for i in range(generations):
        f.writelines("Generation: " + str(i) + "\n")
        population = generate_next_generation(production_filtered, material_info, preferred_sequence, population, population_size, mutation_rate)
    f.writelines("Finished genetic algorithm with population size: " + str(population_size) + " mutation rate: " + str(mutation_rate) + " generations: " + str(generations)+"\n")
    fitness_map = {}
    for porposed_sequence in population:
        f.writelines("\n*****************************\n"+str(porposed_sequence) + "\n")
        fitness_map[tuple(porposed_sequence)] = calculate_fitness(production_filtered, material_info, preferred_sequence, porposed_sequence)
        f.writelines("fitness: " + str(fitness_map[tuple(porposed_sequence)]) + "\n")
    sorted_fitness_map = sorted(fitness_map.items(), key=lambda x: x[1])
    sorted_population = [list(x[0]) for x in sorted_fitness_map]
    best_sequence = sorted_population[0]
    return best_sequence

def get_nth_two_weeks_production(production,n): # n starts from 0
    # error handling
    if n > len(production):
        return get_nth_two_weeks_production(production, n%len(production))
    
    firstYear = len(production[production['year']==2021])
    secondYear = len(production[production['year']==2022])
    offset_week = min(production[production['year']==2021].week)
    if n > firstYear:
        production_filtered = production[production['year']==2022]
        production_filtered = production_filtered[[(production_filtered['week']==n-firstYear+1) | (production_filtered['week']==n-firstYear+2)]]
        return production_filtered
    production_filtered = production[production['year']==2021]
    production_filtered = production_filtered[[(production_filtered['week']==offset_week+n) | (production_filtered['week']==offset_week+n+1)]]
    return production_filtered

def fill_the_pool(pool_size,production_filtered,material_info, preferred_sequence):
    global f

    for i in range(pool_size):
        f.writelines("Pool size: " + str(i+1)+"\n")
        temp_seq = generate_random_sequence(production_filtered)
        temp_fitness = calculate_fitness(production_filtered, material_info, preferred_sequence, temp_seq)
        f.writelines("min_unmet: " + str(min_unmet_orders) + " max_unmet: " + str(max_unmet_orders) + " min_idle: " + str(min_idle_time) + " max_idle: " + str(max_idle_time) + " min_changeover: " + str(min_total_changeover_time) + " max_changeover: " + str(max_total_changeover_time)+"\n")
def main():

    production, material_info = generate_material_and_jobs()
    # production_filtered = get_nth_two_weeks_production(production, 1)
    production_filtered = production[production["year"]==2021]
    production_filtered = production_filtered[(production_filtered["week"]==40) | (production_filtered["week"]==41)]
    production_filtered = production_filtered[production_filtered['machine_number'] != 'P30']
    production_filtered.set_index('Order', inplace=True)
    
    preferred_sequence = generate_cleaning_times()

    print("Production size:", len(production_filtered))
    pool_size = 100
    population_size = 100
    mutation_rate = 0.1
    generations = 100
    f.writelines("before fill the pool"+"\n")
    f.writelines("min_unmet: " + str(min_unmet_orders) + " max_unmet: " + str(max_unmet_orders) + " min_idle: " + str(min_idle_time) + " max_idle: " + str(max_idle_time) + " min_changeover: " + str(min_total_changeover_time) + " max_changeover: " + str(max_total_changeover_time))
    fill_the_pool(pool_size,production_filtered,material_info, preferred_sequence)
    f.writelines("after fill the pool"+"\n")
    f.writelines("min_unmet: " + str(min_unmet_orders) + " max_unmet: " + str(max_unmet_orders) + " min_idle: " + str(min_idle_time) + " max_idle: " + str(max_idle_time) + " min_changeover: " + str(min_total_changeover_time) + " max_changeover: " + str(max_total_changeover_time)+"\n")
    # print(production_filtered[production_filtered['Order']==3827828])
    best_sequence = genetic_algorithm(production_filtered, material_info, preferred_sequence, population_size, mutation_rate, generations)
    f.writelines("best sequence: " + str(best_sequence)+"\n")
    print(best_sequence)
    f.close()
    # print(material_info)
    # print(production_filtered[['Order', 'Material Number', 'machine_number','start_date', 'year', 'week' ,'starthour','endhour']].head(50))
    # print(production.columns)


if __name__ == "__main__":
    main()
