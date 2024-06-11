import model_c as model

# model.tau_m = 60
# model.tau_f = 144
# model.tau_start = 24
# model.tau_end = 120
# model.tau_preg = 5
# model.tau_gap = 2


simulation_duration = 8*12 # in months
initial_goats = 20 # in months
initial_age = 24 # in months


s = model.Society()
s.initialise(count=initial_goats, age=initial_age)

print(f"Initial: {s.history}\n")
for m in range(simulation_duration):
    s.evolve_month()
    print(f"After {m+1:>3} months: {s.history}")
print(f"\nFinal: {s.history}")