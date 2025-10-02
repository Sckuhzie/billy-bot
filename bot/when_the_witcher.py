from datetime import date, timedelta, datetime
import calendar
from discord import Poll
from typing import List, Tuple

month_map = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}


def get_weekends(
    start_date: date = None, end_date: date = None
) -> List[Tuple[date, date]]:
    if start_date is None:
        start_date = date.today()

    # Default end_date: last day of the next month
    if end_date is None:
        year, month = start_date.year, start_date.month
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        _, num_days = calendar.monthrange(next_year, next_month)
        end_date = date(next_year, next_month, num_days)

    weekends = []

    d = start_date
    while d <= end_date:
        if d.weekday() == 5:  # Saturday
            sunday = d + timedelta(days=1)
            if sunday <= end_date:
                weekends.append((d, sunday))
        d += timedelta(days=1)

    return weekends


def secure_when_the_witcher(start_date: str, end_date: str):
    if start_date is None and end_date is None:
        return None, None
    if start_date is not None:
        try:
            start_date: date = datetime.strptime(start_date, "%d/%m/%y").date()
            print(start_date)
        except ValueError:
            raise ValueError("Couldn't parse properly the start date")

        if end_date is None:
            year, month = start_date.year, start_date.month
            next_month = month + 1 if month < 12 else 1
            next_year = year if month < 12 else year + 1
            _, num_days = calendar.monthrange(next_year, next_month)
            end_date: date = date(next_year, next_month, num_days)
        else:
            try:
                end_date: date = datetime.strptime(end_date, "%d/%m/%y").date()
            except:
                ValueError("Couldn't parse properly the end date")

        delta = end_date - start_date
        if delta > timedelta(days=64):
            raise ValueError(
                "Max 2 mois entre les dates (pas de spam de message ici (même si tu peux spammer les commandes))"
            )
        if delta < 0:
            raise ValueError("Met pas la date de fin avant la date de début")

        return start_date, end_date


def create_list_polls_witcher(start_date: date, end_date: date) -> list[Poll]:
    list_weekends = get_weekends(start_date, end_date)
    list_polls = []
    for weekend in list_weekends:
        saturday, sunday = weekend
        poll_text = f"Week-end du {saturday.day} {month_map[saturday.month]} - {sunday.day} {month_map[sunday.month]}"
        p = Poll(question=poll_text, multiple=True, duration=timedelta(days=3))
        p.add_answer(text="Vendredi soir")
        p.add_answer(text="Samedi journée")
        p.add_answer(text="Samedi soir")
        p.add_answer(text="Dimanche journée")
        p.add_answer(text="Dimanche soir")
        list_polls.append(p)
    return list_polls


if __name__ == "__main__":

    # start_date = date.today()
    # start_date = date(year=2025, month=9, day=1)
    # end_date = date(year=2025, month=9, day=30)
    # weekends = get_weekends(start_date, end_date)

    # print("Upcoming weekends:")
    # for w in weekends:
    #     print(w)
    secure_when_the_witcher("bonjour", None)
