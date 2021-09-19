def mean(data: list):
    """
    Calculate mean for the data list

    Parameters
    ----------
    data: list
        list of numeric data points

    Returns
    -------
    None
    """

    length = len(data)

    # length < 1 then error
    if length < 1:
        raise TypeError("divide by zero")

    return sum(data) / length


def square_deviation(data: list):
    """
    Calculate square deviation for the data list

    Parameters
    ----------
    data: list
        list of numeric data points

    Returns
    -------
    None
    """

    c = mean(data)
    ss = sum((x - c) ** 2 for x in data)

    return ss


def stddev(data: list, ddof=0):
    """
    Calculate the population or sampledd standard deviation by default

    Parameters
    ----------
    data: list
        list of numeric data points
    ddof: [0, 1]
        0 for population std and 1 for sampled std

    Returns
    -------
    None
    """

    length = len(data)

    # length < 2 then error
    if length < 2:
        raise TypeError("less than two")

    ss = square_deviation(data)
    pvar = ss / (length - ddof)

    return pvar ** 0.5
