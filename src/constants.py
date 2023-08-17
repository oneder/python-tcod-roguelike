import tcod

import src.color as color

""" INPUT CONSTANTS """

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

CONFIRM_KEYS = {
    tcod.event.K_RETURN,
    tcod.event.K_KP_ENTER,
}

CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}

""" CHARACTER CLASS CONSTANTS """

ENTITY_PLAYER_DEFAULT_COLOR = color.player_alive

ENTITY_PLAYER_TYPE_HUMAN = "Human"
ENTITY_HUMAN_BASE_HP = 20
ENTITY_HUMAN_BASE_DEFENSE = 2
ENTITY_HUMAN_BASE_POWER = 4
ENTITY_HUMAN_BASE_ATTACK_SPEED = 30
ENTITY_HUMAN_BASE_MOVEMENT_SPEED = 8
ENTITY_HUMAN_BASE_INVENTORY_CAPACITY = 26
ENTITY_HUMAN_BASE_LEVEL_UP_BASE = 200
ENTITY_HUMAN_BASE_COLOR = color.player_alive

ENTITY_PLAYER_TYPE_MECH = "Mech"
ENTITY_MECH_BASE_HP = 30
ENTITY_MECH_BASE_DEFENSE = 3
ENTITY_MECH_BASE_POWER = 3
ENTITY_MECH_BASE_ATTACK_SPEED = 20
ENTITY_MECH_BASE_MOVEMENT_SPEED = 6
ENTITY_MECH_BASE_INVENTORY_CAPACITY = 26
ENTITY_MECH_BASE_LEVEL_UP_BASE = 200
ENTITY_MECH_BASE_COLOR = color.player_alive

ENTITY_PLAYER_TYPE_FUNGUS = "Fungus"
ENTITY_FUNGUS_BASE_HP = 15
ENTITY_FUNGUS_BASE_DEFENSE = 4
ENTITY_FUNGUS_BASE_POWER = 2
ENTITY_FUNGUS_BASE_ATTACK_SPEED = 10
ENTITY_FUNGUS_BASE_MOVEMENT_SPEED = 5
ENTITY_FUNGUS_BASE_INVENTORY_CAPACITY = 26
ENTITY_FUNGUS_BASE_LEVEL_UP_BASE = 200
ENTITY_FUNGUS_BASE_COLOR = color.player_alive

""" HOSTILE ENTITY CONSTANTS """

