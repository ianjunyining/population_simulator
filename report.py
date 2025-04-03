import matplotlib.pyplot as plt, numpy as np, Person
import parameters as params

class Stats():
    def __init__(self):
        self.number_of_people = 0
        self.males = 0
        self.females = 0
        self.health0 = 0
        self.married = 0
        self.new_families_on_day = 0
        self.new_babies_on_day = 0

class Reporter():
    def __init__(self, population:Person.Population):
        self.population = population
        self.stats_over_time = []
        self.field_names = ["number_of_people", "new_families_on_day", "new_babies_on_day", "married"]

    def record(self):
        stats = Stats()
        stats.number_of_people = self.population.number_of_people()
        stats.males = self.population.number_of_males()
        stats.females = self.population.number_of_females()
        stats.health0 = self.population.people[0].health
        stats.married = self.population.number_of_married()
        stats.new_families_on_day = self.population.new_families_on_day
        stats.new_babies_on_day = self.population.new_babies_on_day
        self.stats_over_time.append(stats)

    def _plot(self, field_name, ax):
        xPlots = []
        yPlots = []
        for i, stats in enumerate(self.stats_over_time):
            xPlots.append(i / params.days_in_year * params.window_size_in_days)
            yPlots.append(getattr(stats, field_name))
        ax.plot(xPlots, yPlots)
        ax.set_title(field_name)


    def plot(self):
        fig = plt.figure()
        axs = [fig.add_subplot(2, 2, j + 1) for j in range(len(self.field_names))]
        for i, name in enumerate(self.field_names):
            self._plot(name, axs[i])
        plt.show()

    def get_stats(self, field_name):
        field_stats = [getattr(stats, field_name) for stats in self.stats_over_time]
        s = sum(field_stats)
        return s, s / len(field_stats)
            
    def show_stats(self):
        for name in self.field_names:
            s, average = self.get_stats(name)
            print(f"name: {name}, sum: {s}, average: {average}")

    def family_stats(self):
        num_children = [len(f.children) for f in self.population.families]
        max_children = [f.max_num_of_children for f in self.population.families]
        print(f"average number of children: {sum(num_children) / max(len(num_children), 1)}")
        # print(f"num_children: {num_children}")
        print(f"average max number of children: {sum(max_children) / max(len(max_children), 1)}")
        # print(f"max_children: {max_children}")



