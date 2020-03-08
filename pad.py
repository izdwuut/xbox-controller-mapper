import mouse, keyboard
from configparser import ConfigParser
from time import sleep
from xinput import XInput
from math import ceil, floor
import threading

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

    is_button_pressed = {}

    mouse_click_events = {
        'MOUSE_LEFT': 'left',
        'MOUSE_RIGHT': 'right',
        'MOUSE_MIDDLE': 'middle',
    }

    mouse_move_events = {
        'MOUSE_MOVE_X': 1,
        'MOUSE_MOVE_Y': 1,
        'MOUSE_MOVE_-X': -1,
        'MOUSE_MOVE_-Y': -1
    }

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

    def handle_input(self, button):
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
        if self.is_mouse_move(action):
            self.move_mouse(button, action)
            return
        if self.is_key_press(button):
            self.press_key(button, action)

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


    # TODO: refactor
    def detect_thumb_move(self):
        if self.xinput.is_thumb_move('sThumbLX'):
            if self.xinput.get_value('sThumbLX') > 0:
                self.handle_input('LEFT_THUMB_X')
            else:
                self.handle_input('LEFT_THUMB_-X')
        if self.xinput.is_thumb_move('sThumbLY'):
            if self.xinput.get_value('sThumbLY') > 0:
                self.handle_input('LEFT_THUMB_Y')
            else:
                self.handle_input('LEFT_THUMB_-Y')

        if self.xinput.is_thumb_move('sThumbRX'):
            if self.xinput.get_value('sThumbRX') > 0:
                self.handle_input('RIGHT_THUMB_X')
            else:
                self.handle_input('RIGHT_THUMB_-X')
        if self.xinput.is_thumb_move('sThumbRY'):
            if self.xinput.get_value('sThumbRY') > 0:
                self.handle_input('RIGHT_THUMB_Y')
            else:
                self.handle_input('RIGHT_THUMB_-Y')

    def is_mouse_move(self, action):
        return action in self.mouse_move_events

    def get_normalised_thumb_value(self, value):
        return (float(value) / int(self.config['general']['THUMBS_MAGNITUDE'])) * float(
            self.config['general']['SENSITIVITY'])

    def get_normalised_trigger_value(self, value):
        return (float(value & 0xff) / int(self.config['general']['TRIGGERS_MAGNITUDE'])) * 10 * float(
            self.config['general']['SENSITIVITY'])

    # TODO: refactor
    def move_mouse(self, button, action):
        if button == 'LEFT_THUMB_X' or button == 'LEFT_THUMB_-X':
            value = self.xinput.get_value('sThumbLX')
            normalised_value = abs(self.get_normalised_thumb_value(value))
        elif button == 'LEFT_THUMB_Y' or button == 'LEFT_THUMB_-Y':
            value = self.xinput.get_value('sThumbLY')
            normalised_value = abs(self.get_normalised_thumb_value(value))
        elif button == 'RIGHT_THUMB_X' or button == 'RIGHT_THUMB_-X':
            value = self.xinput.get_value('sThumbRX')
            normalised_value = abs(self.get_normalised_thumb_value(value))
        elif button == 'RIGHT_THUMB_Y' or button == 'RIGHT_THUMB_-Y':
            value = self.xinput.get_value('sThumbRY')
            normalised_value = abs(self.get_normalised_thumb_value(value))
        elif button == 'LEFT_TRIGGER':
            value = self.xinput.get_value('bLeftTrigger')
            normalised_value = abs(self.get_normalised_trigger_value(value))
        elif button == 'RIGHT_TRIGGER':
            value = self.xinput.get_value('bRightTrigger')
            normalised_value = abs(self.get_normalised_trigger_value(value))
        else:
            normalised_value = 1

        if action == 'MOUSE_MOVE_X':
            mouse.move(ceil(normalised_value), 0, absolute=False)
        elif action == 'MOUSE_MOVE_-X':
            mouse.move(floor(-normalised_value), 0, absolute=False)
        elif action == 'MOUSE_MOVE_Y':
            mouse.move(0, floor(-normalised_value), absolute=False)
        else:
            mouse.move(0, ceil(normalised_value), absolute=False)

    def detect_button_press(self):
        for button in self.buttons:
            if self.xinput.is_button_pressed(button):
                self.handle_input(button)
            elif button in self.is_button_pressed and self.is_button_pressed[button]:
                self.release_mouse(button)
                self.release_key(button)

    def detect_trigger_press(self):
        button = 'LEFT_TRIGGER'
        if self.xinput.is_trigger_pressed('bLeftTrigger'):
            self.handle_input(button)
            self.is_button_pressed[button] = True
        elif button in self.is_button_pressed and self.is_button_pressed[button]:
            self.release_mouse('LEFT_TRIGGER')
            self.release_key('LEFT_TRIGGER')

        button = 'RIGHT_TRIGGER'
        if self.xinput.is_trigger_pressed('bRightTrigger'):
            self.handle_input(button)
            self.is_button_pressed[button] = True
        elif button in self.is_button_pressed and self.is_button_pressed[button]:
            self.release_mouse('RIGHT_TRIGGER')
            self.release_key('RIGHT_TRIGGER')


    def run(self):
        self.detect_button_press()
        self.detect_thumb_move()
        self.detect_trigger_press()

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(SETTINGS)
        self.xinput = XInput()
        self.mouse_scroll_events = {
            'MOUSE_SCROLL_DOWN': -float(self.config['general']['SCROLL_SPEED']),
            'MOUSE_SCROLL_UP': float(self.config['general']['SCROLL_SPEED'])
        }


if __name__ == '__main__':
    gamepad = Gamepad()
    print('XBox Controller Mapper started. Press Ctrl+C to stop.')
    while True:
        gamepad.run()
        sleep(float(gamepad.config['general']['DELAY']))
