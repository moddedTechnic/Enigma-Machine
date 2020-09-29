from pygame.constants import (
	MOUSEBUTTONDOWN as EVENT_MOUSE_BUTTON_DOWN, MOUSEBUTTONUP as EVENT_MOUSE_BUTTON_UP,
)

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

		nums = range(len(self.letters))
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

		self.active_rotors = [
			self.rotors['III'],
			self.rotors['VII'],
			self.rotors['II'],
		]

		self.reflectors = {
			'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
			'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
			'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
		}
		for k, v in self.reflectors.items():
			self.reflectors[k] = [ ord(c) - 65 for c in v ]

		self.reflector = self.reflectors['B']

		self.plugboard = {
			A: W,
			B: F,
			C: K,
			D: O,
		}
		plugboard = self.plugboard.copy()

		for v, k in self.plugboard.items():
			plugboard[k] = v

		self.plugboard = plugboard.copy()

	def loop(self):
		self.render_keyboard()

	def render_keyboard(self):
		self.filled_rectangle(c=0xe17055, pos=(0.1, 0.1), size=(0.8, 0.8))
		for i in range(9):
			self.render_button(Vector2(0.14 + i * 0.09, 0.16), i)
		for i in range(8):
			self.render_button(Vector2(0.185 + i * 0.09, 0.245), i + 9)
		for i in range(9):
			self.render_button(Vector2(0.14 + i * 0.09, 0.33), i + 17)

		self.filled_rectangle(c=0xfab1a0, pos=(0.14, 0.75), size=(0.72, 0.1))
		self.text('Plugboard', f=('res/Montserrat-Medium.ttf', 16), c=0, pos=(0.2, 0.8), align=self.CENTER_LEFT)

	def render_button(self, pos, idx):
		x, y = Vector2(pos).tuple(float)
		l = self.letters[idx]

		c = 0xfdcb6e if l['lit'] else 0xdfe6e9
		
		self.circle(c=c, pos=(x, y), r=0.04, outline=0xdfe6e9)
		self.text(l['letter'], font=('res/Montserrat-Medium.ttf', 16), c=0x2d3436, pos=(x, y))
	
		y += .32
		c = 0x2d3436 if l['pressed'] else 0x636e72
		self.circle(c=c, pos=(x, y), r=0.04, outline=0xdfe6e9)
		self.text(l['letter'], font=('res/Montserrat-Medium.ttf', 24), c=0xdfe6e9, pos=(x, y))

	def on_mouse_down(self, pos, button, window):
		if button == Engine.LEFT_MOUSE:
			b = self.get_button_pressed(pos)
			if b != -1:
				self.letters[b]['pressed'] = True
				self.encrypt(b)

	def on_mouse_up(self, pos, button, window):
		if button == Engine.LEFT_MOUSE:
			for i in range(len(self.letters)):
				self.letters[i]['pressed'] = False
				self.letters[i]['lit'] = False
			self.rotate()

	def get_button_pressed(self, pos):
		r = (0.04 * min(*self.size.tuple())) ** 2

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

		return -1

	def encrypt(self, letter):
		output = letter
		
		# pass through rotors
		for r in self.active_rotors:
			output += r[output]
			output %= len(self.letters)

		# reflector
		output = self.reflector[output]

		# # pass through rotors
		for r in self.active_rotors:
			output += r.index(output)
			output %= len(self.letters)

		if output in self.plugboard.keys():
			output = self.plugboard[output]

		self.letters[output]['lit'] = True
		print(self.letters[output]['letter'])

	def rotate(self):
		for i, r in enumerate(self.active_rotors):
			new_rotor = [ 0 for _ in range(len(r)) ]
			for j in range(len(r)):
				new_rotor[j] = r[(j + 1) % len(r)]
			self.active_rotors[i] = new_rotor


if __name__ == '__main__':
	from os import system
	system('cls')
	# App(width=1920 // 1.25, height=1080 // 1.25, title='Engima Machine')
	App(width=800, height=600, title='Engima Machine')
