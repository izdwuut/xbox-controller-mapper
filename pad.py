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

    thumbs = [
        'LEFT_THUMB',
        'RIGHT_THUMB'
    ]

    # TODO: merge with buttons
    is_button_pressed = {}

    mouse_click_events = {
        'MOUSE_LEFT': 'left',
        'MOUSE_RIGHT': 'right',
        'MOUSE_MIDDLE': 'middle',
    }

    mouse_move_events = {
        'MOUSE_MOVE_X': 1,
        'MOUSE_MOVE_Y': 1
    }

    mouse_scroll_events = {
        'MOUSE_SCROLL_DOWN': -1,
        'MOUSE_SCROLL_UP': 1
    }

    # move to a Keyboard class
    def is_key_press(self, action):
        return not self.is_mouse_press(action)

    def is_mouse_press(self, button):
        if button.upper() in self.mouse_click_events:
            return True
        return False

    def press_key(self, key):
        keyboard.press(key)

    def press_mouse(self, button, action):
        if not self.is_button_pressed[button]:
            mouse.hold(button=self.mouse_click_events[action])
            self.is_button_pressed[button] = True

    def scroll_mouse(self, action):
        if action == 'MOUSE_SCROLL_DOWN':
            mouse.wheel(self.mouse_scroll_events['MOUSE_SCROLL_DOWN'])
        if action == 'MOUSE_SCROLL_UP':
            mouse.wheel(self.mouse_scroll_events['MOUSE_SCROLL_UP'])

    def is_mouse_scroll(self, action):
        if action in self.mouse_scroll_events:
            return True

    def press_button(self, button):
        if not button in self.is_button_pressed:
            self.is_button_pressed[button] = False
        action = self.config['controls'][button]
        if not action:
            return
        if self.is_mouse_press(action):
            self.press_mouse(button, action)
            return
        if self.is_mouse_scroll(action):
            self.scroll_mouse(action)
            return
        if self.is_key_press(button):
            self.press_key(action)

    # TODO: simplify condition
    def release_mouse(self, button):
        action = self.config['controls'][button]
        if action and self.is_mouse_press(action) and button in self.is_button_pressed and self.is_button_pressed[button]:
            mouse.release(button=self.mouse_click_events[action])
            self.is_button_pressed[button] = False

    # TODO: simplify condition
    def release_key(self, button):
        action = self.config['controls'][button]
        if action and self.is_key_press(action) and button in self.is_button_pressed and self.is_button_pressed[button]:
            keyboard.release(action)
            self.is_button_pressed[button] = False

    def detect_thumb_move(self):
        if self.xinput.is_left_thumb_x_move():
            print(self.xinput.get_left_thumb_x_move())

    def detect_button_press(self):
        for button in self.buttons:
            if self.xinput.is_button_pressed(button):
                self.press_button(button)
            else:
                self.release_mouse(button)
                self.release_key(button)
        self.detect_thumb_move()

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
