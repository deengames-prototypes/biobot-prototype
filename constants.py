# BASE size of the map at difficulty=1000
MAP_WIDTH = 80
MAP_HEIGHT = 30
DIFFICULTY_PER_ROW_INCREASE = 25
DIFFICULTY_PER_COLUMN_INCREASE = 50
BASE_DIFFICULTY = 1000

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 35 # +5 for status bar + health display

# sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50

# spell values
HEAL_AMOUNT = 4
LIGHTNING_DAMAGE = 20
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_NUM_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12

# Traps
POISON_TRAP_RADIUS = 3
POISON_TRAP_TURNS = 3
POISON_DAMAGE_PERCENT = 0.1
SWAMP_TRAP_STUCK_TURNS = 5

NUM_LAKES = 5
LAKE_RADIUS = 5 # base radius

FOV_ALGO = 'BASIC'
FOV_LIGHT_WALLS = True

LIMIT_FPS = 20  # 20 frames-per-second maximum

DELTA_UP = (0, -1)
DELTA_DOWN = (0, 1)
DELTA_LEFT = (-1, 0)
DELTA_RIGHT = (1, 0)
