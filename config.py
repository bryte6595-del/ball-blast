"""
config.py - All constants for Ball Blast.
"""

# Grid - fewer columns = bigger blocks = easier to hit
GRID_COLS = 6
GRID_ROWS = 10

# Ball physics
BALL_SPEED    = 300    # pixels/sec - visible and smooth
GRAVITY       = 120    # gentle pull
BALL_RADIUS   = 0.25   # fraction of cell size - bigger = easier to see
FIRE_INTERVAL = 0.15   # seconds between balls

# Danger zone
DANGER_ROW     = GRID_ROWS - 2
FLASH_INTERVAL = 0.35

# Save
SAVE_FILE = "save.json"

# HP stages per wave
HP_STAGES = [
    (1,   5),
    (3,  12),
    (8,  25),
    (20, 55),
    (45, 120),
]

SHAPES = ['circle', 'triangle', 'pentagon', 'hexagon']

# Colors
C_BG_TOP       = (0.04, 0.07, 0.18, 1)
C_BG_BOT       = (0.02, 0.03, 0.10, 1)
C_GRID_BG      = (0.06, 0.10, 0.22, 1)
C_DANGER_LINE  = (0.90, 0.15, 0.15, 1)
C_GRID_LINE    = (0.10, 0.16, 0.32, 1)
C_WALL_BORDER  = (0.25, 0.45, 0.80, 1)

C_BALL         = (1.00, 0.55, 0.10, 1)
C_BALL_GLOW    = (1.00, 0.75, 0.30, 0.20)
C_BALL_TRAIL   = (1.00, 0.55, 0.10, 0.12)

C_GREEN        = (0.20, 0.88, 0.30, 1)
C_YELLOW       = (0.95, 0.88, 0.10, 1)
C_ORANGE       = (0.95, 0.50, 0.10, 1)
C_RED          = (0.90, 0.15, 0.15, 1)
C_PURPLE       = (0.65, 0.10, 0.90, 1)

C_POWERUP      = (0.35, 0.15, 0.95, 1)
C_POWERUP_RING = (0.70, 0.50, 1.00, 0.8)
C_FLASH        = (1.00, 0.08, 0.08, 1)

C_HUD_BG       = (0.04, 0.07, 0.18, 1)
C_BTN_PLAY     = (0.95, 0.50, 0.10, 1)
C_BTN_DARK     = (0.10, 0.15, 0.35, 1)
C_BTN_DANGER   = (0.70, 0.10, 0.10, 1)
