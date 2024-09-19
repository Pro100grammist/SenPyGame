# В мене є проблема з видаленням "вбитих" мобів (екземплярів класу enemy) з карти.
# Це загальний батьківський клас для всіх типів мобів:
class Enemy(PhysicsEntity):
    """
    A class that represents enemy objects.
    """
    def __init__(self, game, image,  pos, size, e_type, health):
        """
        Initializes the Enemy object.

        Parameters:

            :param game: Reference to the game object.
            :param image: an animated object from of a specific type of enemy implemented using the Animation class
            :param pos: Initial position of the enemy.
            :param size: Size of the entity (width, height).
            :param e_type: Type of the entity (in this case, the enemy type).
            :param health: health reserve
        """
        super().__init__(game, image, pos, size)

        self.walking = 0
        self.e_type = e_type
        self.health = health
        self.max_health = health
        self.current_health_bar = None
        self.attacking = False
        self.dying = False
        self.dead = False
        self.attack_cooldown = random.uniform(90, 150)  # random interval from a to b (in frames)
        self.time_since_last_attack = 0

    def handle_player_dash_collision(self):
        """
        Handles collision with the player during dash attack.
        """
        if 50 <= abs(self.game.player.dashing) >= 40:
            if self.hitbox.colliderect(self.game.player.hitbox):
                self.game.shaking_screen_effect = max(16, self.game.shaking_screen_effect)
                self.game.sfx['hit'].play()
                self.game.sfx[self.e_type].play()
                shade = self.e_type
                stamina = self.game.player.stamina

                if stamina >= 25:
                    self.game.player.stamina -= 25
                else:
                    self.game.player.stamina = 0

                damage = 20 * self.game.player.double_power
                self.take_damage(damage)

                self.game.damage_rates.append(DamageNumber(self.hitbox.center, damage, (255, 255, 255)))
                self.game.sfx[self.e_type].play()

                create_particles(self.game, self.hitbox.center, shade)

    def initiate_attack(self):
        """Initiates an attack by launching an attack animation, if it exists."""
        if f'{self.e_type}/attack' in self.game.assets:
            self.attacking = True
            self.set_action('attack')
        else:
            self.shoot()

    def handle_attack(self):
        """Handles the attack by launching the shoot method after the attack animation is complete."""
        if self.attacking:
            if self.is_animation_done():
                self.attacking = False
                self.shoot()
                self.set_action('idle')

    def take_damage(self, amount):
        self.health -= amount
        self.update_health_image()
        print(f"{self.e_type} take {amount} damage")

    def update_health_image(self):
        key = math.floor((self.health / self.max_health) * 10)
        self.current_health_bar = HEALTH_BARS.get(key)

    def victory_handler(self):
        probability = random.random()
        if probability > 0.75:
            self.game.effects.append(HitEffect(self.game, self.hitbox.midtop, 0))
            self.game.shaking_screen_effect = max(16, self.game.shaking_screen_effect)
        elif probability > 0.5:
            self.game.effects.append(HitEffect2(self.game, self.hitbox.midtop, 0))
            self.game.shaking_screen_effect = max(24, self.game.shaking_screen_effect)
        create_particles(self.game, self.rect().center, self.e_type)
        self.game.player.increase_experience(EXP_POINTS[self.e_type])

    def update(self, tilemap, movement=(0, 0)):
        """
        Updates enemy status, including movement and collisions.
        """

        # 1 Find distance to the player along the X and Y axes
        player_distance_x = abs(self.game.player.pos[0] - self.pos[0])
        player_distance_y = abs(self.game.player.pos[1] - self.pos[1])

        # 2 Chase starts if the player comes into view
        if 100 > player_distance_x > 20 and player_distance_y < 50:  # unit of measurement - pixel
            if self.game.player.pos[0] < self.pos[0]:
                self.flip = True
                movement = (-0.5, 0)
            else:
                self.flip = False
                movement = (0.5, 0)

        # 3 Random attack if the player is in the mob's line of sight
        player_distance = math.hypot(self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
        if player_distance < 100:  # unit of measurement - pixel
            self.attack_cooldown -= 1
            if self.attack_cooldown <= 0:
                self.attack_cooldown = random.uniform(90, 150)  # define new random interval
                self.initiate_attack()

        # 4 Handle motion, collision, and other states
        if self.walking:
            if tilemap.checking_physical_tiles((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if self.collisions['right'] or self.collisions['left']:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if abs(dis[1]) < 16:
                    if self.flip and dis[0] < 0 and not self.dying:
                        self.initiate_attack()
                    elif not self.flip and dis[0] > 0 and not self.dying:
                        self.initiate_attack()
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if not self.attacking and not self.dying:
            self.set_action('run' if movement[0] != 0 else 'idle')

        self.handle_attack()
        self.handle_player_dash_collision()

        if self.health <= 0 and not self.dying:
            self.dying = True
            if f'{self.e_type}/dead' in self.game.assets:
                self.set_action('dead')
                if self.e_type == 'golem':
                    self.game.sfx['golem_fall'].play()
            else:
                self.victory_handler()
                if self.e_type == 'big_zombie':
                    self.blow()
                return True

        if self.dying:
            if self.is_animation_done():
                self.dead = True
                return True

            else:
                return False

        return False

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

    def render_health_bar(self, surf, offset=(0, 0), calibration=(0, 0)):
        if self.current_health_bar:
            pos = (self.rect().centerx - self.current_health_bar.get_width() // 2 - calibration[0], self.rect().top - 40 - calibration[1])
            pos_with_offset = (pos[0] - offset[0], pos[1] - offset[1])
            surf.blit(self.current_health_bar, pos_with_offset)

# всі присутні на мапі вороги знаходяться в списку self.enemies, що є атрибутом класу Game, в якому в циклі while not self.game_over: метода run, здійснюється обробка всіх екземплярів ворогів в цій частині коду:
# updating state and rendering enemies
            for enemy in self.enemies.copy():
                if not enemy.update(self.map, (0, 0)):
                    enemy.render(self.display, offset=render_scroll)
                else:
                    self.enemies.remove(enemy)
# це частина конструктора класу Game:

 def __init__(self):
        self.screen = screen
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGTH), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGTH))
        self.clock = pygame.time.Clock()

# і його обробка в циклі  while not self.game_over: метода run
display_mask = pygame.mask.from_surface(self.display)
display_outline = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
sse_offset = (random.random() * self.shaking_screen_effect - self.shaking_screen_effect / 2,
              random.random() * self.shaking_screen_effect - self.shaking_screen_effect / 2)
for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    self.display_2.blit(display_outline, offset)

self.display_2.blit(self.display, (0, 0))
self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), sse_offset)
pygame.display.update()
self.clock.tick(60)

# проблема полягає в тому, що моби, які мають стан анімації 'dead' інколи після їхньої смерті (завершення анімації 'dead') знову з'являються на карті,
# але вже статично стоять на одному місці і їх більше вже не можна вбити.

# Питання: чому так відбувається, де і в чому може бути проблема і як це вирішити.