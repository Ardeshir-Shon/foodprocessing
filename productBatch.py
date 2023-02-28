class ProductBatch:
    material_number = None
    machine_number = None
    number_of_products = None
    products_per_week = {0:0,1:0,2:0}
    products_finished_per_week = {0:0,1:0,2:0}
    products_finished = 0
    material_production_time = None
    self_cleaning_time = None
    after_cleaning_time = None
    before_cleaning_time = None
    priority_score = None
    order_numbers = []

    def __init__(self, material_number, machine_number, number_of_products, self_cleaning_time, priority_score,material_production_time):
        self.material_number = material_number
        self.machine_number = machine_number
        self.number_of_products = number_of_products
        self.self_cleaning_time = self_cleaning_time
        self.priority_score = priority_score
        self.material_production_time = material_production_time

    def __str__(self):
        return "Material: " + str(self.material_number) + " Machine: " + str(self.machine_number) + " Number of products: " + str(self.number_of_products) + " Self cleaning time: " + str(self.self_cleaning_time) + " After cleaning time: " + str(self.after_cleaning_time) + " Before cleaning time: " + str(self.before_cleaning_time)
    
    # override sorting based on priority score
    def __lt__(self, other):
        return self.priority_score < other.priority_score
    def __eq__(self, other):
        return self.priority_score == other.priority_score
    def __gt__(self, other):
        return self.priority_score > other.priority_score
    
    def get_material_number(self):
        return self.material_number
    
    def get_machine_number(self):
        return self.machine_number
    
    def get_number_of_products(self):
        return self.number_of_products
    
    def get_self_cleaning_time(self):
        return self.self_cleaning_time
    
    def get_after_cleaning_time(self):
        return self.after_cleaning_time
    
    def get_before_cleaning_time(self):
        return self.before_cleaning_time
    
    def get_priority_score(self):
        return self.priority_score
    
    def get_products_finished(self):
        return self.products_finished
    
    def set_number_of_products(self,qty):
        self.number_of_products = qty
    
    def add_product(self,week):
        self.number_of_products += 1
        self.products_per_week[week] += 1
    
    def product_finished(self,week):
        self.products_finished += 1
        self.products_finished_per_week[week] += 1
    
    def set_before_cleaning_time(self,time):
        self.before_cleaning_time = time
    
    def set_after_cleaning_time(self,time):
        self.after_cleaning_time = time