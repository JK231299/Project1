
def main(csvfile, country):
    with open(csvfile, "r") as file:
        lines = file.readlines()

    data = []

    for line in lines:
        # Remove any leading or trailing whitespace and split by the comma
        values = line.strip().split(',')
        data.append(values)

    # 1st Task Maximum and Minimum:

    min_year = 1981  # Minimum year in the range (inclusive)
    max_year = 2000  # Maximum year in the range (inclusive)

    max_employees = float('-inf')
    min_employees = float('inf')
    max_org = ''
    min_org = ''

    # Iterate through the data to find max and min employees in the input country and year range
    for row in data[1:]:
        year_founded = int(row[4])
        if row[
            3] == country and min_year <= year_founded <= max_year:  # Check if country matches and year is within range
            num_employees = int(row[6])  # Convert the number of employees to an integer
            if num_employees > max_employees:
                max_employees = num_employees
                max_org = row[1]
            if num_employees < min_employees:
                min_employees = num_employees
                min_org = row[1]

    result1 = [max_org, min_org]

    # 2nd Task Standard Deviation:

    # Initialize lists to store median salaries for the input country and all organizations
    median_salaries_country = []
    median_salaries_all = []

    # Extract median salaries for the input country and all organizations
    for row in data[1:]:
        median_salary = int(row[7])  # Convert the median salary to an integer
        median_salaries_all.append(median_salary)  # Add to the list for all organizations
        if row[3] == country:
            median_salaries_country.append(median_salary)  # Add to the list for the input country

    # Calculate the mean (average) for the input country
    mean_input_country = sum(median_salaries_country) / len(median_salaries_country)

    # Calculate the mean (average) for all organizations
    mean_all = sum(median_salaries_all) / len(median_salaries_all)

    # Calculate the sum of squared differences for the input country
    squared_diff_input_country = sum((x - mean_input_country) ** 2 for x in median_salaries_country)

    # Calculate the sum of squared differences for all organizations
    squared_diff_all = sum((x - mean_all) ** 2 for x in median_salaries_all)

    # Calculate the standard deviation for the input country
    std_dev_input_country = round((squared_diff_input_country / (len(median_salaries_country) - 1)) ** 0.5 if len(
        median_salaries_country) > 1 else 0.0, 4)

    # Calculate the standard deviation for all organizations
    std_dev_all = round(
        (squared_diff_all / (len(median_salaries_all) - 1)) ** 0.5 if len(median_salaries_all) > 1 else 0.0, 4)

    result2 = [std_dev_input_country, std_dev_all]

    # 3rd Task Ratio:

    profit_increases = 0
    profit_decreases = 0

    # Iterate through the data to calculate profit changes for the input country
    for row in data[1:]:
        if row[3] == country:  # Check if the country matches the input
            profit_2020 = int(row[8])
            profit_2021 = int(row[9])
            profit_change = profit_2021 - profit_2020

            if profit_change > 0:
                profit_increases += profit_change
            elif profit_change < 0:
                profit_decreases += abs(profit_change)

    # Calculate the ratio
    if profit_decreases != 0:
        ratio = profit_increases / profit_decreases
    else:
        ratio = 0.0

    result3 = round(ratio, 4)

    # 4th Task Correlation:

    # Extract data columns

    organization_ids = [row[0] for row in data[1:]]
    countries = [row[3] for row in data[1:]]
    median_salaries = [int(row[7]) for row in data[1:]]
    profits_2020 = [int(row[8]) for row in data[1:]]
    profits_2021 = [int(row[9]) for row in data[1:]]

    # Set input_country to the value of a variable named "country"
    input_country = country  # Replace with the actual value you want to use

    # Find the indices of organizations from the input country with positive profit increases
    positive_increase_indices = [
        i for i, (country, increase) in enumerate(
            zip(countries, [(p21 - p20) / p20 for p21, p20 in zip(profits_2021, profits_2020)])
        )
        if country == input_country and increase > 0
    ]

    # Filter median salaries and profits for organizations from the input country with positive profit increases
    filtered_median_salaries = [median_salaries[i] for i in positive_increase_indices]
    filtered_profits_2021 = [profits_2021[i] for i in positive_increase_indices]

    # Calculate the mean (average) of filtered median salaries and filtered profits for 2021
    mean_median_salaries = sum(filtered_median_salaries) / len(filtered_median_salaries)
    mean_profits_2021 = sum(filtered_profits_2021) / len(filtered_profits_2021)

    # Calculate the covariance and variance
    covariance = sum((x - mean_median_salaries) * (y - mean_profits_2021) for x, y in
                     zip(filtered_median_salaries, filtered_profits_2021))
    variance_median_salaries = sum((x - mean_median_salaries) ** 2 for x in filtered_median_salaries)
    variance_profits_2021 = sum((y - mean_profits_2021) ** 2 for y in filtered_profits_2021)

    # Check if either variance is zero, and handle it appropriately
    if variance_median_salaries == 0 or variance_profits_2021 == 0:
        correlation = 0  # Or set it to some other value as appropriate
    else:
        # Calculate the correlation coefficient
        correlation = round(covariance / (variance_median_salaries ** 0.5 * variance_profits_2021 ** 0.5), 4)

    return result1, result2, result3, correlation

# Calling the function
x1, x2, x3, x4 = main("Organisations.csv", "Belgium")
print(x1)
print(x2)
print(x3)
print(x4)
