# Domain Code: 100% pure Python. No databases, no external APIs.
# Easy to test, easy to maintain.

class Player:
    def __init__(self, hp: int):
        self.hp = hp

class Enemy:
    def __init__(self, hp: int):
        self.hp = hp

def evaluate_answer(player: Player, enemy: Enemy, correct_index: int, chosen_index: int, damage: int):
    """
    Core game business rule:
    If correct, the enemy takes damage.
    If incorrect, the player takes damage.
    """
    if correct_index == chosen_index:
        # Hit: Damage to the enemy
        enemy.hp -= damage
    else:
        # Miss: Damage to the player
        player.hp -= damage
