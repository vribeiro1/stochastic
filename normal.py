import numpy as np

from scipy.stats import norm


def compare_normal(normal1, normal2):
    """
    Returns the probability of the true value of a normally distributed random variable being bigger
    than the true value of another normally distributed random variable

    :param tuple normal1: (mean, std) of the first normal
    :param tuple normal2: (mean, std) of the second normal
    :return: P(Normal1 > Normal2)
    :rtype: float
    """
    n_samples = 1000

    mu1, sigma1 = normal1
    mu2, sigma2 = normal2

    start = mu2 - 4 * sigma2
    stop = mu2 + 4 * sigma2
    step_size = sigma2 / 10
    err = step_size / 2

    P_vector = []
    x = start
    while x <= stop:
        samples = np.random.normal(loc=mu1, scale=sigma1, size=n_samples)
        bigger = len([sample for sample in samples if sample > x])
        P_x = norm.cdf(x + err, loc=mu2, scale=sigma2) - norm.cdf(x - err, loc=mu2, scale=sigma2)

        P_vector.append(P_x * (bigger / n_samples))
        x += step_size

    return sum(P_vector)
