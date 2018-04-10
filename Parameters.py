from enum import Enum
import InputData as InputData


class HealthStates(Enum):
    """ health states """
    Well = 0
    Stroke = 1
    Post_Stroke = 2
    Dead = 3


class Therapies(Enum):
    """ no drug vs. anti-coagulation drug """
    no_drug = 0
    tx_drug = 1


class ParametersFixed:
    def __init__(self, therapy):

        self._therapy = therapy
        self._delta_t = InputData.DELTA_T
        self._initialHealthState = HealthStates.Well

        self._prob_matrix = []

        self._prob_matrix = calculate_prob_matrix_nodrug()

        if self._therapy == Therapies.tx_drug:
            self._prob_matrix = calculate_prob_matrix_drug(
                prob_matrix_nodrug=self._prob_matrix,
                stroke_rr=InputData.RR_stroke,
                bleeding_rr=InputData.RR_bleeding
            )

    def get_delta_t(self):
        return self._delta_t

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_prob_matrix(self, state):
        return self._prob_matrix[state.value]


def calculate_prob_matrix_nodrug():

    prob_matrix_nodrug = InputData.PROB_MATRIX
    return prob_matrix_nodrug


def calculate_prob_matrix_drug(prob_matrix_nodrug, stroke_rr, bleeding_rr):

    prob_matrix_drug = InputData.PROB_MATRIX

    prob_matrix_drug[HealthStates.Post_Stroke.value][HealthStates.Stroke.value] \
        = stroke_rr * prob_matrix_nodrug[HealthStates.Post_Stroke.value][HealthStates.Stroke.value]

    prob_matrix_drug[HealthStates.Post_Stroke.value][HealthStates.Dead.value] \
        = stroke_rr * bleeding_rr * prob_matrix_nodrug[HealthStates.Post_Stroke.value][HealthStates.Dead.value]

    prob_matrix_drug[HealthStates.Post_Stroke.value][HealthStates.Post_Stroke.value] \
        = 1 - (prob_matrix_drug[HealthStates.Post_Stroke.value][HealthStates.Stroke.value]
               + prob_matrix_drug[HealthStates.Post_Stroke.value][HealthStates.Dead.value])

    return prob_matrix_drug


# # check probability matrix
# print(calculate_prob_matrix_nodrug())
# print(calculate_prob_matrix_drug(
#     prob_matrix_nodrug=calculate_prob_matrix_nodrug(),
#     stroke_rr=InputData.RR_stroke,
#     bleeding_rr=InputData.RR_bleeding))







