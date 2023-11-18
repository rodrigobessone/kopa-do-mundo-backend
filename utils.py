from datetime import datetime
from exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError,
)


def data_processing(national_squad: dict):
    if national_squad["titles"] < 0:
        raise NegativeTitlesError()

    nation_first_cup = int(national_squad["first_cup"][:4])
    world_cup_year = 1930

    if nation_first_cup < world_cup_year:
        raise InvalidYearCupError

    while world_cup_year < datetime.now().year:
        if world_cup_year == nation_first_cup:
            break
        world_cup_year += 4
    else:
        raise InvalidYearCupError

    possible_titles = (datetime.now().year - nation_first_cup) / 4
    if national_squad["titles"] > possible_titles:
        raise ImpossibleTitlesError