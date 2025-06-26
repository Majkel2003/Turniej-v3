"""
Moduł pomocniczy z funkcjami do zapisu danych.
"""

import json

def save_results(teams, filename="data.json"):
    """
    Zapisuje wyniki turnieju do pliku JSON.

    Args:
        teams (list): Lista obiektów Team
        filename (str, optional): Nazwa pliku. Domyślnie "data.json".

    Raises:
        IOError: Jeśli wystąpi błąd podczas zapisu pliku
    """
    data = [
        {
            "team": t.name,
            "group points": t.points,
            "goals": t.goals
        } for t in teams
    ]
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nWyniki zapisane do pliku: {filename}")
    except IOError as e:
        print(f"Błąd zapisu do pliku: {e}")