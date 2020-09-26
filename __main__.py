from pygame import (
	init as pg_init,
	QUIT as pg_QUIT,
	gfxdraw as draw,
	draw as _draw,
)
draw.filled_rectangle = lambda surface, rect, colour: _draw.rect(surface, colour, rect)
from pygame.display import (
	set_mode as set_size,
	set_caption as set_title,
	update as update_display,
)
from pygame.time import (
	Clock,
)
from pygame.event import (
	get as get_events,
)

from vector import Vector2


class App:
	def __init__(self):
		pg_init()

		self.width = 800
		self.height = 600
		self.size = Vector2(self.width, self.height)
		self.display = set_size(self.size.tuple(int))

		set_title('Enigma Machine')

		self.clock = Clock()

		self.letters = {
			
		}

		self()

	def __call__(self):
		self.running = True
		while self.running:
			for event in get_events():
				if event.type == pg_QUIT:
					self.running = False
				else:
					print(event)

			self.render_keyboard()

			update_display()
			self.clock.tick(60)

	def render_keyboard(self):
		self.rect(0xe17055, (0.1, 0.1), (0.8, 0.8))
		for i in range(10):
			self.render_button(Vector2(0.14 + i * 0.08, 0.16))
		for i in range(9):
			self.render_button(Vector2(0.18 + i * 0.08, 0.36))
		for i in range(7):
			self.render_button(Vector2(0.22 + i * 0.08, 0.56))

	def render_button(self, pos):
		x, y = Vector2(pos).tuple(float)
	
		self.circle(0xfefefe, (x, y), 0.04)
		self.circle(0xfefefe, (x, y + 0.09), 0.04)

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
		pos = Vector2(pos)
		size = Vector2(size)

		draw.filled_rectangle(
			self.display,
			( *((pos * self.size).tuple(int)), *((size * self.size).tuple(int)) ),
			c
		)

	def circle(self, c, pos, r):
		c = App.process_colour(c)
		pos = Vector2(pos) * self.size
		r *= min(self.width, self.height)

		draw.filled_circle(self.display, *pos.tuple(int), int(r), c)
		draw.aacircle(self.display, *pos.tuple(int), int(r), App.process_colour(0))

if __name__ == '__main__':
	App()
