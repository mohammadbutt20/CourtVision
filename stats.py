import statistics
from statistics import NormalDist


def prob_over_empirical(points: list[float], line: float) -> float:
    """Empirical P(points > line): fraction of past games that cleared it.

    Args:
        points: A player's scoring history across games.
        line: The over/under threshold (e.g. 24.5).
    Returns:
        Probability the next game exceeds the line, as a proportion (0.0-1.0).
    Raises:
        ZeroDivisionError: If ``len(points) == 0``
    """

    return sum(1 for p in points if p > line) / len(points)


def prob_over_normal(points: list[float], line: float) -> float:
    """Normal P(points > line): probability assuming bell curve.

    Args:
        points: A player's scoring history across games.
        line: The over/under threshold (e.g. 24.5).
    Returns:
        Probability the next game exceeds the line, as a proportion (0.0-1.0).
    Raises:
        StatisticsError: If fewer than 2 games are provided.
    """
    return 1 - statistics.NormalDist(
        statistics.mean(points), statistics.stdev(points)
    ).cdf(line)


def prob_over_monte_carlo(
    points: list[float], line: float, n: int = 10_000, random_seed: int | None = None
) -> float:
    """Monte-Carlo simulation that draws ``n`` samples from ``NormalDist``

    Args:
        points: A player's scoring history across games.
        line: The over/under threshold (e.g. 24.5).
        n: number of trials
        random_seed: Seed for reproducible draws. None means random each call.
    Returns:
        Probability the next game exceeds the line, as a proportion (0.0-1.0).
    Raises:
        StatisticsError: If fewer than 2 games are provided.
    """

    dist = NormalDist.from_samples(points)
    simulated = dist.samples(n, seed=random_seed)

    count = 0
    for x in simulated:
        if x > line:
            count += 1

    return count / n
