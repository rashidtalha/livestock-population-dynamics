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
            # val = tau_f
            val = rng.integers(tau_end, tau_f)
    else:
        # val = tau_m
        val = rng.integers(0, tau_m)
    return val


class Society():
    def __init__(self, count=1, starting_age=0):
        self.families = []
        self.counters = {"inactive_familes":0}

        for _ in range(count):
            f = Family(True)
            max_age = estimated_life_expectency(True, starting_age)
            f.goats.append(Goat(True, starting_age, max_age, False))
            self.families.append(f)

    def next_month(self, count=1):
        for _ in range(count):
            new_families = []
            for f in self.families:
                for g in f.goats:
                    ## New family dynamics
                    if g.starts_new and g.age >= tau_start:
                        g.alive = False
                        new_families.append((g.age, g.life))
                        continue

                    ## Birthing dynamics
                    if g.preg_duration == tau_preg:
                        g.preg = False
                        g.preg_duration = 0
                        g.last_preg_end = g.age
                        kids = rng.choice(np.arange(len(prob_kids))+1, p=prob_kids)
                        
                        for k in range(kids):
                            is_female = True if rng.uniform(0,1) < prob_female else False
                            max_age = estimated_life_expectency(is_female, 0)
                            starts_new = is_female and (not f.first_female_born) and (max_age > tau_start)
                            if starts_new:
                                f.first_female_born = True
                            f.goats.append(Goat(is_female, 0, max_age, starts_new))
                        continue

                    ## Pregnancy dynamics
                    if g.preg:
                        g.preg_duration += 1
                    else:
                        if g.female and g.age >= tau_start and g.age < tau_end and (g.last_preg_end is None or (g.age - g.last_preg_end) >= tau_gap):
                            g.preg = True if rng.uniform(0,1) < prob_preg else False
                            g.preg_duration += 1

                    ## Death dynamics
                    g.age += 1
                    g.alive = g.age < g.life

                f.goats = [g for g in f.goats if g.alive]
                f.active = len(f.goats) > 0

            for j in new_families:
                f = Family(True)
                f.goats.append(Goat(True, j[0], j[1], False))
                self.families.append(f)

            a = len(self.families)
            self.families = [f for f in self.families if f.active]
            b = len(self.families)
            self.counters["inactive_familes"] += max(a-b, 0)

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

    @property
    def inactive_families(self):
        return self.counters["inactive_familes"]


class Family():
    def __init__(self, active=False):
        """
        Parameters:
        -----------
        active (Bool):
            If this family has any goats or not
        """
        self.goats = []
        self.active = active
        self.first_female_born = False


class Goat():
    def __init__(self, female, age, life, starts_new=False):
        """
        Parameters:
        -----------
        female (Bool):
            The gender of the goat
        age (int):
            Current the age of the goat, in months [0 <= age < MAX]
        life (int):
            The age at which the goat will die, in months [age <= life < MAX]
        starts_new (Bool):
            Whether this goat will start a new family (when it reaches maturity) or not
        """
        self.female = female
        self.starts_new = starts_new
        self.life = life
        self.age = age
        self.alive = self.age < self.life
        self.preg = False
        self.preg_duration = 0
        self.last_preg_end = None
