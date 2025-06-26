"""
Symulator Turnieju Piłkarskiego

Główny moduł programu symulującego turniej piłkarski dla 8 drużyn.
Zawiera logikę przepływu turnieju (faza grupowa i pucharowa).
"""

from models import Team, Match
from utils import save_results
from stats import get_total_goals
from stats import plot_goals, plot_points_distribution
import random
import requests

def get_teams_from_user():
    """
    Pobiera od użytkownika nazwy 8 drużyn uczestniczących w turnieju.

    Returns:
        list: Lista unikalnych nazw drużyn (8 elementów)

    Raises:
        ValueError: Jeśli nazwa jest pusta lub drużyna już istnieje
    """
    print("Podaj dokładnie 8 drużyn do turnieju:")
    teams = set()
    while len(teams) < 8:
        try:
            name = input(f"Podaj nazwę drużyny {len(teams) + 1}: ").strip()
            if not name:
                raise ValueError("Nazwa nie może być pusta.")
            if name in teams:
                raise ValueError("Drużyna o tej nazwie już istnieje.")
            teams.add(name)
        except ValueError as e:
            print(f"Błąd: {e}")
    return list(teams)


def play_group_matches(group_name, teams):
    """
    Przeprowadza wszystkie mecze w fazie grupowej.

    Args:
        group_name (str): Nazwa grupy ('A' lub 'B')
        teams (list): Lista obiektów Team w grupie (4 drużyny)

    Returns:
        list: Lista obiektów Match z rozegranymi meczami
    """
    print(f"\n=== Faza grupowa: Grupa {group_name} ===")
    matches = []
    for i, t1 in enumerate(teams):
        for t2 in teams[i + 1:]:
            match = Match(t1, t2, phase=f"Grupa {group_name}")
            match.play()
            print(match.summary())
            matches.append(match)
    return matches


def sort_group(teams):
    """
    Sortuje drużyny w grupie według punktów i goli.

    Args:
        teams (list): Lista obiektów Team do posortowania

    Returns:
        list: Posortowana lista drużyn
    """
    return sorted(teams, key=lambda t: (t.points, t.goals), reverse=True)


def play_knockout(name, team1, team2):
    """
    Przeprowadza mecz w fazie pucharowej.

    Args:
        name (str): Nazwa fazy (np. 'Półfinał 1')
        team1 (Team): Pierwsza drużyna
        team2 (Team): Druga drużyna

    Returns:
        Match: Obiekt reprezentujący rozegrany mecz
    """
    print(f"\n=== {name} ===")
    match = Match(team1, team2, name)
    match.play()
    print(match.summary())
    return match


def main():
    """Główna funkcja uruchamiająca symulację turnieju."""
    print("=== Symulator Turnieju Piłkarskiego (8 drużyn, 2 grupy) ===")
    team_names = get_teams_from_user()
    random.shuffle(team_names)

    teams = [Team(name) for name in team_names]
    group_a = teams[:4]
    group_b = teams[4:]

    matches_a = play_group_matches("A", group_a)
    top_a = sort_group(group_a)[:2]

    matches_b = play_group_matches("B", group_b)
    top_b = sort_group(group_b)[:2]

    semi1 = play_knockout("Półfinał 1", top_a[0], top_b[1])
    semi2 = play_knockout("Półfinał 2", top_b[0], top_a[1])

    third_place = play_knockout("Mecz o 3. miejsce", semi1.get_loser(), semi2.get_loser())
    final = play_knockout("Finał", semi1.get_winner(), semi2.get_winner())

    print("\n=== 🏆 Końcowa Klasyfikacja ===")
    print(f"🥇 Mistrz: {final.get_winner().name}")
    print(f"🥈 Wicemistrz: {final.get_loser().name}")
    print(f"🥉 Trzecie miejsce: {third_place.get_winner().name}")

    save_results(teams, "data.json")
    print(f"\n📈 Łączna liczba goli w turnieju: {get_total_goals(teams)}")
    plot_goals(teams)
    plot_points_distribution(teams)

if __name__ == "__main__":
    main()