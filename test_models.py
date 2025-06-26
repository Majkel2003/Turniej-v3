"""
Testy jednostkowe dla modułu models.py.
"""

import unittest
import random
from models import Team, Match


class TestTeam(unittest.TestCase):
    """Testy dla klasy Team."""

    def setUp(self):
        self.team = Team("Test Team")

    def test_team_initialization(self):
        """Test poprawnej inicjalizacji drużyny."""
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.points, 0)
        self.assertEqual(self.team.goals, 0)

    def test_team_str_representation(self):
        """Test reprezentacji tekstowej drużyny."""
        self.assertEqual(str(self.team), "Test Team – 0 pkt, 0 goli")


class TestMatch(unittest.TestCase):
    """Testy dla klasy Match."""

    def setUp(self):
        self.team1 = Team("Team A")
        self.team2 = Team("Team B")
        self.match = Match(self.team1, self.team2)

    def test_match_initialization(self):
        """Test poprawnej inicjalizacji meczu."""
        self.assertEqual(self.match.team1.name, "Team A")
        self.assertEqual(self.match.team2.name, "Team B")
        self.assertEqual(self.match.score, (0, 0))
        self.assertEqual(self.match.phase, "Faza grupowa")

    def test_play_group_match(self):
        """Test symulacji meczu w fazie grupowej."""
        random.seed(42)
        self.match.play()

        self.assertTrue(0 <= self.match.score[0] <= 5)
        self.assertTrue(0 <= self.match.score[1] <= 5)

        self.assertEqual(self.team1.goals, self.match.score[0])
        self.assertEqual(self.team2.goals, self.match.score[1])

    def test_play_knockout_match_with_draw(self):
        """Test rzutów karnych w fazie pucharowej."""
        knockout_match = Match(self.team1, self.team2, "Półfinał")
        random.seed(123)
        knockout_match.play()

        if knockout_match.score[0] == knockout_match.score[1]:
            self.assertIsNotNone(knockout_match.penalty_result)
            self.assertEqual(len(knockout_match.penalty_result), 2)


class TestRanking(unittest.TestCase):
    """Testy funkcji związanych z rankingiem."""

    def test_load_teams_with_rank(self):
        """Test ładowania drużyn z rankingiem."""
        with open("test_ranking.txt", 'w') as f:
            f.write("1. Brazylia\n2. Francja\n")

        teams = load_teams_with_rank(["Brazylia", "Polska"], "test_ranking.txt")
        self.assertEqual(teams[0].rank, 1)
        self.assertEqual(teams[1].rank, 50)  # Domyślny ranking

if __name__ == "__main__":
    unittest.main()