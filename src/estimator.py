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

    total_hospital_beds = data['totalHospitalBeds']
    available_beds = 0.35 * total_hospital_beds

    ##############################
    ####     Challenge 3      ####
    ##############################

    cases_for_ICU_by_requested_time = 0.05 * projected_infections

    SI_cases_for_ICU_by_requested_time = 0.05 * projected_severe_infections

    cases_for_ventilators_by_requested_time = 0.02 * projected_infections

    SI_cases_for_ventilators_by_requested_time = 0.02 * projected_severe_infections

    avg_daily_income_USD = data['region']['avgDailyIncomeInUSD']

    avg_daily_income_population = data['region']['avgDailyIncomePopulation']

    dollars_in_flight = (projected_infections * avg_daily_income_USD *
                         avg_daily_income_population) / projection_period_in_days

    dollars_in_flight = '%.2f' % dollars_in_flight

    SI_dollars_in_flight = (projected_severe_infections * avg_daily_income_USD *
                            avg_daily_income_population) / projection_period_in_days

    SI_dollars_in_flight = '%.2f' % SI_dollars_in_flight

    response = {
        "data": data,
        "impact": {
            "currentlyInfected": int(currently_infected),
            "infectionsByRequestedTime": int(projected_infections),
            "severeCasesByRequestedTime": int(severe_cases_by_requested_time),
            "hospitalBedsByRequestedTime": int(available_beds - severe_cases_by_requested_time),
            "casesForICUByRequestedTime": int(cases_for_ICU_by_requested_time),
            "casesForVentilatorsByRequestedTime": int(cases_for_ventilators_by_requested_time),
            "dollarsInFlight": float(dollars_in_flight)
        },
        "severeImpact": {
            "currentlyInfected": int(severe_currently_infected),
            "infectionsByRequestedTime": int(projected_severe_infections),
            "severeCasesByRequestedTime": int(SI_severe_cases_by_requested_time),
            "hospitalBedsByRequestedTime": int(available_beds - SI_severe_cases_by_requested_time),
            "casesForICUByRequestedTime": int(SI_cases_for_ICU_by_requested_time),
            "casesForVentilatorsByRequestedTime": int(SI_cases_for_ventilators_by_requested_time),
            "dollarsInFlight": float(SI_dollars_in_flight)
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
