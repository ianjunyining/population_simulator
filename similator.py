import Person, parameters, report

class Similator():
    def __init__(self):
        self.pop = Person.Population(parameters.people_at_start)
        self.reporter = report.Reporter(self.pop)

    def Similate(self): 
        for i in range(parameters.run_similation_days):
            if i % 500 == 0:
                print(f"{i / parameters.run_similation_days * 100:.2f}%, {self.pop}")
            self.pop.update()
            self.reporter.record()
        self.reporter.show_stats()
        self.reporter.family_stats()
        self.reporter.plot()
        
            