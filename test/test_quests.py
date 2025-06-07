import pytest
from quests import Objective, Quest, Reward


# --------------------------
# Testing Objective
# --------------------------

def test_objective_progress_and_completion():
    obj = Objective(name="Find the Crystal", objective_type="find", target="magic_crystal", quantity=2)

    assert not obj.completed
    assert obj.progress == 0

    obj.update()
    assert obj.progress == 1
    assert not obj.completed

    obj.update()
    assert obj.progress == 2
    assert obj.completed


# --------------------------
# Testing Quest
# --------------------------

def test_quest_completion_check():
    objectives = [
        Objective("Find", "find", target="crystal", quantity=1),
        Objective("Deliver", "deliver", target="OldMan", quantity=1)
    ]
    quest = Quest(name="Test Quest", description="Desc", objectives=objectives, rewards=None, dialogs=[])

    assert not quest.is_completed()

    quest.complete_objective("Find")
    assert not quest.is_completed()

    quest.complete_objective("Deliver")
    assert quest.is_completed()


# --------------------------
# Testing Reward
# --------------------------

class DummyPlayer:
    def __init__(self):
        self.experience = 0
        self.money = 0
        self.inventory = []
        self.spells = []
        self.exp_multiplier = 1.0
        self.experience_points = 0
        self.level = 1
        self.next_level_experience = 100

    def increase_experience(self, amount):
        self.experience += int(amount * self.exp_multiplier)


def test_reward_application():
    dummy_item = type('DummyItem', (), {})()
    reward = Reward(exp=100, gold=50, items=[dummy_item], spells=["fireball"])

    player = DummyPlayer()
    reward.give_to(player)

    assert player.experience == 100
    assert player.money == 50
    assert dummy_item in player.inventory
    assert "fireball" in player.spells
