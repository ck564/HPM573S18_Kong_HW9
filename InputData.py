
# Simulation settings
POP_SIZE = 2000  # cohort population size
SIM_LENGTH = 50  # simulation length (years)
ALPHA = 0.05     # significance level for confidence intervals
DELTA_T = 1      # frequency of health state update

# Transition probability matrix with no drug
PROB_MATRIX = [
    [0.75, 0.15, 0.00, 0.10],
    [0.00, 0.00, 1.00, 0.00],
    [0.00, 0.25, 0.55, 0.20],
    [0.00, 0.00, 0.00, 1.00]
]

# Relative risks with anti-coagulation drug
RR_stroke = 0.65
RR_bleeding = 1.05
