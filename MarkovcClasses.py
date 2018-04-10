import InputData as InputData
import Parameters as Parameters
import scr.RandomVariantGenerators as RndClasses
import scr.StatisticalClasses as StatClasses
import scr.SamplePathClasses as PathClasses


class Patient:
    def __init__(self, id, parameters):
        self._id = id
        self._rng = None
        self._param = parameters
        self._delta_t = parameters.get_delta_t()
        self._healthStateMonitor = PatientHealthState(parameters)

    def simulate(self, sim_length):
        self._rng = RndClasses.RNG(self._id)

        t = 0

        while self._healthStateMonitor.get_if_alive() and t * self._delta_t < sim_length:

            trans_prob = self._param.get_prob_matrix(self._healthStateMonitor.get_current_state())
            empirical_dist = RndClasses.Empirical(trans_prob)
            new_state_index = empirical_dist.sample(self._rng)

            self._healthStateMonitor.update(t, Parameters.HealthStates(new_state_index))

            t += 1

    def get_survival_time(self):
        return self._healthStateMonitor.get_survival_time()


class PatientHealthState:

    def __init__(self, parameters):
        self._currentState = parameters.get_initial_health_state()
        self._survivalTime = 0
        self._delta_t = parameters.get_delta_t()

    def get_if_alive(self):
        result = True
        if self._currentState == Parameters.HealthStates.Dead:
            result = False
        return result

    def get_current_state(self):
        return self._currentState

    def update(self, t, next_state):

        if not self.get_if_alive():
            return

        if next_state == Parameters.HealthStates.Dead:
            self._survivalTime = (t + 0.5) * self._delta_t

        self._currentState = next_state

    def get_survival_time(self):
        if not self.get_if_alive():
            return self._survivalTime
        else:
            return None


class Cohort:
    def __init__(self, id, therapy):
        self._initial_pop_size = InputData.POP_SIZE
        self._patients = []

        # populate cohort
        for i in range(self._initial_pop_size):
            patient = Patient(id * self._initial_pop_size + i, Parameters.ParametersFixed(therapy))
            self._patients.append(patient)

    def simulate(self):
        for patient in self._patients:
            patient.simulate(InputData.SIM_LENGTH)

        return CohortOutputs(self)

    def get_patients(self):
        return self._patients

    def get_initial_pop_size(self):
        return self._initial_pop_size


class CohortOutputs:
    def __init__(self, simulated_cohort):

        self._survivalTimes = []

        self._survivalCurve = PathClasses.SamplePathBatchUpdate(
            'Population over time', id, simulated_cohort.get_initial_pop_size())

        for patient in simulated_cohort.get_patients():

            survival_time = patient.get_survival_time()
            if not (survival_time is None):
                self._survivalTimes.append(survival_time)
                self._survivalCurve.record(survival_time, -1)

        self._sumStat_survivalTime = StatClasses.SummaryStat(
            'Patient Survival Time', self._survivalTimes)

    def get_sumStat_survival_times(self):
        return self._sumStat_survivalTime

    def get_survival_curve(self):
        return self._survivalCurve






