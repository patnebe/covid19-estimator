def estimator(data):
    reported_cases = data['reportedCases']

    currently_infected = reported_cases * 10
    severe_currently_infected = reported_cases * 50

    projection_period_in_days = normalize_period(
        data['timeToElapse'], data['periodType'])
    # confirm that the arguments above are correct
    if projection_period_in_days is None:
        return None

    number_of_times_the_cases_will_double = int(projection_period_in_days/3)
    growth_factor = number_of_times_the_cases_will_double
    projected_infections = currently_infected * (2 ** growth_factor)
    projected_severe_infections = severe_currently_infected * \
        (2 ** growth_factor)

    severe_cases_by_requested_time = projected_infections * 0.15
    SI_severe_cases_by_requested_time = projected_severe_infections * 0.15

    # use the totalHospitalBeds input data to 

    response = {
        "data": data,
        "impact": {
            "currentlyInfected": int(currently_infected),
            "infectionsByRequestedTime": int(projected_infections),
            "severeCasesByRequestedTime": int(severe_cases_by_requested_time)
        },
        "severeImpact": {
            "currentlyInfected": int(severe_currently_infected),
            "infectionsByRequestedTime": int(projected_severe_infections),
            "severeCasesByRequestedTime": int(SI_severe_cases_by_requested_time)
        }
    }

    return response


def normalize_period(period_length, period_type):
    number_of_days = None

    if period_type == "days":
        number_of_days = int(period_length)

    elif period_type == "weeks":
        number_of_days = int(7 * period_length)

    elif period_type == "months":
        number_of_days = int(30 * period_length)

    return number_of_days
