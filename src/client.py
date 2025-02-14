import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date

import matplotlib.pyplot as plt
import model

#####################################

# OVERWRITE THE DEFAULT VALUES:

# model.t_max_male = 144                # Maximum age of a male goat (in months)
# model.t_max_female = 144              # Maximum age of a female goat (in months)
# model.t_prod_start = 7                # Minimum age after which the female goat can become pregnant (in months)
# model.t_prod_end = 120                # Maximum age after which the female goat cannot become pregnant (in months)
# model.t_preg_duration = 6             # Duration of the pregnancy (in months)
# model.t_preg_gap = 2                  # Minimum gap between pregnancies (in months)
# model.t_sell_min_male = 12            # Minimum age after which a male goat can be sold (in months)
# model.t_sell_min_female = 120         # Minimum age after which a female goat can be sold (in months)

# model.p_prod_start = 0.90             # Probability that the female goat survives until t_prod_start
# model.p_prod_end = 0.85               # Probability that the female goat survives until t_prod_end
# model.p_female_kid = 0.50             # Probability that a new born kid is a female
# model.p_get_pregnant = 0.95           # Probability of getting pregnant in a given month (when all conditions are met)
# model.p_kids = [0.35, 0.45, 0.20]     # Probability distribution for giving birth to 1,2,3,... kids (extend by adding/removing values)
# model.p_sell_male = 0.95              # Probability of being sold (in a given month) for male goats over the age of t_sell_min_male
# model.p_sell_female = 0.95            # Probability of being sold (in a given month) for female goats over the age of t_sell_min_female

# model.expand_ownership = True        # Whether the number of owners will grow or not (according to the policy)

#####################################

# RUNTIME PARAMETERS:

f_interventions = 'data.csv'    # Record of manually adding new goats
# t_sim = 57                      # Duration of the simulation
iterations = 100                 # Number of iterations (to minimise dispersion due to probablistic effects)
show_graphs = False

#####################################

# SETUP THE SOCIETY, LOAD EXTERNAL INTERVENTIONS & SIMULATE:

def delta_months(this, base):
    d = relativedelta(this,base)
    return d.months + 12*d.years

df = pd.read_csv(
    f_interventions,
    header=None,
    parse_dates=[0],
    names=["Date", "F Goats", "F Ages", "M Goats", "M Ages"],
    dtype={"F Goats": int, "F Ages": int, "M Goats": int, "M Ages": int},
)
df["Date"] = pd.to_datetime(df["Date"])
df["Months"] = df['Date'].apply( lambda x: delta_months(x, df["Date"].min()) )
ending = delta_months(date.today(), df["Date"].min())
unique_months = np.sort(df['Months'].unique())
df.drop('Date', axis=1, inplace=True)

t_sim = ending

#####################################

res = pd.DataFrame({k : np.zeros(t_sim+1, dtype=int) for k in model.Society().stats.keys()})
for t in range(iterations):
    print(f'Iteration # {t+1:>2} (simulating {t_sim} months)')
    
    s = model.Society()
    for m in range(t_sim):
        if m in unique_months:
            a = df.loc[df['Months'] == m, ['F Goats', 'F Ages', 'M Goats', 'M Ages']]
            for entry in a.values:
                s.add_goats(True,  entry[0], entry[1])
                s.add_goats(True,  entry[2], entry[3])
        
        for k in res:
            res.loc[m,k] += s.stats[k]

        s.next_month()
        if m == t_sim-1:
            for k in res:
                res.loc[m+1,k] += s.stats[k]

res = np.ceil(res / iterations).astype(int)

# DISPLAY THE RESULTS:

print(f'\nResults after {t_sim} months (average of {iterations} iterations):')
for k in res:
    print(f'\t{k:<16} = {res[k].iloc[-1]}')

plt.rcParams.update({
    "lines.linewidth": 1.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "legend.framealpha": 1,
    "figure.constrained_layout.use": True,
    "savefig.dpi" : 600,
})

t = np.arange(t_sim+1)

fig, ax = plt.subplots()
ax.plot(t, res['num_male'], c='#0047ab', label="Male")
ax.plot(t, res['num_female'], c='#ff2052', label="Female")
ax.plot(t, res['num_male']+res['num_female'], c='#7d7d7d', label="Total")
ax.legend()
ax.set(ylim=(0,None), xlim=(0,t_sim))
ax.set_title('Alive Goats')
ax.set_xlabel('Months')
plt.savefig("goats.png")
if show_graphs: plt.show()

fig, ax = plt.subplots()
ax.plot(t, res['num_families'], c='#0047ab')
ax.set(ylim=(0,None), xlim=(0,t_sim))
ax.set_title('Active Families')
ax.set_xlabel('Months')
plt.savefig("families.png")
if show_graphs: plt.show()