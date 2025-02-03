Population Dynamics of Livestock
==============================

### Use.
Run the `client.py` file. This can also be adapted to track/display other statistics. Currently, two plots [`goats.png`](/src/goats.png) and [`families.png`](/src/families.png) are produced.

The `model.py` file contains the main model. No sanity checks are done, so use responsibly.

Each row in the `data.csv` contains a record of how many goats were added to the society. The first column is the month in which these goats were added (zero means at the start of the simulation). The second column list the number of female goats added at that point, and the third column states their age. The fourth and fifth columns give the same data for male goats. Rows don't need to be ordered, and each month can be repeated multiple times. The header row should always be present.

### Dependencies.
```bash
pip install numpy==2.2.*
pip install matplotlib==3.10.*  # optional: for plotting in client.py
```

### Available Parameters.
```python
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
expand_ownership = True         # Whether the number of owners will grow or not (according to the policy)
```

### Sample output.

```
Results after 60 months (average of 50 iterations):
    num_families     = 188
    inactive_familes = 5
    num_male         = 915
    dead_male        = 797
    num_female       = 1603
    dead_female      = 154
```

