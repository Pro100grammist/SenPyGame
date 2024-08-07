









































































































































































class Enemy(PhysicsEntity):
    def __init__(self, game, image, pos, size, e_type, health):
        super().__init__(game, image, pos, size)

        self.walking = 0
        self.e_type = e_type
        self.health = health
        self.attacking = False  # Додаємо флаг для атаки

    def update(self, tilemap, movement=(0, 0)):
        """
        Updates enemy status, including movement and collisions.
        """
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
                    if self.flip and dis[0] < 0:
                        self.game.sfx['shoot'].play()
                        self.initiate_attack()
                    elif not self.flip and dis[0] > 0:
                        self.game.sfx['shoot'].play()
                        self.initiate_attack()
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)
        self.set_action('run' if movement[0] != 0 else 'idle')

        self.handle_player_dash_collision()

        if self.health <= 0:
            self.game.effects.append(HitEffect(self.game, self.hitbox.midtop, 0))
            self.game.sfx[self.e_type].play()
            self.game.shaking_screen_effect = max(16, self.game.shaking_screen_effect)
            create_particles(self.game, self.rect().center, self.e_type)
            self.game.player.increase_experience(EXP_POINTS[self.e_type])
            return True
        else:
            return False

    def initiate_attack(self):
        """Ініціює атаку, запустивши анімацію атаки, якщо вона існує."""
        if 'attack' in self.game.assets[self.e_type]:
            self.attacking = True
            self.set_action('attack')
        else:
            self.shoot()

    def handle_attack(self):
        """Обробляє атаку, запускаючи метод shoot після завершення анімації атаки."""
        if self.attacking:
            if self.is_animation_done():
                self.attacking = False
                self.set_action('idle')
                self.shoot()
