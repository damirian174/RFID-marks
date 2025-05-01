extends Node

enum DATA_MODES {WRITE, READ, REST}

signal set_data_access(mode: DATA_MODES)
signal data_access(body: Sticker, mode: DATA_MODES)
signal virtual_keyboard_press(button: String)

## Обучение(маркировка)
signal authed
signal hint_keyboard
signal started_filling_in
signal submitted_mark_parameters
