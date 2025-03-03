import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

rng = np.random.default_rng()

### MODEL-SPECIFIC PARAMETERS (RELATED TO TIME)
t_max_male = 144                # Maximum age of a male goat (in months)
t_max_female = 144              # Maximum age of a female goat (in months)
t_prod_start = 7                # Minimum age after which the female goat can become pregnant (in months)
t_prod_end = 120                # Maximum age after which the female goat cannot become pregnant (in months)
t_preg_duration = 6             # Duration of the pregnancy (in months)
t_preg_gap = 2                  # Minimum gap between pregnancies (in months)
t_sell_min_male = 12            # Minimum age after which a male goat can be sold (in months)
t_sell_min_female = 120         # Minimum age after which a female goat can be sold (in months)

### MODEL-SPECIFIC PARAMETERS (RELATED TO PROBABILITY)
p_prod_start = 0.90             # Probability that the female goat survives until t_prod_start
p_prod_end = 0.85               # Probability that the female goat survives until t_prod_end
p_female_kid = 0.50             # Probability that a new born kid is a female
p_get_pregnant = 0.95           # Probability of getting pregnant in a given month (when all conditions are met)
p_kids = [0.35, 0.45, 0.20]     # Probability distribution for giving birth to 1,2,3,... kids (extend by adding/removing values)
p_sell_male = 0.95              # Probability of being sold (in a given month) for male goats over the age of t_sell_min_male
p_sell_female = 0.95            # Probability of being sold (in a given month) for female goats over the age of t_sell_min_female

### MODEL-SPECIFIC PARAMETERS (RELATED TO ENVIRONMENT)
expand_ownership = True       # Whether the number of owners will grow or not (according to the policy)

### ESTIMATE THE MAXIMUM AGE OF A GOAT
def predict_max_age(is_female, current_age):
    f_1 = lambda x: (((t_max_female - t_prod_end) / (0 - p_prod_start*p_prod_end)) * x) + t_max_female
    f_2 = lambda x: (((t_prod_end - t_prod_start) / (p_prod_start*p_prod_end - p_prod_start)) * (x - p_prod_start)) + t_prod_start
    f_3 = lambda x: (t_prod_start / (p_prod_start - 1)) * (x - 1)
    m_1 = lambda x: t_max_male * (1 - x)

    while True:
        x = rng.uniform(0,1)
        t = m_1(x)
        if is_female:
            t = f_1(x) if x < p_prod_start*p_prod_end else (f_2(x) if x < p_prod_start else f_3(x))
        if t > current_age:
            return int(np.ceil(t))

# WHAT IS A GOAT?
class Goat():
    def __init__(self, is_female, age, max_age, starts_new):
        self.is_female = is_female
        self.age = age
        self.max_age = max_age
        self.starts_new = starts_new

        self.is_alive = self.age <= self.max_age
        self.is_preg = False

        self.months_preg = 0
        self.last_birth_at = None

# FAMILY MEANS OWNER
class Family():
    def __init__(self):
        self.goats = []
        self.first_female_born = False

