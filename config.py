"""
config.py - All constants for Ball Blast.
"""

# Grid
GRID_COLS = 7
GRID_ROWS = 11

# Ball physics
BALL_SPEED    = 500    # initial speed pixels/sec
GRAVITY       = 250    # downward pull pixels/sec^2
BALL_RADIUS   = 0.20   # fraction of cell size
FIRE_INTERVAL = 0.10   # seconds between each ball fired
SUB_STEPS     = 12     # collision accuracy steps per frame

# Danger zone
DANGER_ROW    = GRID_ROWS - 2
FLASH_INTERVAL = 0.35

# Save
SAVE_FILE = "save.json"

# HP stages — increases every 5 waves
HP_STAGES = [
    (1,   6),
    (4,  15),
    (10, 35),
    (25, 70),
    (50, 150),
]

# Shapes
SHAPES = ['circle', 'triangle', 'pentagon', 'hexagon']

# ── Colors ────────────────────────────────────────────────────────────────────
C_BG_TOP      = (0.04, 0.07, 0.18, 1)   # dark navy top
C_BG_BOT      = (0.02, 0.03, 0.10, 1)   # darker navy bottom
C_GRID_BG     = (0.06, 0.10, 0.22, 1)   # grid area
C_DANGER_LINE = (0.85, 0.20, 0.20, 0.9) # red danger line
C_GRID_LINE   = (0.10, 0.16, 0.32, 1)   # subtle grid lines

# Ball colors
C_BALL        = (1.00, 0.55, 0.10, 1)   # orange
C_BALL_GLOW   = (1.00, 0.75, 0.30, 0.3) # glow ring

# Block colors by HP
C_GREEN       = (0.20, 0.85, 0.30, 1)
C_YELLOW      = (0.95, 0.85, 0.10, 1)
C_ORANGE      = (0.95, 0.50, 0.10, 1)
C_RED         = (0.90, 0.15, 0.15, 1)
C_PURPLE      = (0.65, 0.10, 0.90, 1)

# Power-up
C_POWERUP     = (0.40, 0.20, 0.95, 1)
C_POWERUP_RING= (0.70, 0.50, 1.00, 0.7)

# Warning flash
C_FLASH       = (1.00, 0.08, 0.08, 1)

# UI
C_HUD_BG      = (0.05, 0.08, 0.20, 1)
C_BTN_PLAY    = (0.95, 0.50, 0.10, 1)
C_BTN_DARK    = (0.12, 0.16, 0.35, 1)
C_BTN_DANGER  = (0.70, 0.10, 0.10, 1)
