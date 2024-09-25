import pygame

from data import NPC_DATA, UI_PATH


class NPC:
    def __init__(self, game, pos, size, animation, name, dialogues, quests, flip=False):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.animation = self.game.assets[animation].copy()
        self.flip = flip
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0] + 16, self.size[1] + 16)
        self.name = name
        self.dialogues = dialogues  # list of dialogs
        self.quests = quests  # list of quests related to NPCs
        self.current_dialogue = 0  # index of the current dialog
        self.completed_quests = []  # list of completed quests

    def create_dialog(self):
        """Open the dialog box"""
        dialog = DialogueWindow(self)
        self.game.active_dialog = dialog
        self.game.player.talks = True

    def get_dialogue(self):
        """Get the current dialog."""
        return self.dialogues[self.current_dialogue]

    def next_dialogue(self):
        """Move the dialog to the next step."""
        if self.current_dialogue < len(self.dialogues) - 1:
            self.current_dialogue += 1

    def start_quest(self, quest):
        """Run the quest."""
        self.quests.append(quest)

    def complete_quest(self, quest):
        """Complete the quest."""
        self.completed_quests.append(quest)
        self.quests.remove(quest)

    def update(self):
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1] + 6))


class OldMan(NPC):
    def __init__(self, game, pos):
        data = NPC_DATA['OldMan']
        quests = {
            'quest1': Quest(
                name="Find Lost Staff",
                description="Find the Old Man's lost staff near the river.",
                objectives=[{'name': 'Find the Staff', 'completed': False}],
                rewards=None
            ),
            'quest2': Quest(
                name="Retrieve the Magic Crystal",
                description="Find and bring back the Magic Crystal from the forest.",
                objectives=[{'name': 'Find the Crystal', 'completed': False}],
                rewards=None
            )
        }

        super().__init__(game, pos, data['size'], data['animation'], data['name'], data['dialogues'], quests)


class Blacksmith(NPC):
    def __init__(self, game, pos):
        data = NPC_DATA['Blacksmith']
        quests = {
            'quest1': Quest(
                name="Bring Iron Ore",
                description="Bring 5 iron ores to the blacksmith.",
                objectives=[{'name': 'Collect 5 Iron Ores', 'completed': False}],
                rewards=None
            )
        }

        super().__init__(game, pos, data['size'], data['animation'], data['name'], data['dialogues'], quests, flip=True)


class Quest:
    def __init__(self, name, description, objectives, rewards, completed=False):
        self.name = name
        self.description = description
        self.objectives = objectives  # List of quest goals
        self.rewards = rewards  # Remuneration for performance
        self.completed = completed

    def is_completed(self):
        """Check if all quest goals have been completed."""
        return all(obj['completed'] for obj in self.objectives)

    def complete_objective(self, objective_name):
        """Mark the goal as completed."""
        for obj in self.objectives:
            if obj['name'] == objective_name:
                obj['completed'] = True

    def complete(self):
        """Mark quest as complete."""
        self.completed = True


class DialogueWindow:
    def __init__(self, npc):
        self.npc = npc
        self.options = []
        self.dialogue_box = UI_PATH.get('dialogue_box')
        self.font = pygame.font.Font('data/fonts/Darinia.ttf', 16)

    def display_dialogue(self):
        """Displays the NPC dialog and options for selection."""
        current_dialogue = self.npc.get_dialogue()
        print(f"{self.npc.name}: {current_dialogue['npc_text']}")

        self.options = current_dialogue['player_choices']
        for i, option in enumerate(self.options):
            print(f"{i + 1}. {option['text']}")

    def select_option(self, option_index):
        selected_option = self.options[option_index]
        print(f"Player: {selected_option['text']}")
        print(f"{self.npc.name}: {selected_option['response']}")
        self.npc.next_dialogue()

        if 'action' in selected_option:
            selected_option['action']()

    def render(self):
        # board
        x = 16
        y = 24
        self.npc.game.display.blit(self.dialogue_box, (x, y))


class QuestJournal:
    def __init__(self, game):
        self.game = game
        self.active_quests = []
        self.completed_quests = []

    def add_quest(self, quest):
        """Adding a new quest to the log."""
        self.active_quests.append(quest)

    def complete_quest(self, quest):
        """Marks the quest as completed and moves it to the list of completed quests."""
        quest.complete()
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)

    def display_journal(self):
        """Displays all active and completed quests."""
        print("Active quests:")
        for quest in self.active_quests:
            print(f"{quest.name}: {quest.description}")
            for obj in quest.objectives:
                status = "Completed" if obj['completed'] else "Not completed"
                print(f"- {obj['name']} [{status}]")

        print("\nCompleted quests:")
        for quest in self.completed_quests:
            print(f"{quest.name}")
