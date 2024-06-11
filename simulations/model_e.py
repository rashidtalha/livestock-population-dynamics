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
prob_female = 0.5
prob_preg = 0.9
prob_kids = [0.4, 0.3, 0.2, 0.1]

def estimated_life_expectency(female, current_age):
    val = 0
    if female:
        if (0 <= current_age < tau_start):
            if rng.uniform() < prob_start:
                val = tau_start
            else:
                val = rng.integers(0, tau_start)
        if (tau_start <= current_age < tau_end) or (val == tau_start):
            if rng.uniform() < prob_end:
                val = tau_end
            else:
                val = rng.integers(tau_start+tau_preg, tau_end)
        if (tau_end <= current_age) or (tau_end == val):
            val = tau_f
    else:
        val = tau_m
    return val

class Society():
    def __init__(self, count=1, starting_age=0):
        self.families = []

        for _ in range(count):
            f = Family()
            max_age = estimated_life_expectency(True, starting_age)
            f.add_goat(female=True, age=starting_age, life=max_age)
            self.families.append(f)

    def evolve_month(self):
        self.families = [f for f in self.families if f.active]
        for f in self.families:
            root_goat = f.step()
            if root_goat is not None:
                f = Family()
                f.add_goat(female=True, age=tau_start, life=root_goat)
                self.families.append(f)

    @property
    def alive_goats(self):
        goats_f = 0
        goats_m = 0
        self.families = [f for f in self.families if f.active]
        for f in self.families:
            for g in f.goats:
                if g.alive:
                    if g.female:
                        goats_f += 1
                    else:
                        goats_m += 1
        return goats_f, goats_m

    @property
    def active_families(self):
        return len([f for f in self.families if f.active])


class Family():
    def __init__(self):
        self.goats = []
        self.active = len(self.goats) > 0
        self.pledge_complete = False

    def step(self):
        self.goats = [g for g in self.goats if g.alive]
        root_goat = None
        for g in self.goats:
            ## New family dynamics
            if g.starts_new and g.age >= tau_start:
                g.alive = False
                root_goat = g.life_expectancy
                continue

            ## Pregnancy dynamics
            if g.preg:
                g.preg_duration += 1
            else:
                if g.female and g.age >= tau_start and g.age < tau_end and (g.last_preg_end is None or (g.age - g.last_preg_end) >= tau_gap):
                    g.preg = True if rng.uniform(0,1) < prob_preg else False
                    # g.preg_duration += 1

            ## Birthing dynamics
            if g.preg_duration == tau_preg:
                g.preg = False
                g.preg_duration = 0
                g.last_preg_end = g.age
                kids = rng.choice(np.arange(len(prob_kids))+1, p=prob_kids)
                
                for k in range(kids):
                    is_female = True if rng.uniform(0,1) < prob_female else False
                    max_age = estimated_life_expectency(is_female, 0)
                    starts_new = is_female and (not self.pledge_complete) and (max_age > tau_start)
                    if starts_new:
                        self.pledge_complete = True
                    self.add_goat(is_female, 0, max_age, starts_new)
                continue

            ## Death dynamics
            g.age += 1
            g.alive = g.age < g.life_expectancy
        self.active = len([g for g in self.goats if g.alive]) > 0
        return root_goat

    def add_goat(self, female, age, life, starts_new=False):
        self.goats.append(Goat(female, age, life, starts_new))
        self.active = len(self.goats) > 0

    # moving a goat to start a new family is the same as
    # killing that goat (without counter increments) and
    # starting a new family with a goat of the same age

class Goat():
    def __init__(self, female, age, life_expectancy, starts_new=False):
        self.female = female
        self.starts_new = starts_new

        self.life_expectancy = life_expectancy
        self.age = age
        self.alive = self.age < self.life_expectancy
        
        self.preg = False
        self.preg_duration = 0
        self.last_preg_end = None
        # self.pledge_complete = False

    # def step_age(self):
    #     self.age += 1
    #     self.alive = self.age < self.life_expectancy
