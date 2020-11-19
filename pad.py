import mouse
import keyboard
from configparser import ConfigParser
from time import sleep
from xinput import XInput
from math import ceil, floor
import threading

SETTINGS = 'settings.ini'


class Gamepad:
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
        'LEFT_THUMB_X',
        'LEFT_THUMB_-X',
        'LEFT_THUMB_Y',
        'LEFT_THUMB_-Y',
        'RIGHT_THUMB_X',
        'RIGHT_THUMB_-X',
        'RIGHT_THUMB_Y',
        'RIGHT_THUMB_-Y'
    ]

    is_button_pressed = {}

    mouse_click_events = {
        'MOUSE_LEFT': 'lmb',
        'MOUSE_RIGHT': 'rmb',
        'MOUSE_MIDDLE': 'mmb',
    }

    mouse_move_events = {
        'MOUSE_MOVE_X': 1,
        'MOUSE_MOVE_Y': 1,
        'MOUSE_MOVE_-X': -1,
        'MOUSE_MOVE_-Y': -1
    }

    mouse = mouse.Mouse()

    # move to a Keyboard class
    def is_key_press(self, action):
        return not self.is_mouse_press(action)

    def is_mouse_press(self, button):
        if button.upper() in self.mouse_click_events:
            return True
        return False

    def press_key(self, button, action):
        if self.is_button_pressed[button]:
            return
        keyboard.press(action)
        self.is_button_pressed[button] = True
        threading.Timer(float(self.config['general']['MOUSE_CLICK_DELAY']), self.release_key, args=[button]).start()

    def press_mouse(self, button, action):
        if self.is_button_pressed[button]:
            return
        self.mouse.button_down(self.mouse_click_events[action])
        self.is_button_pressed[button] = True

        # TODO: simplify condition
    def release_mouse(self, button):
        action = self.config['controls'][button]
        if action and self.is_mouse_press(action) and button in self.is_button_pressed and self.is_button_pressed[
            button]:
            self.mouse.button_up(self.mouse_click_events[action])

            self.is_button_pressed[button] = False

    def scroll_mouse(self, action):
        if action == 'MOUSE_SCROLL_DOWN':
            mouse.wheel(self.mouse_scroll_events['MOUSE_SCROLL_DOWN'])
        if action == 'MOUSE_SCROLL_UP':
            mouse.wheel(self.mouse_scroll_events['MOUSE_SCROLL_UP'])

    def is_mouse_scroll(self, action):
        if action in self.mouse_scroll_events:
            return True

    def handle_input(self, button):
        if button not in self.is_button_pressed:
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
        if self.is_mouse_move(action):
            self.move_mouse(button, action)
            return
        if self.is_key_press(button):
            self.press_key(button, action)

    # TODO: simplify condition
    def release_key(self, button):
        action = self.config['controls'][button]
        if action and self.is_key_press(action) and button in self.is_button_pressed and self.is_button_pressed[button]:
            keyboard.release(action)
            self.is_button_pressed[button] = False

    def handle_thumb(self, thumb):
        if self.api.is_thumb_move(thumb):
            self.handle_input(thumb)

    def handle_thumbs(self):
        for thumb in self.thumbs:
            self.handle_thumb(thumb)

    def is_mouse_move(self, action):
        return action in self.mouse_move_events

    # TODO: refactor
    def move_mouse(self, button, action):
        if button == 'LEFT_THUMB_X' or button == 'LEFT_THUMB_-X':
            value = self.api.get_axis_value('LEFT_THUMB_X')
            normalised_value = self.api.get_normalised_thumb_value(value)
        elif button == 'LEFT_THUMB_Y' or button == 'LEFT_THUMB_-Y':
            value = self.api.get_axis_value('LEFT_THUMB_Y')
            normalised_value = self.api.get_normalised_thumb_value(value)
        elif button == 'RIGHT_THUMB_X' or button == 'RIGHT_THUMB_-X':
            value = self.api.get_axis_value('RIGHT_THUMB_X')
            normalised_value = self.api.get_normalised_thumb_value(value)
        elif button == 'RIGHT_THUMB_Y' or button == 'RIGHT_THUMB_-Y':
            value = self.api.get_axis_value('RIGHT_THUMB_Y')
            normalised_value = self.api.get_normalised_thumb_value(value)
        elif button == 'LEFT_TRIGGER':
            value = self.api.get_trigger_value('LEFT_TRIGGER')
            normalised_value = abs(self.api.get_normalised_trigger_value(value))
        elif button == 'RIGHT_TRIGGER':
            value = self.api.get_trigger_value('RIGHT_TRIGGER')
            normalised_value = abs(self.api.get_normalised_trigger_value(value))
        else:
            normalised_value = 1

        if action == 'MOUSE_MOVE_X':
            self.mouse.move(ceil(normalised_value), 0)
        elif action == 'MOUSE_MOVE_-X':
            self.mouse.move(floor(-normalised_value), 0)
        elif action == 'MOUSE_MOVE_Y':
            self.mouse.move(0, floor(normalised_value))
        elif action == 'MOUSE_MOVE_-Y':
            self.mouse.move(0, ceil(normalised_value))
        else:
            raise Exception('Invalid mouse axis.')

    def detect_button_press(self):
        for button in self.buttons:
            if self.api.is_button_pressed(button):
                self.handle_input(button)
            elif button in self.is_button_pressed and self.is_button_pressed[button]:
                self.release_mouse(button)
                self.release_key(button)

    # TODO: refactor
    def detect_trigger_press(self):
        button = 'LEFT_TRIGGER'
        if self.api.is_trigger_pressed(button):
            self.handle_input(button)
            self.is_button_pressed[button] = True
        elif button in self.is_button_pressed and self.is_button_pressed[button]:
            self.release_mouse('LEFT_TRIGGER')
            self.release_key('LEFT_TRIGGER')

        button = 'RIGHT_TRIGGER'
        if self.api.is_trigger_pressed(button):
            self.handle_input(button)
            self.is_button_pressed[button] = True
        elif button in self.is_button_pressed and self.is_button_pressed[button]:
            self.release_mouse('RIGHT_TRIGGER')
            self.release_key('RIGHT_TRIGGER')

    def run(self):
        self.detect_button_press()
        self.handle_thumbs()
        self.detect_trigger_press()

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(SETTINGS)
        self.api = XInput()
        self.mouse_scroll_events = {
            'MOUSE_SCROLL_DOWN': -float(self.config['general']['SCROLL_SPEED']),
            'MOUSE_SCROLL_UP': float(self.config['general']['SCROLL_SPEED'])
        }


# TODO: handle hot plug
if __name__ == '__main__':
    gamepad = Gamepad()
    print('XBox Controller Mapper started. Press Ctrl+C to stop.')
    while True:
        gamepad.run()
        sleep(float(gamepad.config['general']['DELAY']))
