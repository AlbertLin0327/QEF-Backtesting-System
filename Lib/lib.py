def mean(data: list):
    # Return the sample arithmetic mean of data.
    n = len(data)
    if n < 1:
        raise TypeError("divide by zero")
    return sum(data) / n

def square_deviation(data: list):
    # Return sum of square deviations of sequence data
    c = mean(data)
    ss = sum((x - c) ** 2 for x in data)
    return ss

def stddev(data: list, ddof=0):
    # Calculate the population standard deviation by default
    # ddof = 1 to compute the sample standard deviation
    n = len(data)
    if n < 2:
        raise TypeError("less than two")
    ss = square_deviation(data)
    pvar = ss / (n - ddof)
    return pvar ** 0.5
