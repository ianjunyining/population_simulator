import Person, parameters as params, report, math

class Similator():
    def __init__(self):
        self.pop = Person.Population(params.people_at_start)
        self.reporter = report.Reporter(self.pop)

    def Similate(self): 
        iterations:int = math.floor(params.run_similation_days / params.window_size_in_days)
        interval_print = math.floor(10 * params.days_in_year / params.window_size_in_days)
        for i in range(iterations):
            if i % interval_print == 0:
                print(f"{i / iterations * 100:.2f}%, {self.pop}")
            self.pop.update()
            self.reporter.record()
        self.reporter.show_stats()
        self.reporter.family_stats()
        self.reporter.plot()
        
            