import random, Util, numpy as np, enum, parameters as params, math

class Gender(enum.Enum):
    Boy = 1
    Girl = 2

class Person(): 
    def __init__(self, gender:Gender=None, privilege=None, health=None, age=None):
        self.gender = gender if gender else Gender.Boy if random.random() > 0.5 else Gender.Girl
        self.privilege = privilege if privilege else Util.RandFloat(0, 100)
        self.age = age if age else int(Util.RandFloat(0, params.days_in_year * 100)) # in days
        self.health = health if health else params.health_k_age * self.age + params.health_b_age # 0-100
        self.live = True
        self.married = False

    def update(self, days:int): 
        self.age += days
        self.health += Util.RandFloat(
            params.health_k_low * self.age + params.health_b_low, 
            params.health_k_up * self.age + params.health_b_up,
        ) * days
        self.health = Util.Constrain(self.health, [0, 100])
        if self.health <= 0 or random.random() < params.sudden_death_rate: 
            self.live = False
        #self.privilege += sum(Util.RandFloat(-0.1, 0.1) for _ in range(days))

    def __str__(self):
        return f"gender: {self.gender}, age: {self.age / params.days_in_year}, health: {self.health}"

class Family():
    def __init__(self, husband:Person, wife:Person, max_num_of_children:int):
        self.husband = husband
        self.wife = wife
        self.husband.married = True
        self.wife.married = True
        self.max_num_of_children = max_num_of_children
        self.index = 0
        self.children = []

    def give_birth(self):
        if len(self.children) >= self.max_num_of_children:
            return
        if self.children and self.children[-1].age < params.min_gap_bet_children:
            return
        if self.children and self.children[-1].age >= params.max_children_gap:
            return
        if self.wife.age > params.max_age_give_birth:
            return
        if self.wife.health < params.min_health_give_birth_wife and \
            self.husband.health < params.min_health_give_birth_husband:
            return
        if random.random() > params.prob_children_per_window:
            return
        self.children.append(Person(age=1))
        return self.children[-1]

class Population():
    def __init__(self, inital_population_amount):
        self.families = []
        self.people = []
        self.inital_population(inital_population_amount)
        self.new_families_on_day = 0
        self.new_babies_on_day = 0
        self.cached_nums_children_family = []
        self.cache_index = 0

    def __str__(self):
        return f"population: {self.number_of_people()}, life span: {self.average_life_span():.2f}, family: {len(self.families)}, avg: {params.avg_num_children_family:.2f}"
    
    def inital_population(self, amount):
        for i in range(amount):
            self.people.append(Person())

    def adjust_avg_num_children_per_family(self):
        if not params.enable_negative_feedback: 
            return
        if self.number_of_people() > params.stable_population and \
            params.avg_num_children_family - params.avg_num_children_delta > params.avg_num_children_lb:
            params.avg_num_children_family -= params.avg_num_children_delta
        elif params.avg_num_children_family + params.avg_num_children_delta < params.avg_num_children_ub:
            params.avg_num_children_family += params.avg_num_children_delta

    def average_life_span(self) -> float:
        total_dead = 0
        total_age = 0
        for person in self.people:
            if person.live: continue
            total_dead += 1
            total_age += person.age
        return total_age / max(total_dead, 1) / params.days_in_year

    def number_of_people(self):
        people_count = 0
        for person in self.people:
            if person.live:
                people_count += 1
        return people_count
    
    def number_of_males(self):
        males = 0
        for person in self.people:
            if person.gender == Gender.Boy and person.live:
                males += 1
        return males
    
    def number_of_females(self):
        return self.number_of_people() - self.number_of_males()
    
    def number_of_married(self):
        married = 0
        for person in self.people:
            if person.married and person.live:
                married += 1
        return married
    
    def next_num_children_family(self):
        if not self.cached_nums_children_family or self.cache_index >= len(self.cached_nums_children_family):
            self.cached_nums_children_family = Util.generate_random_sequence(
                10,
                params.min_num_children_family,
                params.max_num_children_family,
                params.avg_num_children_family,
            )
            self.cache_index = 0
        ret = self.cached_nums_children_family[self.cache_index]
        self.cache_index += 1
        return ret
        
    def create_families(self):
        married = self.number_of_married()
        expected_married = params.marriage_rate * self.number_of_people()
        if married >= expected_married:
            return

        potential_marry_boys = []
        potential_marry_girls = []

        for person in self.people:
            if not person.live:
                continue
            if person.married or person.age < params.min_age_marry:
                continue
            if person.gender == Gender.Boy:
                potential_marry_boys.append(person)
            else:
                potential_marry_girls.append(person)

        potential_marry_boys.sort(key=lambda person: person.age)
        potential_marry_girls.sort(key=lambda person: person.age)
        self.new_families_on_day = min(
            len(potential_marry_boys), 
            len(potential_marry_girls), 
            math.floor((expected_married - married) / 2),
        )

        for i in range(self.new_families_on_day):
            family = Family(
                husband=potential_marry_boys[i],
                wife=potential_marry_girls[i],  
                max_num_of_children=self.next_num_children_family(),
            )
            family.index = len(self.families)
            self.families.append(family)
        
    def update(self):
        for person in self.people:
            if person.live:
                person.update(params.window_size_in_days)

        self.create_families()

        self.new_babies_on_day = 0
        for family in self.families:
            baby = family.give_birth()
            if baby:
                self.new_babies_on_day += 1
                self.people.append(baby)
        self.adjust_avg_num_children_per_family()
