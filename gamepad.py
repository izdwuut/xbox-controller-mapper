from mouse import Mouse
from keyboard import Keyboard
from configparser import ConfigParser
from time import sleep
from xinput import XInput
from math import ceil, floor
import os
import sys


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
    _is_pressed = {}
    mouse_click_events = [
        'MOUSE_LEFT',
        'MOUSE_MIDDLE',
        'MOUSE_RIGHT',
    ]
    mouse_move_events = {
        'MOUSE_MOVE_X': 1,
        'MOUSE_MOVE_Y': 1,
        'MOUSE_MOVE_-X': -1,
        'MOUSE_MOVE_-Y': -1
    }
    mouse_scroll_events = {
        'MOUSE_SCROLL_DOWN',
        'MOUSE_SCROLL_UP'
    }

    mouse = Mouse()
    keyboard = Keyboard()

    def __init__(self, profile='default.ini'):
        config = ConfigParser()

        config.read(profile)
        self.config = config
        self.api = XInput(profile)
        self.mouse_scroll_events = {
            'MOUSE_SCROLL_DOWN': -float(self.config['general']['SCROLL_SPEED']),
            'MOUSE_SCROLL_UP': float(self.config['general']['SCROLL_SPEED'])
        }

    @classmethod
    def from_profile(cls):
        profiles = [profile for profile in os.listdir('.') if profile.endswith('.ini')]
        if len(profiles) == 1:
            cls.validate_profile(profiles[0])
            return cls(profiles[0])
        print('Profiles:')
        for i in range(len(profiles)):
            print('{}. {}'.format(i, profiles[i]))

        index = None
        while True:
            choice = input('Select profile: ')
            try:
                index = int(choice)
            except ValueError:
                print('Invalid value.')
                continue
            if index < 0 or index > len(profiles) - 1:
                print('Invalid value.')
                continue
            break
        cls.validate_profile(profiles[0])
        return cls(profiles[index])

    # TODO: validate the rest of the profile
    @classmethod
    def validate_profile(cls, profile):
        config = ConfigParser()
        config.read(profile)
        print('Checking profile...')
        if 'general' not in config:
            print('No "general" section in loaded profile.')
            sys.exit()
        for option in config['general']:
            if '.' in config['general'][option]:
                func = float
            else:
                func = int
            try:
                func(config['general'][option])
            except ValueError:
                print('Invalid "{}" option value.'.format(option.upper()))
                sys.exit()
        print('Profile OK!')

    # TODO: unify methods name (they should start with handle_)
    def run(self):
        self.detect_button_press()
        self.handle_thumbs()
        self.handle_triggers_press()

    def is_key_press(self, action):
        mouse_events = [*self.mouse_move_events.keys(), *self.mouse_scroll_events, *self.mouse_click_events]
        return action not in mouse_events

    def is_mouse_press(self, button):
        if button.upper() in self.mouse_click_events:
            return True
        return False

    def press_key(self, button, action):
        if self._is_pressed[button]:
            return
        self.keyboard.key_down(action)
        self._is_pressed[button] = True

    def press_mouse(self, button, action):
        if self._is_pressed[button]:
            return
        self.mouse.button_down(action)
        self._is_pressed[button] = True

    def release_mouse(self, button):
        action = self.config['controls'][button]
        if action and self.is_mouse_press(action) and self.is_pressed(button):
            self.mouse.button_up(action)
            self._is_pressed[button] = False

    # TODO: handle scroll
    def scroll_mouse(self, action):
        # if action == 'MOUSE_SCROLL_DOWN':
        #     mouse.wheel(self.mouse_scroll_events['MOUSE_SCROLL_DOWN'])
        # if action == 'MOUSE_SCROLL_UP':
        #     mouse.wheel(self.mouse_scroll_events['MOUSE_SCROLL_UP'])
        pass

    def is_mouse_scroll(self, action):
        if action in self.mouse_scroll_events:
            return True

    def handle_input(self, button):
        if button not in self._is_pressed:
            self._is_pressed[button] = False
        action = self.config['controls'][button]
        if not action:
            return
        if self.is_mouse_press(action):
            self.press_mouse(button, action)
            return
        if self.is_mouse_move(action):
            self.move_mouse(button, action)
            return
        if self.is_key_press(button):
            self.press_key(button, action)
        if self.is_mouse_scroll(action):
            self.scroll_mouse(action)
            return

    def release_key(self, button):
        action = self.config['controls'][button]
        if action and self.is_key_press(action) and self.is_pressed(button):
            self.keyboard.key_up(action)
            self._is_pressed[button] = False

    def handle_thumb(self, thumb):
        if self.api.is_thumb_move(thumb):
            self.handle_input(thumb)
        elif self.is_pressed(thumb):
            self.release_mouse(thumb)
            self.release_key(thumb)

    def is_pressed(self, button):
        return button in self._is_pressed and self._is_pressed[button]

    def handle_thumbs(self):
        for thumb in self.thumbs:
            self.handle_thumb(thumb)

    def is_mouse_move(self, action):
        return action in self.mouse_move_events

    def move_mouse(self, button, action):
        if 'THUMB' in button:
            normalised_value = self.api.get_normalised_thumb_value(button)
        elif 'TRIGGER' in button:
            normalised_value = abs(self.api.get_normalised_trigger_value(button))
        else:
            normalised_value = 1

        if action == 'MOUSE_MOVE_X':
            self.mouse.move(ceil(normalised_value), 0)
        elif action == 'MOUSE_MOVE_-X':
            self.mouse.move(floor(normalised_value), 0)
        elif action == 'MOUSE_MOVE_Y':
            self.mouse.move(0, floor(normalised_value))
        elif action == 'MOUSE_MOVE_-Y':
            self.mouse.move(0, ceil(normalised_value))
        else:
            raise Exception('Invalid mouse axis.')

    def detect_button_press(self):
        for button in self.buttons:
            if self.api.is_button_press(button):
                self.handle_input(button)
            elif self.is_pressed(button):
                self.release_mouse(button)
                self.release_key(button)

    def handle_trigger_press(self, trigger='LEFT_TRIGGER'):
        if self.api.is_trigger_pressed(trigger):
            self.handle_input(trigger)
            self._is_pressed[trigger] = True
        elif self.is_pressed(trigger):
            self.release_mouse(trigger)
            self.release_key(trigger)

    def handle_triggers_press(self):
        self.handle_trigger_press()
        self.handle_trigger_press('RIGHT_TRIGGER')


# TODO: validate profile at startup
# TODO: handle hot plug (print a msg)
if __name__ == '__main__':
    gamepad = Gamepad.from_profile()
    print('XBox Controller Mapper has started. Press Ctrl+C to stop.')
    while True:
        gamepad.run()
        sleep(float(gamepad.config['general']['DELAY']))
