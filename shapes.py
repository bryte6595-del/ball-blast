"""
shapes.py - Block class with shape, HP, color, and flash logic.
"""

import random
from config import (
    C_GREEN, C_YELLOW, C_ORANGE, C_RED, C_PURPLE,
    C_POWERUP, C_FLASH, SHAPES, HP_STAGES,
)


class Block:
    def __init__(self, hp: int, shape: str, is_powerup: bool = False):
        self.hp         = hp
        self.max_hp     = hp
        self.shape      = shape
        self.is_powerup = is_powerup
        self.flashing   = False

    def hit(self) -> bool:
        """Returns True if block is destroyed."""
        if self.is_powerup:
            return True
        self.hp -= 1
        return self.hp <= 0

    def color(self):
        if self.is_powerup:
            return C_POWERUP
        if self.flashing:
            return C_FLASH
        if self.hp <= 6:
            return C_GREEN
        elif self.hp <= 15:
            return C_YELLOW
        elif self.hp <= 35:
            return C_ORANGE
        elif self.hp <= 70:
            return C_RED
        else:
            return C_PURPLE

    def border_color(self):
        """Slightly lighter version of block color for outline."""
        r, g, b, a = self.color()
        return (min(1, r + 0.25), min(1, g + 0.25), min(1, b + 0.25), 0.9)

    def toggle_flash(self):
        self.flashing = not self.flashing

    @staticmethod
    def random_block(wave: int) -> 'Block':
        stage  = min(wave // 5, len(HP_STAGES) - 1)
        lo, hi = HP_STAGES[stage]
        hp     = random.randint(lo, hi)
        shape  = random.choice(SHAPES)
        return Block(hp, shape)

    @staticmethod
    def make_powerup() -> 'Block':
        return Block(1, 'circle', is_powerup=True)
