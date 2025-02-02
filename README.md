Lifespan Dynamics of Livestock
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

