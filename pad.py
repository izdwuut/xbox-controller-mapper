import mouse, keyboard
from configparser import ConfigParser
from time import sleep
from xinput import XInput

SETTINGS = 'settings.ini'

class Gamepad():
    buttons = [
        'DPAD_UP',
        'DPAD_DOWN',
        'DPAD_LEFT',
        'DPAD_RIGHT',
        'START',
        'LEFT_THUMB',
        'RIGHT_THUMB',
        'LEFT_SHOULDER',
        'RIGHT_SHOULDER',
        'A',
        'B',
        'X',
        'Y'
    ]

    # TODO: add mouse scroll
    is_mouse_pressed = {
        'MOUSE_LEFT': False,
        'MOUSE_RIGHT': False,
        'MOUSE_MIDDLE': False
    }

    mouse_mapping = {
        'MOUSE_LEFT': 'left',
        'MOUSE_RIGHT': 'right',
        'MOUSE_MIDDLE': 'middle'
    }

    # move to a Keyboard class
    def is_keypress(self, action):
        return False

    def is_mouse_press(self, action):
        if action.upper() in ['MOUSE_LEFT', 'MOUSE_RIGHT', 'MOUSE_MIDDLE']:
            return True
        return False

    def press_key(self, key):
        keyboard.press(key)

    def press_mouse(self, action):
        for act, button in self.mouse_mapping.items():
            if action == act and not self.is_mouse_pressed[action]:
                mouse.hold(button=button)
                self.is_mouse_pressed[action] = True

    def press_button(self, button):
        action = self.config['controls'][button]
        if not action:
            return
        if self.is_mouse_press(action):
            self.press_mouse(action)
            return
        if self.is_key_press(action):
            self.press_key(action)

    def release_button(self, button):
        action = self.config['controls'][button]
        for act, button in self.mouse_mapping.items():
            if action == act and self.is_mouse_pressed[action]:
                mouse.release(button=button)
        self.is_mouse_pressed[action] = False

    def detect_button_press(self):
        for button in self.buttons:
            if self.xinput.is_button_pressed(button):
                self.press_button(button)
            else:
                self.release_button(button)

    def detect_thumb_move(self):
        pass

    def run(self):
        self.detect_button_press()
        self.detect_thumb_move()

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(SETTINGS)
        self.xinput = XInput()


if __name__ == '__main__':
    gamepad = Gamepad()

    while True:
        gamepad.run()
        sleep(float(gamepad.config['general']['DELAY']))
