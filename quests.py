import pygame

from data import NPC_DATA, UI_PATH
from items import create_equipment


class NPC:
    def __init__(self, game, pos, size, animation, name, dialogues, quests, avatar, flip=False):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.animation = self.game.assets[animation].copy()
        self.flip = flip
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0] + 16, self.size[1] + 16)
        self.name = name
        self.avatar = avatar
        self.dialogues = dialogues  # list of dialogues
        self.quests = quests  # list of quests related to NPCs
        self.active_quests = []
        self.current_dialogue_index = 0  # track index for current dialogue
        self.dialogue_path = []  # stack to track the path through dialogue
        self.completed_quests = []

    def create_dialog(self):
        """Open the dialog box."""
        dialog = DialogueWindow(self)
        self.game.active_dialog = dialog
        self.game.player.talks = True

    def get_current_dialogue(self):
        """Get current dialog"""
        current_dialogue = self.dialogues[self.current_dialogue_index]
        if self.dialogue_path:
            for index in self.dialogue_path:
                if 'next_choices' in current_dialogue:
                    current_dialogue = current_dialogue['next_choices'].get(index)
                    if current_dialogue is None:
                        return None
                else:
                    return current_dialogue  # Return the current dialog if the following options are not available

        # Check if the current dialog contains 'player_choices'
        if 'player_choices' not in current_dialogue:
            return None

        return current_dialogue

    def next_dialogue(self, current_option=None):
        """Move to the next dialogue based on player's choice."""
        current_dialogue = self.get_current_dialogue()

        # Make sure current_dialogue is valid before proceeding
        if not current_dialogue:
            print("Error: No current dialogue available.")
            return

        # Check if current_dialogue contains 'player_choices'
        if 'player_choices' in current_dialogue and current_option is not None:
            try:
                # Proceed only if 'next_choices' exists and player_choice is valid
                next_choice = current_dialogue['player_choices'][current_option]
                if 'next_choices' in next_choice:
                    self.dialogue_path.append(current_option)
            except (IndexError, TypeError) as e:
                print(f"Error accessing player choice: {e}")

    def start_quest(self, quest_id):
        new_quest = self.quests.get(quest_id)
        if new_quest not in self.active_quests:
            self.active_quests.append(new_quest)
            self.game.quest_journal.add_quest(new_quest, self)
            self.game.sfx['new_journal_entry'].play()

            # Перевірка: чи вже є предмет у гравця
            for obj in new_quest.objectives:
                if obj.obj_type == "find":
                    for item in self.game.player.inventory:
                        if getattr(item, "i_type", None) == obj.target:
                            obj.update(1)
            if new_quest.is_completed():
                self.game.quest_journal.complete_quest(new_quest)

            message = f"Quest '{new_quest.name}' started!"
            notification = QuestNotification(self.game, message, duration=7)
            self.game.notifications.append(notification)

            print(message)
        else:
            print(f"Quest '{new_quest.name}' is already active.")

    def complete_quest(self, quest):
        """Complete the quest."""
        self.completed_quests.append(quest)
        if quest in self.active_quests:
            self.active_quests.remove(quest)

    def update(self):
        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.current_sprite(), self.flip, False),
                  (self.pos[0] - offset[0], self.pos[1] - offset[1] + 6))


def build_objectives(objectives_data):
    objectives = []
    for obj in objectives_data:
        objectives.append(Objective(
            name=obj.get("name"),
            description=obj.get("description", ""),
            objective_type=obj.get("obj_type", "find"),
            target=obj.get("target"),
            quantity=obj.get("quantity", 1),
            completed=obj.get("completed", False)
        ))
    return objectives


def build_reward(reward_data):
    if not reward_data:
        return Reward()

    exp = reward_data.get("exp", 0)
    gold = reward_data.get("gold", 0)

    items = []
    for item in reward_data.get("items", []):
        items.append(create_equipment(name=item))

    spells = reward_data.get("spells", [])

    return Reward(exp=exp, gold=gold, items=items, spells=spells)


class OldMan(NPC):
    def __init__(self, game, pos):
        data = NPC_DATA['OldMan']
        avatar = UI_PATH.get('old_man')
        quests = {
            quest_id: Quest(
                name=quest_data['name'],
                description=quest_data['description'],
                objectives=build_objectives(quest_data['objectives']),
                rewards=build_reward(quest_data.get('rewards')),
                dialogs=quest_data['dialogs']
            ) for quest_id, quest_data in data.get('quests', {}).items()
        }

        super().__init__(game, pos, data['size'], data['animation'], data['name'], data['dialogues'], quests, avatar)


