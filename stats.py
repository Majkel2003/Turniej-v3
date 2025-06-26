"""
Moduł z funkcjami statystycznymi.
"""
import matplotlib.pyplot as plt
from functools import reduce

def get_total_goals(teams):
    """
    Oblicza łączną liczbę goli w turnieju.

    Args:
        teams (list): Lista obiektów Team

    Returns:
        int: Suma goli wszystkich drużyn
    """
    return reduce(lambda acc, t: acc + t.goals, teams, 0)
def plot_goals(teams):
    if not teams:
        raise ValueError("Lista drużyn nie może być pusta.")
    teams_sorted = sorted(teams, key=lambda t: t.goals, reverse=True)
    names=[team.name for team in teams_sorted]
    goals=[team.goals for team in teams_sorted]
    plt.figure(figsize=(10,6))
    bars=plt.bar(names, goals, color='green')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')

    plt.title('Wykres zdobytych goli przez drużyny')
    plt.xlabel('Nazwy drużyn')
    plt.ylabel('Zdobyte gole')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_points_distribution(teams):
    if not teams:
        raise ValueError("Lista drużyn nie może być pusta.")
    teams_with_points = [t for t in teams if t.points > 0]
    if not teams_with_points:
        print("Żadna drużyna nie zdobyła jeszcze punktów.")
        return

    labels = [f"{t.name}\n({t.points} pkt)" for t in teams_with_points]
    sizes = [t.points for t in teams_with_points]

    plt.figure(figsize=(8,8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor':'white'})
    plt.title('Rozkład punktów między drużynami', fontsize=14)
    plt.tight_layout()
    plt.show()