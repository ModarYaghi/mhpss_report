import pandas as pd


def normalized_value_counts(series):
    counts = series.value_counts(dropna=False)
    percentages = series.value_counts(normalize=True, dropna=False).mul(100).round(2).astype(str) + '%'
    # result = pd.concat([counts, percentages], axis=1, keys=['N', '%'])
    result = pd.DataFrame({
        'N': counts,
        '%': percentages
    })
    return result


def categorize_and_count_ages(ages, start=18, end=80, interval=10):
    """
    Categorize ages into bins and count the number of occurrences in each bin.

    Parameters:
        :param ages: List of ages to categorize.
        :param start: Starting age for the first bin.
        :param end: Ending age for the last bin.
        :param interval: Interval for each age bin.

    Returns:
        pd.Series: Counts of ages in each bin.

    """
    # Define the age bins
    bins = list(range(start, end + 1, interval))

    # Define the labels for each bin
    labels = [f'{bins[i]}-{bins[i + 1] - 1}' for i in range(len(bins) - 1)]

    # Create a pandas' series for the ages
    age_series = pd.Series(ages)

    # Create a new series for the age bins
    age_groups = pd.cut(age_series, bins=bins, labels=labels, right=False)

    # Count the number of occurrences in each bin
    # age_counts = age_groups.value_counts(sort=True)

    # return age_counts
    return age_groups


if __name__ == "__main__":
    # Code to run when this module is executed directly goes here
    # For now, it's just a placeholder
    pass
