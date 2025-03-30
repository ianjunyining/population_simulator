import random, Util, numpy as np, enum, parameters as params

class Gender(enum.Enum):
    Boy = 1
    Girl = 2

class Person(): 
    def __init__(self, gender:Gender=None, privilege=None, health=None, age=None):
        self.gender = gender if gender else Gender.Boy if random.random() > 0.5 else Gender.Girl
        self.privilege = privilege if privilege else Util.RandFloat(0, 100)
        self.age = age if age else Util.RandFloat(0, 36500)# in days
        self.health = health if health else params.health_k_age * self.age + params.health_b_age # 0-100
        self.live = True

    def update(self): 
        self.age += 1
        self.health += Util.RandFloat(
            params.health_k_low * self.age + params.health_b_low, 
            params.health_k_up * self.age + params.health_b_up,
        )
        self.health = Util.Constrain(self.health, [0, 100])
        if self.health <= 0 or random.random() < params.sudden_death_rate: 
            self.live = False
        self.privilege += Util.RandFloat(-0.1, 0.1)

    def __str__(self):
        return f"gender: {self.gender}, age: {self.age / 365}, health: {self.health}"

class Family():
    def __init__(self, husband, wife, max_num_of_children):
        self.husband = husband
        self.wife = wife
        self.max_num_of_children = max_num_of_children
        self.children = []

    def give_birth(self):
        if len(self.children) >= self.max_num_of_children:
            return
        if self.children[-1].age < params.min_gap_bet_children:
            return
        if self.children[-1].age >= params.max_children_gap:
            return
        if self.wife.age > params.max_age_give_birth:
            return
        if self.wife.health < params.min_health_give_birth_wife and \
            self.husband.health < params.min_health_give_birth_husband:
            return
        if random.random() > params.birth_chance:
            return

        return self.children.append(Person(age=0))

class Population():
    def __init__(self, inital_population_amount):
        self.families = []
        self.people = []
        self.inital_population(inital_population_amount)

    def inital_population(self, amount):
        for i in range(amount):
            self.people.append(Person())

    def number_of_people(self):
        people_count = 0
        for person in self.people:
            if person.live:
                people_count += 1
        return people_count
    
    def update(self):
        for person in self.people:
            if person.live:
                person.update()

    def number_of_males(self):
        males = 0
        for person in self.people:
            if person.gender == Gender.Boy and person.live:
                males += 1
        return males
    
    def number_of_females(self):
        return self.number_of_people() - self.number_of_males()




