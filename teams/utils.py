from datetime import date
from .exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


def data_processing(data: dict):
    today: date = date.today()

    first_cup: int = int(data["first_cup"][0:4])
    titles: int = data["titles"]

    participation_years_gap: int = today.year - first_cup

    total_years_gap: int = first_cup - 1930

    if titles < 0:
        raise NegativeTitlesError()

    if not (total_years_gap % 4) == 0:
        raise InvalidYearCupError()

    if total_years_gap < 0:
        raise InvalidYearCupError()

    if (participation_years_gap / 4) < titles:
        raise ImpossibleTitlesError()
