class Order:
    
    def __init__(self,order_number,material_number,production_line,due_week,production_time,priority_score) -> None:
        self.material_number = material_number
        self.production_line = production_line
        self.due_week = due_week
        self.production_time = production_time
        self.order_number = order_number
        self.priority_score = priority_score
        self.is_finished = False
    
    def __str__(self) -> str:
        return "Order: " + str(self.order_number) + " Material: " + str(self.material_number) + " Production line: " + str(self.production_line) + " Due week: " + str(self.due_week) + " Production time: " + str(self.production_time) + " Priority score: " + str(self.priority_score) + " Is finished: " + str(self.is_finished)
    
    def __eq__(self, other):
        return self.material_number == other.material_number
    
    def get_material_number(self):
        return self.material_number
    
    def get_production_line(self):
        return self.production_line
    
    def get_due_week(self):
        return self.due_week
    
    def get_production_time(self):
        return self.production_time
    
    def get_order_number(self):
        return self.order_number
    
    def get_is_finished(self):
        return self.is_finished
    
    def get_priority_score(self):
        return self.priority_score
    
    def set_is_finished(self,finished):
        self.is_finished = finished
