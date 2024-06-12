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

def estimated_life_expectency(female, current_age):
    val = 0
    if female:
        if current_age < tau_start:
            if rng.uniform() < prob_start:
                val = tau_start
        if (tau_start <= current_age < tau_end) or (tau_start <= val < tau_end):
            if rng.uniform() < prob_end:
                val = tau_end
        if (tau_end <= current_age) or (tau_end <= val):
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
            new_family = f.step()
            if new_family is not None:
                f = Family()
                f.add_goat(female=True, age=tau_start, life=new_family)
                self.families.append(f)
                print(True)

    @property
    def total_goats(self):
        goats_f = 0
        goats_m = 0
        self.families = [f for f in self.families if f.active]
        for f in self.families:
            goats_f += len([g for g in f.goats if (g.alive and g.female)])
            goats_m += len([g for g in f.goats if (g.alive and (not g.female))])
        return goats_f, goats_m

    @property
    def total_families(self):
        return len([f for f in self.families if f.active])


class Family():
    def __init__(self):
        self.goats = []
        self.active = len(self.goats) > 0
        self.pledge_complete = False

    def step(self):
        # self.goats = [g for g in self.goats if g.alive]
        self.update_state()
        new_family = None
        print(len(self.goats))
        for g in self.goats:
            print("TRUESSSS")
            if g.starts_new and g.age >= tau_start:
                g.alive = False
                new_family = g.life_expectancy
                continue

            if g.preg:
                g.preg_duration += 1
            else:
                if g.female and g.age >= tau_start and g.age < tau_end and (g.last_preg_end is None or (g.age - g.last_preg_end) >= tau_gap):
                    g.preg = True
                    # g.preg_duration += 1

            if g.preg_duration == tau_preg:
                g.preg = False
                g.preg_duration = 0
                g.last_preg_end = g.age
                kids = rng.choice([1,2,3,4], p=[0.4, 0.3, 0.2, 0.1])
                
                for k in range(kids):
                    is_female = True if rng.uniform(0,1) > 0.5 else False
                    max_age = estimated_life_expectency(is_female, 0)
                    starts_new = is_female and (not self.pledge_complete) and (max_age > tau_start)
                    if starts_new:
                        self.pledge_complete = True
                    self.add_goat(is_female, 0, max_age, starts_new)

            ## Death dynamics
            g.step_age()

            return new_family

    def add_goat(self, female, age, life, starts_new=False):
        self.goats.append(Goat(female, age, life, starts_new))
        # if self.goats[-1].starts_new: print("HHHMMM", self.goats[-1].starts_new, self.goats[-1].age)
        self.active = len(self.goats) > 0

    # moving a goat to start a new family is the same as
    # killing that goat (without counter increments) and
    # starting a new family with a goat of the same age

    def update_state(self):
        self.goats = [g for g in self.goats if g.alive]
        self.active = len(self.goats) > 0


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
        self.pledge_complete = False

    def step_age(self):
        self.age += 1
        self.alive = self.age < self.life_expectancy

s = Society(3, 0)
print(f"After {0:>2} months: {s.total_goats}, {s.total_families}")

for m in range(120):
    s.evolve_month()
    print(f"After {m+1:>2} months: {s.total_goats}, {s.total_families}")

