"""
Moduł zawierający klasy reprezentujące drużyny i mecze.
"""

import random
import requests
from pathlib import Path
from http.client import responses


class Team:
    """
    Klasa reprezentująca drużynę piłkarską.

    Attributes:
        name (str): Nazwa drużyny
        points (int): Liczba punktów w turnieju
        goals (int): Łączna liczba zdobytych goli
    """

    def __init__(self, name, rank=None):
        """
        Inicjalizacja drużyny.

        Args:
            name (str): Nazwa drużyny
        """
        self.name = name
        self.points = 0
        self.goals = 0
        self.rank = rank
    def __str__(self):
        """
        Reprezentacja tekstowa drużyny.

        Returns:
            str: String w formacie 'Nazwa - X pkt, Y goli'
        """
        return f"{self.name} – {self.points} pkt, {self.goals} goli"

class Match:
    """
    Klasa reprezentująca mecz piłkarski.

    Attributes:
        team1 (Team): Pierwsza drużyna
        team2 (Team): Druga drużyna
        score (tuple): Wynik meczu (gole_team1, gole_team2)
        phase (str): Faza turnieju
        penalty_result (tuple): Wynik rzutów karnych (jeśli były)
    """

    def __init__(self, team1, team2, phase="Faza grupowa"):
        """
        Inicjalizacja meczu.

        Args:
            team1 (Team): Pierwsza drużyna
            team2 (Team): Druga drużyna
            phase (str, optional): Faza turnieju. Domyślnie "Faza grupowa".
        """
        self.team1 = team1
        self.team2 = team2
        self.score = (0, 0)
        self.phase = phase
        self.penalty_result = None

    def play(self):
        """Symuluje rozegranie meczu z losowym wynikiem."""
        base_prob = 0.5
        if self.team1.rank and self.team2.rank:
            rank_diff = self.team2.rank - self.team1.rank
            prob = min(0.9, max(0.1, base_prob + rank_diff * 0.05))
        else:
            prob = base_prob
        if random.random() < prob:
            g1 = random.randint(1, 3) + (1 if self.team1.rank < self.team2.rank else 0)
            g2 = random.randint(0, 2)
        else:
            g1 = random.randint(0, 2)
            g2 = random.randint(1, 3) + (1 if self.team2.rank < self.team1.rank else 0)

        self.score = (g1, g2)
        self.update_stats()

    def update_stats(self):
        """Aktualizuje statystyki drużyn po meczu."""
        g1, g2 = self.score
        self.team1.goals += g1
        self.team2.goals += g2
        g1 = random.randint(0, 5)
        g2 = random.randint(0, 5)
        self.score = (g1, g2)
        self.team1.goals += g1
        self.team2.goals += g2

        if self.phase.startswith("Grupa"):
            if g1 > g2:
                self.team1.points += 3
            elif g1 < g2:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1
        else:
            if g1 == g2:
                self.play_penalties()

    def fetch_fifa_ranking(filename="ranking.txt"):
        """Pobiera ranking FIFA z API football-data.org (wymaga klucza API)"""
        API_KEY = "https://www.football-data.org"  # Wymagana rejestracja na https://www.football-data.org/
        url = f"https://api.football-data.org/v4/competitions/WC/standings"

        try:
            response = requests.get(url, headers={"X-Auth-Token": API_KEY}, timeout=10)
            response.raise_for_status()

            with open(filename, 'w') as f:
                for group in response.json()["standings"]:
                    for team in group["table"]:
                        f.write(f"{team['position']}. {team['team']['name']}\n")
            print(f"Zaktualizowano ranking w pliku {filename}")
        except Exception as e:
            print(f"Błąd pobierania rankingu: {e}")
            # Fallback - ręczne tworzenie pliku
            with open(filename, 'w') as f:
                f.write("1. Brazylia\n2. Francja\n3. Argentyna\n")

    def load_teams_with_rank(team_names, filename="ranking.txt"):
        """Łączy nazwy drużyn z rankingiem i przypisuje wagi"""
        ranked_teams = {}

        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split('. ')
                    if len(parts) == 2:
                        rank = int(parts[0])
                        name = parts[1].strip()
                        ranked_teams[name] = rank
        except FileNotFoundError:
            print(f"⚠️ Brak pliku rankingu. Użyj fetch_fifa_ranking()")
            return [Team(name) for name in team_names]

        teams = []
        for name in team_names:
            # Szukanie dopasowania z tolerancją wielkości liter
            matched_name = next(
                (k for k in ranked_teams if k.lower() == name.lower()), None
            )
            rank = ranked_teams.get(matched_name, 50)  # Domyślny ranking 50
            team = Team(name)
            team.rank = rank  # Dodanie rankingu do obiektu Team
            teams.append(team)

        return teams
        # Przypisz rankingi do drużyn użytkownika
        teams = []
        for name in team_names:
            # Dopasowanie bez uwzględniania wielkości liter i białych znaków
            matched_name = next(
                (ranked_name for ranked_name in ranked_teams
                 if ranked_name.lower().strip() == name.lower().strip()),
                None
            )
            teams.append(Team(name, ranked_teams.get(matched_name)))

        return teams
    def play_penalties(self):
        """Symuluje rzuty karne w przypadku remisu w fazie pucharowej."""
        print(f"   🔄 Remis! Rzuty karne między {self.team1.name} i {self.team2.name}")
        p1 = sum(random.choices([0, 1], k=5))
        p2 = sum(random.choices([0, 1], k=5))

        while p1 == p2:
            p1 += random.choice([0, 1])
            p2 += random.choice([0, 1])

        self.penalty_result = (p1, p2)

    def get_winner(self):
        """
        Zwraca zwycięzcę meczu.

        Returns:
            Team: Zwycięska drużyna
        """
        if self.score[0] > self.score[1]:
            return self.team1
        elif self.score[0] < self.score[1]:
            return self.team2
        else:
            return self.team1 if self.penalty_result[0] > self.penalty_result[1] else self.team2

    def get_loser(self):
        """
        Zwazuje przegranego meczu.

        Returns:
            Team: Przegrana drużyna
        """
        winner = self.get_winner()
        return self.team2 if winner == self.team1 else self.team1

    def summary(self):
        """
        Generuje podsumowanie meczu.

        Returns:
            str: Tekstowe podsumowanie meczu
        """
        result = f"[{self.phase}] {self.team1.name} {self.score[0]} : {self.score[1]} {self.team2.name}"
        if self.penalty_result:
            result += f" ⚽ (karne: {self.team1.name} {self.penalty_result[0]} - {self.penalty_result[1]} {self.team2.name})"
        return result