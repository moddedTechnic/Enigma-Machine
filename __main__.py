from pygame.constants import (
	MOUSEBUTTONDOWN as EVENT_MOUSE_BUTTON_DOWN, MOUSEBUTTONUP as EVENT_MOUSE_BUTTON_UP,
)

from pygame import Rect

from vector import Vector2
from engine import Engine

A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = tuple(range(26))

class App(Engine):
	def setup(self):
		self.add_event_listener(EVENT_MOUSE_BUTTON_DOWN, self.on_mouse_down)
		self.add_event_listener(EVENT_MOUSE_BUTTON_UP, self.on_mouse_up)

		self.letters = [
			{ 'letter': l, 'lit': False, 'pressed': False }
			for l in [
				'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O',
				  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K',
				'P', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', 'L',
			]
		]

		self.rotors = {
			'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
			'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
			'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
			'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
			'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
			'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
			'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
			'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
		}
		for k, v in self.rotors.items():
			self.rotors[k] = [ ord(c) - 65 for c in v ]

		self.active_rotor_keys = [
			'III',
			'VII',
			'II'
		]
		self.active_rotors = []
		self.rebind_rotors()
		self.offsets = [ 0 for _ in range(len(self.active_rotor_keys)) ]

		self.reflectors = {
			'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
			'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
			'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
		}
		self.reflector_keys = list(self.reflectors.keys())
		for k, v in self.reflectors.items():
			self.reflectors[k] = [ ord(c) - 65 for c in v ]

		self.reflector_key = 'B'

		self.plugboard = {}

		self.KEYBOARD  = 0
		self.ROTORS    = 1
		self.PLUGBOARD = 2
		self.REFLECTOR = 3
		self.view = self.KEYBOARD

		self.selected = [ -1, -1 ]

	@property
	def reflector(self):
		return self.reflectors[self.reflector_key]

	def loop(self):
		self.filled_rectangle(c=0xe17055, pos=(0.1, 0.1), size=(0.8, 0.8))

		if self.view == self.KEYBOARD:
			self.render_keyboard()
		elif self.view == self.ROTORS:
			self.render_rotors()
		elif self.view == self.PLUGBOARD:
			self.render_plugboard()
		elif self.view == self.REFLECTOR:
			self.render_reflector()

		self.filled_rectangle(c=0xfab1a0, pos=(0.185, 0.75), size=(0.63, 0.1))
		self.text('Keyboard' if self.view == self.PLUGBOARD else 'Plugboard', f=('res/Montserrat-Medium.ttf', 16), c=0x2d3436, pos=(0.4, 0.8), align=self.CENTER_RIGHT)

		self.filled_rectangle(c=0x2d3436, pos=(0.425, 0.75), size=(0.005, 0.1))
		self.text('Keyboard' if self.view == self.ROTORS else 'Rotors', f=('res/Montserrat-Medium.ttf', 16), c=0x2d3436, pos=(0.5, 0.8), align=self.CENTER_CENTER)

		self.filled_rectangle(c=0x2d3436, pos=(0.57, 0.75), size=(0.005, 0.1))
		self.text('Keyboard' if self.view == self.REFLECTOR else 'Reflector', f=('res/Montserrat-Medium.ttf', 16), c=0x2d3436, pos=(0.6, 0.8), align=self.CENTER_LEFT)

	def render_keyboard(self):
		for i in range(9):
			self.render_button(Vector2(0.14 + i * 0.09, 0.16), i)
		for i in range(8):
			self.render_button(Vector2(0.185 + i * 0.09, 0.245), i + 9)
		for i in range(9):
			self.render_button(Vector2(0.14 + i * 0.09, 0.33), i + 17)

	def render_rotors(self):
		for i, r in enumerate(self.active_rotor_keys):
			_x = 1 / (1 + len(self.active_rotor_keys))
			x = (1 + i) * _x
			self.filled_rectangle(pos=(x - _x / 20, 0.14), size=(_x / 10, .04), c=0xe17055 - 0x1f1f1f)
			self.text('+', f=('res/Montserrat-Medium.ttf', 24), c=0xe17055, pos=(x, 0.16))
			
			self.text(r, f=('res/Montserrat-Medium.ttf', 32), c=0, pos=(x, 0.24))
			
			self.filled_rectangle(pos=(x - _x / 20, 0.3), size=(_x / 10, .04), c=0xe17055 - 0x1f1f1f)
			self.text('-', f=('res/Montserrat-Medium.ttf', 24), c=0xe17055, pos=(x, 0.32))

			self.filled_rectangle(pos=(x - _x / 20, 0.5), size=(_x / 10, .04), c=0xe17055 - 0x1f1f1f)
			self.text('+', f=('res/Montserrat-Medium.ttf', 24), c=0xe17055, pos=(x, 0.52))

			self.text(chr((self.active_rotors[i][0] + self.offsets[self.active_rotor_keys.index(r)]) % len(self.letters) + 65), f=('res/Montserrat-Medium.ttf', 32), c=0, pos=(x, 0.6))

			self.filled_rectangle(pos=(x - _x / 20, 0.66), size=(_x / 10, .04), c=0xe17055 - 0x1f1f1f)
			self.text('-', f=('res/Montserrat-Medium.ttf', 24), c=0xe17055, pos=(x, 0.68))

	def render_plugboard(self):
		for i in range(9):
			self.render_button(Vector2(0.14 + i * 0.09, 0.16), i, True)
		for i in range(8):
			self.render_button(Vector2(0.185 + i * 0.09, 0.33), i + 9, True)
		for i in range(9):
			self.render_button(Vector2(0.14 + i * 0.09, 0.5), i + 17, True)

		self.draw_connected()

	def render_reflector(self):
		self.filled_rectangle(pos=(0.48, 0.14), size=(0.04, .04), c=0xe17055 - 0x1f1f1f)
		self.text('+', f=('res/Montserrat-Medium.ttf', 24), c=0xe17055, pos=(0.5, 0.16))
		
		self.text(self.reflector_key, f=('res/Montserrat-Medium.ttf', 32), c=0, pos=(0.5, 0.24))
		
		self.filled_rectangle(pos=(0.48, 0.3), size=(0.04, .04), c=0xe17055 - 0x1f1f1f)
		self.text('-', f=('res/Montserrat-Medium.ttf', 24), c=0xe17055, pos=(0.5, 0.32))

	def render_button(self, pos, idx, together=False):
		x, y = Vector2(pos).tuple(float)
		l = self.letters[idx]

		c = 0xfdcb6e if l['lit'] else 0xdfe6e9
		
		self.circle(c=c, pos=(x, y), r=0.04, outline=0xdfe6e9)
		self.text(l['letter'], font=('res/Montserrat-Medium.ttf', 16), c=0x2d3436, pos=(x, y), align=self.CENTER_CENTER) if not together else None
	
		y += .09 if together else .32
		c = 0x2d3436 if l['pressed'] else 0x636e72
		self.circle(c=c, pos=(x, y), r=0.04, outline=0xdfe6e9)
		self.text(l['letter'], font=('res/Montserrat-Medium.ttf', 24), c=0xdfe6e9, pos=(x, y), align=self.CENTER_CENTER)

	def on_mouse_down(self, pos, button, window, touch):
		if button == Engine.LEFT_MOUSE:
			if self.view == self.KEYBOARD:
				b = self.get_button_pressed(pos)
				if b != -1:
					self.letters[b]['pressed'] = True
					self.encrypt(b)
					return

			elif self.view == self.PLUGBOARD:
				s = self.get_button_pressed(pos)
				self.selected[0] = s if s != -1 else self.selected[0]

			elif self.view == self.ROTORS:
				for i, r in enumerate(self.active_rotor_keys):
					_x = 1 / (1 + len(self.active_rotor_keys))
					x = (1 + i) * _x
					if Rect(*((x - _x / 20, 0.14) * self.size).tuple(int), *((_x / 10, .04) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
						self.active_rotor_keys[i] = self.advance(r)
						self.rebind_rotors()
					if Rect(*((x - _x / 20, 0.3) * self.size).tuple(int), *((_x / 10, .04) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
						self.active_rotor_keys[i] = self.decrease(r)

					if Rect(*((x - _x / 20, 0.5) * self.size).tuple(int), *((_x / 10, .04) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
						self._rotate(r)
					if Rect(*((x - _x / 20, 0.66) * self.size).tuple(int), *((_x / 10, .04) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
						self._rotate(r)

			elif self.view == self.REFLECTOR:
				if Rect(*((0.48, 0.14) * self.size).tuple(int), *((0.04, .04) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
					self.advance_reflector()
				if Rect(*((0.48, 0.3) * self.size).tuple(int), *((0.04, .04) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
					self.deadvance_reflector()

			if Rect(*((0.185, 0.75) * self.size).tuple(int), *((0.225, 0.1) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
				self.view = self.PLUGBOARD if self.view != self.PLUGBOARD else self.KEYBOARD

			elif Rect(*((0.415, 0.75) * self.size).tuple(int), *((0.185, 0.1) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
				self.view = self.ROTORS if self.view != self.ROTORS else self.KEYBOARD

			elif Rect(*((0.605, 0.75) * self.size).tuple(int), *((0.21, 0.1) * self.size).tuple(int)).collidepoint(pos.tuple(int)):
				self.view = self.REFLECTOR if self.view != self.REFLECTOR else self.KEYBOARD

	def on_mouse_up(self, pos, button, window, touch):
		if self.view == self.KEYBOARD:
			if button == Engine.LEFT_MOUSE:
				for i in range(len(self.letters)):
					self.letters[i]['pressed'] = False
					self.letters[i]['lit'] = False
				self.rotate()

		if self.view == self.PLUGBOARD:
			s = self.get_button_pressed(pos)
			self.selected[1] = s if s != -1 else self.selected[1]
			if -1 not in self.selected and self.selected[0] != self.selected[1]:
				self.connect()

	def get_button_pressed(self, pos):
		r = (0.04 * min(*self.size.tuple())) ** 2

		if self.view == self.KEYBOARD:
			for i in range(9):
				key_pos = Vector2(0.14 + i * 0.09, 0.48) * self.size
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i
				
			for i in range(8):
				key_pos = Vector2(0.185 + i * 0.09, 0.565) * self.size
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i + 9

			for i in range(9):
				key_pos = Vector2(0.14 + i * 0.09, 0.65) * self.size
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i + 17

		elif self.view == self.PLUGBOARD:
			for i in range(9):
				key_pos = Vector2(0.14 + i * 0.09, 0.16) * self.size
				self.circle(c=0xff0000, pos=key_pos, r=0.04, scaled=True)
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i
				key_pos = Vector2(0.14 + i * 0.09, 0.25) * self.size
				self.circle(c=0xff0000, pos=key_pos, r=0.04, scaled=True)
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i
				
			for i in range(8):
				key_pos = Vector2(0.185 + i * 0.09, 0.33) * self.size
				self.circle(c=0x00ff00, pos=key_pos, r=0.04, scaled=True)
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i + 9
				key_pos = Vector2(0.185 + i * 0.09, 0.42) * self.size
				self.circle(c=0x00ff00, pos=key_pos, r=0.04, scaled=True)
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i + 9

			for i in range(9):
				key_pos = Vector2(0.14 + i * 0.09, 0.5) * self.size
				self.circle(c=0x0000ff, pos=key_pos, r=0.04, scaled=True)
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i + 17
				key_pos = Vector2(0.14 + i * 0.09, 0.59) * self.size
				self.circle(c=0x0000ff, pos=key_pos, r=0.04, scaled=True)
				d = (key_pos - pos).mag_sq()
				if d < r:
					return i + 17

		return -1

	def encrypt(self, letter):
		output = letter
		
		# pass through rotors
		for r in self.active_rotors:
			output += r[(output + self.offsets[self.active_rotors.index(r)]) % len(self.letters)]
			output %= len(self.letters)

		# reflector
		output = self.reflector[output]

		# # pass through rotors
		for r in self.active_rotors:
			output += r.index((output + self.offsets[self.active_rotors.index(r)]) % len(self.letters))
			output %= len(self.letters)

		if output in self.plugboard.keys():
			output = self.plugboard[output]

		self.letters[output]['lit'] = True
		print(self.letters[output]['letter'])

	def rotate(self):
		for r in self.active_rotor_keys:
			self._rotate(r)

	def _rotate(self, r):
		self.offsets[self.active_rotor_keys.index(r)] += 1
		self.offsets[self.active_rotor_keys.index(r)] %= 26

	def _derotate(self, r):
		self.offsets[self.active_rotor_keys.index(r)] -= 1
		self.offsets[self.active_rotor_keys.index(r)] %= 26

	def connect(self):
		disconnect = False
		if self.selected[0] in self.plugboard.keys():
			disconnect = self.plugboard[self.selected[0]] == self.selected[1]
			self.plugboard.pop(self.plugboard[self.selected[0]])
			self.plugboard.pop(self.selected[0])
		if self.selected[1] in self.plugboard.keys():
			self.plugboard.pop(self.plugboard[self.selected[1]])
			self.plugboard.pop(self.selected[1])
			
		if not disconnect:
			self.plugboard[self.selected[0]] = self.selected[1]
			self.plugboard[self.selected[1]] = self.selected[0]

		self.selected = [-1, -1]

	def draw_connected(self):
		for k, v in self.plugboard.items():
			row: int
			col: int
			if k < 9:
				row = 0
				col = k
			elif k < 17:
				row = 1
				col = k - 9
			else:
				row = 2
				col = k - 17

			x1 = (0.14 if not (9 <= k and k <= 16) else 0.185) + col * 0.09
			y1 = 0.17 * row + 0.16

			if v < 9:
				row = 0
				col = v
			elif v < 17:
				row = 1
				col = v - 9
			else:
				row = 2
				col = v - 17

			x2 = (0.14 if not (9 <= v and v <= 16) else 0.185) + col * 0.09
			y2 = 0.17 * row + 0.16

			self.line(a=(x1 - 0.001, y1        ), b=(x2 + 0.001, y2        ), c=0)
			self.line(a=(x1,         y1 - 0.001), b=(x2,         y2 + 0.001), c=0)
			self.line(a=(x1,         y1        ), b=(x2,         y2        ), c=0)
			self.line(a=(x1 + 0.001, y1        ), b=(x2 - 0.001, y2        ), c=0)
			self.line(a=(x1,         y1 + 0.001), b=(x2,         y2 - 0.001), c=0)

	def rebind_rotors(self):
		self.active_rotors = [ self.rotors[r] for r in self.active_rotor_keys ]

	def advance(self, r):
		rotors = list(self.rotors.keys())
		res = rotors[(rotors.index(r) + 1) % len(rotors)]
		return (res if res not in self.active_rotor_keys else self.advance(res))

	def decrease(self, r):
		rotors = list(self.rotors.keys())
		res = rotors[(rotors.index(r) - 1) % len(rotors)]
		return (res if res not in self.active_rotor_keys else self.decrease(res))

	def advance_reflector(self):
		self.reflector_key = self.reflector_keys[(self.reflector_keys.index(self.reflector_key) + 1) % len(self.reflector_keys)]

	def deadvance_reflector(self):
		self.reflector_key = self.reflector_keys[(self.reflector_keys.index(self.reflector_key) - 1) % len(self.reflector_keys)]


if __name__ == '__main__':
	from os import system
	system('cls')
	# App(width=1920 // 1.25, height=1080 // 1.25, title='Engima Machine')
	App(width=800, height=600, title='Engima Machine')
