"""
grid.py - Manages the entire block grid.
"""

import random
from config import GRID_COLS, GRID_ROWS, DANGER_ROW, FLASH_INTERVAL
from shapes import Block


class Grid:
    def __init__(self):
        self.blocks       = {}   # (col, row) -> Block
        self.wave         = 0
        self._flash_timer = 0.0
        self._flash_state = False
        self.warning      = False

    def add_new_row(self):
        """Shift all blocks up one row, spawn fresh row at bottom."""
        shifted = {}
        for (col, row), block in self.blocks.items():
            shifted[(col, row + 1)] = block
        self.blocks = shifted

        # Pick which columns get blocks this wave
        num_blocks = random.randint(GRID_COLS - 2, GRID_COLS)
        cols = random.sample(range(GRID_COLS), k=num_blocks)

        # Every 3rd wave after wave 1, one block is a power-up
        powerup_col = None
        if self.wave > 0 and self.wave % 3 == 0:
            powerup_col = random.choice(cols)

        for col in cols:
            if col == powerup_col:
                self.blocks[(col, 0)] = Block.make_powerup()
            else:
                self.blocks[(col, 0)] = Block.random_block(self.wave)

        self.wave += 1

    def get_block(self, col: int, row: int):
        return self.blocks.get((col, row))

    def hit_block(self, col: int, row: int) -> tuple:
        """Returns (destroyed, is_powerup)."""
        block = self.blocks.get((col, row))
        if not block:
            return False, False
        is_pu     = block.is_powerup
        destroyed = block.hit()
        if destroyed:
            del self.blocks[(col, row)]
        return destroyed, is_pu

    def is_game_over(self) -> bool:
        return any(row >= GRID_ROWS - 1 for (_, row) in self.blocks)

    def is_warning(self) -> bool:
        return any(row >= DANGER_ROW for (_, row) in self.blocks)

    def tick(self, dt: float):
        if not self.is_warning():
            if self.warning:
                self.warning = False
                for b in self.blocks.values():
                    b.flashing = False
            return
        self.warning       = True
        self._flash_timer += dt
        if self._flash_timer >= FLASH_INTERVAL:
            self._flash_timer = 0.0
            self._flash_state = not self._flash_state
            for b in self.blocks.values():
                b.flashing = self._flash_state

    def all_blocks(self):
        return [(c, r, b) for (c, r), b in self.blocks.items()]
