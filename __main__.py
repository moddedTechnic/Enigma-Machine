from pygame.constants import (
	MOUSEBUTTONDOWN as EVENT_MOUSE_BUTTON_DOWN,
)

from vector import Vector2


from engine import Engine

class App(Engine):
	def setup(self):
		self.add_event_listener(EVENT_MOUSE_BUTTON_DOWN, self.on_mouse_down)

		self.letters = [
			{ 'letter': l, 'lit': False }
			for l in [
				'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O',
				  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K',
				'P', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', 'L',
			]
		]

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

	def render_button(self, pos, idx):
		x, y = Vector2(pos).tuple(float)
		l = self.letters[idx]

		c = 0xfdcb6e if l['lit'] else 0xdfe6e9
		
		self.circle(c=c, pos=(x, y), r=0.04, outline=0xdfe6e9)
		self.text(l['letter'], font=('res/Montserrat-Medium.ttf', 16), c=0x2d3436, pos=(x, y))
	
		y += .32
		self.circle(c=0x2d3436, pos=(x, y), r=0.04, outline=0xdfe6e9)
		self.text(l['letter'], font=('res/Montserrat-Medium.ttf', 24), c=0xdfe6e9, pos=(x, y))

	def on_mouse_down(self, pos, button, window):
		pass

if __name__ == '__main__':
	from os import system
	system('cls')
	App(width=800, height=600, title='Engima Machine')
