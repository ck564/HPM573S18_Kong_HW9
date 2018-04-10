import MarkovcClasses as MarkovClasses
import Parameters as Parameters
import SupportMarkovModel as Support
import scr.SamplePathClasses as PathClasses

# no drug
cohort1 = MarkovClasses.Cohort(id=1, therapy=Parameters.Therapies.no_drug)
simOutputs1 = cohort1.simulate()
Support.print_outcomes(simOutputs1, "No drug")

# drug treatment
cohort2 = MarkovClasses.Cohort(id=1, therapy=Parameters.Therapies.tx_drug)
simOutputs2 = cohort2.simulate()
Support.print_outcomes(simOutputs2, "Drug Treatment")


# survival curves
PathClasses.graph_sample_path(
    sample_path=simOutputs1.get_survival_curve(),
    title='Survival curve (no drug)',
    x_label='Simulation time step',
    y_label='Number of alive individuals'
)

PathClasses.graph_sample_path(
    sample_path=simOutputs2.get_survival_curve(),
    title='Survival curve (drug treatment)',
    x_label='Simulation time step',
    y_label='Number of alive individuals'
)