class Blacksmith(NPC):
    def __init__(self, game, pos):
        data = NPC_DATA['Blacksmith']
        avatar = UI_PATH.get('blacksmith')
        quests = {
            quest_id: Quest(
                name=quest_data['name'],
                description=quest_data['description'],
                objectives=quest_data['objectives'],
                rewards=quest_data['rewards'],
                dialogs=quest_data['dialogs']
            ) for quest_id, quest_data in data.get('quests', {}).items()
        }

        super().__init__(game, pos, data['size'], data['animation'], data['name'], data['dialogues'], quests, avatar, flip=True)


class Quest:
    def __init__(self, name, description, objectives, rewards, dialogs, completed=False):
        self.name = name
        self.description = description
        self.objectives = objectives  # List of quest goals
        self.rewards = rewards  # Remuneration for performance
        self.completed = completed
        self.dialogs = dialogs
        self.giver = None

    def is_completed(self):
        """Check if all quest goals have been completed."""
        return all(obj.completed for obj in self.objectives)

    def complete_objective(self, objective_name):
        """Mark the goal as completed."""
        for obj in self.objectives:
            if obj.name == objective_name:
                obj.completed = True

    def complete(self):
        """Mark quest as complete."""
        self.completed = True


class Objective:
    def __init__(self, name, objective_type="generic", description="", target=None, quantity=1, completed=False):
        self.name = name
        self.description = description
        self.obj_type = objective_type  # "find", "kill", "talk_to", "deliver", etc.
        self.target = target
        self.quantity = quantity
        self.completed = completed
        self.progress = 0

    def update(self, amount=1):
        if not self.completed:
            self.progress += amount
            if self.progress >= self.quantity:
                self.completed = True


class Reward:
    def __init__(self, exp=0, gold=0, items=None, spells=None):
        self.exp = exp
        self.gold = gold
        self.items = items or []  # Equipment, Scrolls, GameLoot
        self.spells = spells or []

    def give_to(self, player):
        player.increase_experience(self.exp)
        player.money += self.gold
        for item in self.items:
            player.inventory.append(item)
        for spell in self.spells:
            if spell not in player.spells:
                player.spells.append(spell)


