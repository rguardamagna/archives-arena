import pytest
from app.domain.battle import Player, Enemy, evaluate_answer

def test_correct_answer_reduces_enemy_hp():
    # Arrange
    player = Player(hp=100)
    enemy = Enemy(hp=50)
    
    # Act
    evaluate_answer(
        player=player, 
        enemy=enemy, 
        correct_index=0, 
        chosen_index=0,
        damage=20
    )
    
    # Assert
    assert enemy.hp == 30    # Enemy lost 20 HP
    assert player.hp == 100  # Player remains intact

def test_incorrect_answer_reduces_player_hp():
    # Arrange
    player = Player(hp=100)
    enemy = Enemy(hp=50)
    
    # Act: Player chooses wrong answer (1 instead of 0)
    evaluate_answer(
        player=player, 
        enemy=enemy, 
        correct_index=0, 
        chosen_index=1,
        damage=20
    )
    
    # Assert
    assert enemy.hp == 50   # Enemy remains intact
    assert player.hp == 80  # Player lost 20 HP