# SOCIETY IS A COLLECTION OF OWNERS
class Society():
    def __init__(self):
        self.families = []
        self.stats = {
            'num_families': 0,
            'inactive_familes': 0,
            'num_male': 0,
            'dead_male': 0,
            'num_female': 0,
            'dead_female': 0,
        } 

    def add_goats(self, is_female=True, count=1, age=0):
        if expand_ownership:
            for _ in range(count):
                f = Family()
                max_age = predict_max_age(is_female, age)
                f.goats.append( Goat(is_female, age, max_age, False) )
                self.families.append(f)
        else:
            if len(self.families) == 0:
                f = Family()
                f.first_female_born = True
                self.families.append(f)
            
            for _ in range(count):
                f = self.families[0]
                max_age = predict_max_age(is_female, age)
                f.goats.append( Goat(is_female, age, max_age, False) )

        self.stats['num_families'] = len(self.families)
        if is_female:
            self.stats['num_female'] += count
        else:
            self.stats['num_male'] += count

    def next_month(self):
        new_families_bucket = []
        dfam, dfem, dmal = 0, 0, 0

        for f in self.families:
            for g in f.goats:

                # New family dynamics
                if g.starts_new and g.age >= t_prod_start:
                    g.is_alive = False
                    new_families_bucket.append((g.age+1, g.max_age))
                    continue

                # Birthing dynamics
                if g.months_preg == t_preg_duration:
                    g.is_preg = False
                    g.months_preg = 0
                    g.last_birth_at = g.age

                    kids = rng.choice(np.arange(len(p_kids))+1, p=p_kids)

                    for _ in range(kids):
                        is_female = True if rng.uniform(0,1) < p_female_kid else False
                        max_age = predict_max_age(is_female, 0)
                        starts_new = (not f.first_female_born) and is_female and (max_age > t_prod_start)
                        f.goats.append( Goat(is_female, 0, max_age, starts_new) )
                        if starts_new: f.first_female_born = True

                # Pregnancy dynamics
                if (not g.is_preg) and g.is_female and g.age >= t_prod_start and g.age < t_prod_end and ((g.last_birth_at is None) or (g.age - g.last_birth_at) >= t_preg_gap):
                    g.is_preg = True if rng.uniform(0,1) < p_get_pregnant else False
                if g.is_preg: g.months_preg += 1

                # Selling dynamics (male)
                if (not g.is_female) and g.age >= t_sell_min_male:
                    g.is_alive = False if rng.uniform(0,1) < p_sell_male else True
                    if not g.is_alive:
                        self.stats['dead_male'] += 1
                    continue

                # Selling dynamics (female old)
                if g.is_female and g.age >= t_sell_min_female:
                    g.is_alive = False if rng.uniform(0,1) < p_sell_female else True
                    if not g.is_alive:
                        self.stats['dead_female'] += 1
                    continue

                # Ageing and death dynamics
                g.age += 1
                g.is_alive = g.age <= g.max_age
                if not g.is_alive:
                    if g.is_female:
                        self.stats['dead_female'] += 1
                    else:
                        self.stats['dead_male'] += 1

            # Remove all the goats that died during this months
            f.goats = [g for g in f.goats if g.is_alive]

        a = len(self.families)
        self.families = [f for f in self.families if len(f.goats) > 0]
        b = len(self.families)
        self.stats['inactive_familes'] = self.stats['inactive_familes'] + (a-b)

        for j in new_families_bucket:
            f = Family()
            f.goats.append( Goat(True, j[0], j[1], False) )
            self.families.append(f)

        self.stats['num_families'] = len(self.families)
        self.stats['num_male'] = sum([len([g for g in f.goats if not g.is_female]) for f in self.families])
        self.stats['num_female'] = sum([len([g for g in f.goats if g.is_female]) for f in self.families])

### Auxiliary Tools (I/O)
def delta_months(this, base):
    d = relativedelta(this,base)
    return d.months + 12*d.years

def read_data(datafile, sim_end_date=None):
    df = pd.read_csv(
        datafile,
        header=None,
        parse_dates=[0],
        names=["Date", "F Goats", "F Ages", "M Goats", "M Ages"],
        dtype={"F Goats": int, "F Ages": int, "M Goats": int, "M Ages": int},
        comment="#",
    )
    df["Date"] = pd.to_datetime(df["Date"])
    earliest_date = df["Date"].min()
    df["Months"] = df['Date'].apply( lambda x: delta_months(x, earliest_date) )
    months = np.sort(df['Months'].unique())
    df.drop('Date', axis=1, inplace=True)

    if sim_end_date is None:
        duration = None
    elif sim_end_date == 'today':
        duration = delta_months(date.today(), earliest_date)
    else:
        n = datetime.strptime(sim_end_date, '%Y-%m')
        duration = delta_months(n, earliest_date)

    return df, months, duration

### Auxiliary Tools (Running the simulation)
def iterate_history_full(df, duration, additions):
    ha, hi, ma, md, fa, fd = np.zeros((6,duration+1), dtype=int)

    s = Society()
    for month in range(duration):
        if month in additions:
            a = df.loc[df['Months'] == month, ['F Goats', 'F Ages', 'M Goats', 'M Ages']]
            for entry in a.values:
                s.add_goats(True,  entry[0], entry[1])
                s.add_goats(True,  entry[2], entry[3])

        ha[month] = s.stats['num_families']
        hi[month] = s.stats['inactive_familes']
        ma[month] = s.stats['num_male']
        md[month] = s.stats['dead_male']
        fa[month] = s.stats['num_female']
        fd[month] = s.stats['dead_female']

        s.next_month()

    ha[-1] = s.stats['num_families']
    hi[-1] = s.stats['inactive_familes']
    ma[-1] = s.stats['num_male']
    md[-1] = s.stats['dead_male']
    fa[-1] = s.stats['num_female']
    fd[-1] = s.stats['dead_female']

    return ha, hi, ma, md, fa, fd

def iterate_history_final(df, duration, additions):
    ha, hi, ma, md, fa, fd = 0, 0, 0, 0, 0, 0

    s = Society()
    for month in range(duration):
        if month in additions:
            a = df.loc[df['Months'] == month, ['F Goats', 'F Ages', 'M Goats', 'M Ages']]
            for entry in a.values:
                s.add_goats(True,  entry[0], entry[1])
                s.add_goats(True,  entry[2], entry[3])

        s.next_month()

    ha = s.stats['num_families']
    hi = s.stats['inactive_familes']
    ma = s.stats['num_male']
    md = s.stats['dead_male']
    fa = s.stats['num_female']
    fd = s.stats['dead_female']

    return ha, hi, ma, md, fa, fd

### Auxiliary Tools (Running the simulation: final result)
