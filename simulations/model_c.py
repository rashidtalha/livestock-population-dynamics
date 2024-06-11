import numpy as np
rng = np.random.default_rng()

tau_m = 60
tau_f = 144

tau_start = 24
tau_end = 120

tau_preg = 5
tau_gap = 2

prob_start = 0.95
prob_end = 0.93

class Society():
    def __init__(self):
        self.goats = []
        self.history = {"female_alive":0, "female_dead":0, "male_alive":0, "male_dead":0, "families_cumulative":0}

    def __cleanup(self):
        self.goats = [g for g in self.goats if g.alive]

    def __assign_life_expectancy(self, female, age):
        ### TO BE IMPROVED
        val = 0
        if female:
            if age < tau_start:
                if rng.uniform() < prob_start:
                    val = tau_start
            if (tau_start <= age < tau_end) or (tau_start <= val < tau_end):
                if rng.uniform() < prob_end:
                    val = tau_end
            if (tau_end <= age) or (tau_end <= val):
                val = tau_f
        else:
            val = tau_m
        return val

    def __add_goat(self, female, age, life_expectancy, starts_new):
        if female:
            self.history["female_alive"] += 1
        else:
            self.history["male_alive"] += 1

        self.goats.append(Goat(female, age, life_expectancy, starts_new))

    def __remove_goat(self, female):
        if female:
            self.history["female_alive"] -= 1
            self.history["female_dead"] += 1
        else:
            self.history["male_alive"] -= 1
            self.history["male_dead"] += 1

    def initialise(self, count, age):
        self.history["families_cumulative"] += count
        for _ in range(count):
            life_expectancy = self.__assign_life_expectancy(True, age)
            self.__add_goat(True, age, life_expectancy, False)

    def evolve_month(self):
        self.__cleanup()
        for g in self.goats:
            if g.starts_new and g.age >= tau_start:
                self.history["families_cumulative"] += 1
                g.starts_new = False

            if g.preg:
                g.preg_duration += 1
            else:
                if g.female and g.age >= tau_start and g.age < tau_end and (g.last_preg_end is None or (g.age - g.last_preg_end) >= tau_gap):
                    g.preg = True
                    g.preg_duration += 1

            if g.preg_duration == tau_preg:
                g.preg = False
                g.preg_duration = 0
                g.last_preg_end = g.age
                kids = rng.choice([1,2,3,4], p=[0.4, 0.3, 0.2, 0.1])
                
                for k in range(kids):
                    is_female = True if rng.uniform(0,1) > 0.5 else False
                    life_expectancy = self.__assign_life_expectancy(is_female, 0)
                    starts_new = is_female and (not g.pledge_complete) and (life_expectancy > tau_start)
                    if starts_new: g.pledge_complete = True
                    self.__add_goat(is_female, 0, life_expectancy, starts_new)

            ## Death dynamics
            g.step_age()
            if not g.alive: self.__remove_goat(g.female)


class Goat():
    def __init__(self, female, age, life_expectancy, starts_new):
        self.female = female
        self.starts_new = starts_new

        self.age = age
        self.life_expectancy = life_expectancy
        self.alive = self.age < self.life_expectancy
        
        self.preg = False
        self.preg_duration = 0
        self.last_preg_end = None
        self.pledge_complete = False

    def step_age(self):
        self.age += 1
        self.alive = self.age < self.life_expectancy
