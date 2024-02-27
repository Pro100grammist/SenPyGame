import json
import itertools

import pygame


AUTOMAP = {
    frozenset([(1, 0), (0, 1)]): 0,
    frozenset([(1, 0), (0, 1), (-1, 0)]): 1,
    frozenset([(-1, 0), (0, 1)]): 2,
    frozenset([(-1, 0), (0, -1), (0, 1)]): 3,
    frozenset([(-1, 0), (0, -1)]): 4,
    frozenset([(-1, 0), (0, -1), (1, 0)]): 5,
    frozenset([(1, 0), (0, -1)]): 6,
    frozenset([(1, 0), (0, -1), (0, 1)]): 7,
    frozenset([(1, 0), (-1, 0), (0, 1), (0, -1)]): 8,
}


NEIGHBOR_OFFSETS = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
PHYSICS_TILES = {'grass', 'stone', 'terrain'}
AUTO_TYPES = {'grass', 'stone', 'terrain'}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def get_ground_level(self, y):
        y_index = int(y / self.tile_size)
        if 0 <= y_index < len(self.tilemap):
            tile_loc = f"0;{y_index}"
            if tile_loc in self.tilemap:
                return y_index * self.tile_size - 32
        return y
        
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc, tile in list(self.tilemap.items()):
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f, indent=4)

    def load(self, path):
        with open(path, 'r') as f:
            map_data = json.load(f)
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
        
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTO_TYPES) and (neighbors in AUTOMAP):
                tile['variant'] = AUTOMAP[neighbors]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']],
                      (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    self.draw_tile(tile, surf, offset)

    def draw_tile(self, tile, surf, offset):
        if tile['type'] == 'animated_tiles':
            try:
                animated_tileset = self.game.assets['animated_tiles'][tile['variant']]
                animation_frame = tile.get('animation_frame', 0)
                animation_frame %= len(animated_tileset)
                surf.blit(animated_tileset[animation_frame], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
            except TypeError:
                pass
        else:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

    def update_animated_tiles(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if tile['type'] == 'animated_tiles':
                animated_tileset = self.game.assets['animated_tiles'][tile['variant']]
                animation_frame = tile.get('animation_frame', 0)
                animation_frame = (animation_frame + 1) % (len(animated_tileset) * tile.get('animation_speed', 1))
                tile['animation_frame'] = animation_frame
