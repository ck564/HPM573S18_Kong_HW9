import scr.FormatFunctions as F
import InputData as InputData


def print_outcomes(simOuput, therapy_name):

    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOuput.get_sumStat_survival_times().get_mean(),
        interval=simOuput.get_sumStat_survival_times().get_t_CI(alpha=InputData.ALPHA),
        deci=2
    )

    # print outcomes
    print(therapy_name)
    print(" Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - InputData.ALPHA, prec=0),
          survival_mean_CI_text)