class DialogueWindow:
    def __init__(self, npc):
        self.npc = npc
        self.options = []
        self.current_option = 0
        self.dialogue_box_npc = UI_PATH.get('dialogue_box_npc')
        self.dialogue_box_player = UI_PATH.get('dialogue_box_player')
        self.cursor = UI_PATH.get('cursor')
        self.font = pygame.font.Font('data/fonts/Darinia.ttf', 16)
        self.player_avatar = self.npc.game.player.avatar
        self.current_response = None
        self.current_voice = None
        self.current_voice_channel = None
        self.inactive_options = set()

    def display_dialogue(self):
        """Refreshes and displays dialog options."""
        current_dialogue = self.npc.get_current_dialogue()

        if current_dialogue is None:
            print("Error: Unable to retrieve the current dialog.")
            return

        self.options = current_dialogue.get('player_choices', [])

        if 'next_choices' in current_dialogue:
            self.options = current_dialogue['next_choices']

    def update_dialog(self):
        """Refresh the dialog thread after the quest starts."""
        current_quest = self.npc.active_quests[-1]  # Take the last active quest
        if current_quest and current_quest.dialogs:
            # Update the player's dialog branch based on the active quest
            quest_dialog = current_quest.dialogs[0]  # the first dialog in the list is the initial one
            current_dialogue = self.npc.get_current_dialogue()

            # Replace the corresponding dialog option with a new dialog from the quest
            for i, choice in enumerate(current_dialogue['player_choices']):
                if choice.get('text') == "Any tasks for me?":
                    current_dialogue['player_choices'][i] = quest_dialog
                    break

    def select_option(self):
        if 0 <= self.current_option < len(self.options):
            selected_option = self.options[self.current_option]
        else:
            print("Error: the index of the selected option goes beyond the list")
            return

        if selected_option.get('id'):
            if selected_option['id'] in self.inactive_options:
                return

        # QUEST STATUS UPDATE
        if selected_option.get("status") == "dialogue_completed":
            print("-> Selected option is dialogue_completed")

            for quest in self.npc.quests.values():
                print(f"Checking quest: {quest.name}")
                print(f"Is active: {quest in self.npc.game.quest_journal.active_quests}")

                if quest in self.npc.game.quest_journal.active_quests:
                    # Complete objects of type "deliver" for this NPC
                    for obj in quest.objectives:
                        print(f"Objective type: {obj.obj_type}, target: {obj.target}")
                        print(f"NPC name: {self.npc.name}")
                        print(f"Comparison result: {obj.target == self.npc.name}")

                        if obj.obj_type == "deliver" and obj.target == self.npc.name:
                            print(f"Found deliver objective: {obj.name} for target: {obj.target}")
                            print(f"NPC name: {self.npc.name}")

                            related_find = next((f for f in quest.objectives if f.obj_type == "find"), None)
                            if related_find:
                                for item in self.npc.game.player.inventory:
                                    if getattr(item, "is_quest_item", False) and getattr(item, "i_type", None) == related_find.target:
                                        print(f"Found item in inventory: {item.name}, i_type: {item.i_type}")
                                        obj.completed = True
                                        break

                    if quest.is_completed():

                        quest.rewards.give_to(self.npc.game.player)
                        self.npc.game.quest_journal.complete_quest(quest)
                        print(f"Quest completed: {quest.name}")

                        # Remove only items that were used in the 'find' objectives of this quest
                        quest_targets = [obj.target for obj in quest.objectives if obj.obj_type == "find"]

                        print(f"Removed quest items: {quest_targets}")

                        self.npc.game.player.inventory = [
                            item for item in self.npc.game.player.inventory
                            if not (getattr(item, 'i_type', None) in quest_targets)
                        ]

                        self.npc.game.inventory_menu.refresh_inventory()

                        # Show notifications and sound
                        notification = QuestNotification(self.npc.game, f"Quest '{quest.name}' completed!",
                                                         duration=5)
                        self.npc.game.notifications.append(notification)
                        self.npc.game.sfx['quest_completed'].play()
                    break  # complete the quest cycle

        # work with dialog actions
        if 'action' in selected_option:
            if selected_option['action'] == 'exit':
                self.npc.game.active_dialog = None
                self.npc.game.player.talks = False
                self.stop_voice()
                return
            elif selected_option['action'] == 'next':
                # Moving on to the next stage of the dialog
                self.npc.dialogue_path.append(self.current_option)
                self.options = selected_option.get('next_choices', [])
                self.current_option = 0
                self.render()
                return
            elif selected_option['action'] == 'decline':
                self.stop_voice()
                # return to the main branch
                if self.npc.dialogue_path:
                    self.npc.dialogue_path.pop()  # Delete the current branch (not used yet)
                self.options = self.npc.get_current_dialogue().get('player_choices', [])
                self.current_option = 0  # reset the cursor to the first option
                self.current_response = selected_option.get('response', None)
                self.render()
                return
            elif selected_option['action'].startswith('quest'):
                self.npc.start_quest(selected_option['action'])
                self.update_dialog()
                self.options = self.npc.get_current_dialogue().get('player_choices', [])
                self.current_option = 0
                self.current_response = selected_option.get('response', None)
                self.render()

        self.npc.game.sfx['cursor_select'].play()

        # Set the current npc answer
        self.current_response = selected_option.get('response', None)
        self.current_voice = selected_option.get('npc_voice', None)
        self.stop_voice()

        # Check if there are 'next_choices' for the selected option
        if 'next_choices' in selected_option:
            # Update dialog options based on 'next_choices'
            self.options = selected_option['next_choices']
            self.current_option = 0  # Reset the selection to the first option
            self.render()  # Added to render new options
        else:
            print(f"'next_choices' не знайдено для обраної опції {self.current_option}.")
            self.inactive_options.add(selected_option.get('id', None))  # Add an option to the inactive list

    def move_selection(self, direction):
        """Switching between options."""
        if direction == "up":
            self.current_option = (self.current_option - 1) % len(self.options)
            self.npc.game.sfx['cursor_up'].play()
        elif direction == "down":
            self.current_option = (self.current_option + 1) % len(self.options)
            self.npc.game.sfx['cursor_down'].play()

    @staticmethod
    def split_text_to_lines(text, font, max_width):
        """Splits the text into multiple lines to fit the specified width."""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Check the width of the current line with the new word added
            test_line = current_line + word + " "
            line_width, _ = font.size(test_line)

            if line_width <= max_width:
                current_line = test_line
            else:
                # If the string exceeds the width, add it to the list of strings and start a new one
                lines.append(current_line.strip())
                current_line = word + " "

        # add the last line
        if current_line:
            lines.append(current_line.strip())

        return lines

    def play_voice(self, sound):
        self.current_voice_channel = pygame.mixer.find_channel()  # get a free channel
        if self.current_voice_channel:
            self.current_voice_channel.play(sound)

    def stop_voice(self):
        if self.current_voice_channel:
            self.current_voice_channel.stop()

    def render(self):
        """Renders the dialogue window with text and options."""
        max_text_width = 410
        x = 16
        y = 24
        self.npc.game.display.blit(self.dialogue_box_npc, (x, y))
        self.npc.game.display.blit(self.npc.avatar, (x + 20, y + 36))
        self.npc.game.display.blit(self.dialogue_box_player, (x, y + 180))
        self.npc.game.display.blit(self.player_avatar, (x + 430, y + 223))

        current_dialogue = self.npc.get_current_dialogue()
        npc_text = current_dialogue['npc_text']
        npc_voice = current_dialogue.get('npc_voice', None)

        if npc_voice:
            self.play_voice(self.npc.game.voices[npc_voice])
            current_dialogue['npc_voice'] = None

        # Display NPC text only if there is no active response
        if not self.current_response:
            npc_lines = self.split_text_to_lines(npc_text, self.font, max_text_width)
            line_y = y + 56  # Starting height for the first row
            for line in npc_lines:
                npc_text_surface = self.font.render(line, True, (255, 255, 255))
                self.npc.game.display.blit(npc_text_surface, (x + 180, line_y))
                line_y += 24  # Distance between lines

        option_y = y + 240
        for i, option in enumerate(self.options):
            option_id = option.get('id')
            text_color = (255, 255, 255)
            if option_id:
                if option_id in self.inactive_options:
                    text_color = (128, 128, 128)
            else:
                text_color = (255, 255, 255) if i != self.current_option else (255, 255, 0)

            option_surface = self.font.render(option['text'], True, text_color)
            self.npc.game.display.blit(option_surface, (x + 40, option_y))
            option_y += 30  # Space between options

        # Display the player's answer, if any
        if self.current_response:
            response_lines = self.split_text_to_lines(self.current_response, self.font, max_text_width)
            line_y = y + 56
            for line in response_lines:
                response_surface = self.font.render(line, True, (255, 255, 255))  # Білий колір
                self.npc.game.display.blit(response_surface, (x + 180, line_y))
                line_y += 18

            if self.current_voice:
                self.play_voice(self.npc.game.voices[self.current_voice])
                self.options[self.current_option][self.current_voice] = None
                self.current_voice = None

        # Pointer (arrow or indicator) for selected option
        self.npc.game.display.blit(self.cursor, (x + 16, y + 244 + self.current_option * 30))


