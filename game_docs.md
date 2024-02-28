# Game Class Documentation

A class that represents the main module of the game.

## Attributes:

- `screen`: The screen of the game.
- `display`: The front surface to display the graphics.
- `display_2`: The rear surface for displaying graphics.
- `clock`: A clock object to control the frame rate.
- `sfx`: Sound effects in the game (dictionary).
- `volume_settings`: Sound volume settings.
- `assets`: All objects, entities, and components in the game (glossary).
- `clouds`: The object responsible for the clouds in the background.
- `raindrops`: A group of objects that represent raindrops.
- `movement`: The movement of the player on the map.
- `player`: The player object.
- `player_controller`: The object controlling the player.
- `tilemap`: The map of the level.
- `ui`: A user interface object.
- `projectiles`: A list of projectiles that are present on the map.
- `animated_projectiles`: A list of current animated projectiles.
- `particles`: A list of particles that are currently displayed on the map.
- `sparks`: A list of sparks currently displayed on the map.
- `weapons`: A list of the player's projectiles that currently exist on the map.
- `spells`: List of magic spells currently being processed on the map.
- `effects`: A list of current effects.
- `damage_rates`: List of damage rates.
- `loot`: List of items in the level.
- `enemies`: List of enemies in the level.
- `shaking_screen_effect`: Screen shaking effect.
- `scroll`: Screen offset.
- `dead`: The status of the player (alive or dead).
- `transition`: Status of the transition between levels.
- `death_timer`: Timer after the player dies.
- `artifacts_remaining`: The number of artifacts remaining in the level.
- `level`: The current level of the game.
- `game_over`: The status of the game over.

## Methods:

### clear_lists(self)
Method for cleaning the list of objects on the map before loading a new level.

- **Description:** Cleans various lists including enemies, loot, projectiles, animated projectiles, particles, sparks, munition, spells, effects, and damage rates.

### load_level(self, map_id)
Method for downloading the level map and all objects.

- **Parameters:**
  - `map_id`: int - The identifier of the map to be loaded.

- **Description:** 
  - Clears lists using the `clear_lists()` method.
  - Loads the level map from a JSON file.
  - Loads music for the level and sets its volume.
  - Adjusts the volume of sound effects.
  - Places enemies on the level map according to spawn locations.
  - Loads game loot items on the map.
  - Initializes rain effect if applicable for the level.
  - Initializes various attributes such as screen offset, player status, and timers.

### projectile_impact(self, projectile)
Method for processing a projectile hitting a physical obstacle.

- **Parameters:**
  - `projectile`: list - Information about the projectile.

- **Description:** 
  - Plays a sound effect indicating a projectile impact.
  - Generates sparks representing the impact.

### harming_the_player(self, projectile)
Method for handling a projectile hit to the player.

- **Parameters:**
  - `projectile`: list - Information about the projectile.

- **Description:** 
  - Reduces player health if not invulnerable.
  - Plays a pain sound effect.
  - Generates visual effects and updates screen shaking.

### run(self)
Method to start the main game cycle.

- **Description:** Starts the game loop, processing all events that occur at a level in the game and updating the game state accordingly.

- **Steps:**
  1. Loads music and background sound effects for the current level.
  2. Defines nested functions for transitioning to the next level and restarting the current level.
  3. Enters the main game loop while the game is not over.
  4. Processes level completion and player status.
  5. Renders the game environment including background, map, enemies, player, projectiles, items, visual effects, and UI elements.
  6. Handles various game events such as collisions, player actions, and user input.
  7. Updates the display and clock to maintain a stable frame rate.

- **Parameters:** None

- **Returns:** None