import Person, parameters, report

class Similator():
    def __init__(self):
        self.pop = Person.Population(parameters.people_at_start)
        self.reporter = report.Reporter()

    def Similate(self): 
        for i in range(parameters.run_similation_days):
            if i == 0:
                print(self.pop.people[0])
            self.pop.update()
            self.reporter.record(self.pop)
        self.reporter.plot()
            