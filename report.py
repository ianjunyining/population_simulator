import matplotlib.pyplot as plt, numpy as np, Person


class Stats():
    def __init__(self):
        self.number_of_people = None
        self.males = None
        self.females = None
        self.health0 = None

class Reporter():
    def __init__(self):
        self.stats_over_time = []

    def record(self, population:Person.Population):
        stats = Stats()
        stats.number_of_people = population.number_of_people()
        stats.males = population.number_of_males()
        stats.females = population.number_of_females()
        stats.health0 = population.people[0].health
        self.stats_over_time.append(stats)

    def _plot(self, field_name):
        plt.figure()
        xPlots = []
        yPlots = []
        for i, stats in enumerate(self.stats_over_time):
            xPlots.append(i / 365)
            yPlots.append(getattr(stats, field_name))
        plt.plot(np.array(xPlots), np.array(yPlots))
        plt.show()

    def plot(self):
        self._plot("number_of_people")
        # self._plot("health0")