class QuestJournal:
    def __init__(self, game):
        self.game = game
        self.active_quests = []
        self.completed_quests = []

    def add_quest(self, quest, giver_npc):
        """Adding a new quest to the log."""
        quest.giver = giver_npc
        self.active_quests.append(quest)

    def complete_quest(self, quest):
        """Marks the quest as completed and moves it to the list of completed quests."""
        quest.complete()
        if quest in self.active_quests:
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
            self.game.sfx['new_journal_entry'].play()
            message = f"Quest '{quest.name}' completed!"
            self.game.notifications.append(QuestNotification(self.game, message, duration=6))

    def get_quest_by_name(self, name):
        for quest in self.active_quests:
            if quest.name == name:
                return
        return None

    def display_journal(self):
        """Displays all active and completed quests."""
        print("Active quests:")
        for quest in self.active_quests:
            print(f"{quest.name}: {quest.description}")
            for obj in quest.objectives:
                status = "Completed" if obj.completed else "Not completed"
                print(f"- {obj.name} [{status}]")

        print("\nCompleted quests:")
        for quest in self.completed_quests:
            print(f"{quest.name}")


class QuestNotification:
    def __init__(self, game, text, duration):
        self.game = game
        self.text = text
        self.duration = duration  # Message display duration (in seconds)
        self.start_time = pygame.time.get_ticks()  # Start time of the message display
        self.font = pygame.font.Font('data/fonts/Darinia.ttf', 24)
        self.color = (255, 255, 255)
        self.bg_color = (50, 50, 50)
        self.padding = 10

    def render(self):
        """Displays the message on the screen."""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Elapsed time in seconds

        if elapsed_time < self.duration:
            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(
                center=(self.game.display.get_width() // 2, self.game.display.get_height() // 2))

            bg_rect = pygame.Rect(
                text_rect.left - self.padding // 2,
                text_rect.top - self.padding // 2,
                text_rect.width + self.padding,
                text_rect.height + self.padding
            )

            pygame.draw.rect(self.game.display, self.bg_color, bg_rect)

            self.game.display.blit(text_surface, text_rect)
        else:
            if self in self.game.notifications:
                self.game.notifications.remove(self)
