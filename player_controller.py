import pygame


class PlayerController:
    def __init__(self, player, sfx, movement):
        self.player = player
        self.sfx = sfx
        self.movement = movement

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and self.player.current_health > 0:
            if event.key == pygame.K_LEFT:
                self.movement[0] = True
            if event.key == pygame.K_RIGHT:
                self.movement[1] = True
            if event.key == pygame.K_UP:
                self.player.attack_pressed = False
                self.player.jump()
            if event.key == pygame.K_d:
                self.player.dash()
            if event.key == pygame.K_SPACE:
                self.player.attack()
            if event.key == pygame.K_e:
                self.player.ranged_attack()
            if event.key == pygame.K_q:
                self.player.cast_spell()
            if event.key == pygame.K_LCTRL:
                self.player.selected_scroll += 1
            if event.key == pygame.K_LSHIFT:
                self.player.selected_item += 1
                self.sfx['select'].play()
            if event.key == pygame.K_f:
                self.player.use_item()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.movement[0] = False
            if event.key == pygame.K_RIGHT:
                self.movement[1] = False
