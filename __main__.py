from pygame import (
	init as pg_init,
	QUIT as EVENT_QUIT,
	gfxdraw as draw,
	draw as _draw,
	MOUSEBUTTONDOWN as EVENT_MOUSE_BUTTON_DOWN,
)
draw.filled_rectangle = lambda surface, rect, colour: _draw.rect(surface, colour, rect)
from pygame.display import (
	set_mode as set_size,
	set_caption as set_title,
	update as update_display,
)
from pygame.font import (
	Font
)
from pygame.time import (
	Clock,
)
from pygame.event import (
	get as get_events,
)

from vector import Vector2


class App:
	CENTER = 0

	def __init__(self):
		pg_init()

		self.width = 800
		self.height = 600
		self.size = Vector2(self.width, self.height)
		self.display = set_size(self.size.tuple(int))

		set_title('Enigma Machine')

		self.clock = Clock()

		self.letters = [
			{ 'letter': l, 'lit': False }
			for l in [
				'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O',
				  'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K',
				'P', 'Y', 'X', 'C', 'V', 'B', 'N', 'M', 'L',
			]
		]

		self()

	def __call__(self):
		self.running = True
		while self.running:
			for event in get_events():
				t = event.type
				d = event.dict
				if t == EVENT_QUIT:
					self.running = False
				elif t == EVENT_MOUSE_BUTTON_DOWN:
					print(Vector2(d['pos']))
				else:
					print(event)

			self.render_keyboard()

			update_display()
			self.clock.tick(60)

	def render_keyboard(self):
		self.rect(0xe17055, (0.1, 0.1), (0.8, 0.8))
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
		
		self.circle(c, (x, y), 0.04, outline=0xdfe6e9)
		self.text(l['letter'], ('res/Montserrat-Medium.ttf', 16), 0x2d3436, (x, y))
	
		y += .32
		self.circle(0x2d3436, (x, y), 0.04, outline=0xdfe6e9)
		self.text(l['letter'], ('res/Montserrat-Medium.ttf', 24), 0xdfe6e9, (x, y))

	@staticmethod
	def process_colour(c):
		if type(c) == int:
			r = (c & 0xff0000) >> 16
			g = (c & 0x00ff00) >> 8
			b = (c & 0x0000ff)
			c = (r, g, b)

		return c

	def rect(self, c, pos, size):
		c = App.process_colour(c)
		pos = Vector2(pos) * self.size
		size = Vector2(size) * self.size

		draw.filled_rectangle(
			self.display,
			( *(pos.tuple(int)), *(size.tuple(int)) ),
			c
		)

	def circle(self, c, pos, r, outline = 0):
		c = App.process_colour(c)
		outline = App.process_colour(outline)
		pos = Vector2(pos) * self.size
		r *= min(self.width, self.height)

		draw.filled_circle(self.display, *pos.tuple(int), int(r), c)
		draw.aacircle(self.display, *pos.tuple(int), int(r), outline)

	def text(self, text, f, c, pos, draw_mode = CENTER):
		f = Font(*f)
		c = App.process_colour(c)
		pos = Vector2(pos) * self.size

		text_surface = f.render(text, True, c)
		text_rect = text_surface.get_rect()
		
		if draw_mode == App.CENTER:
			text_rect.center = pos.tuple(int)
		else:
			text_rect.center = (pos + Vector2(text_rect.size) / 2).tuple(int)

		self.display.blit(text_surface, text_rect)

if __name__ == '__main__':
	from os import system
	system('cls')
	App()
