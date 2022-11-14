from pygame import (
	init as pg_init,
	gfxdraw as draw,
	draw as _draw,
)
draw.filled_rectangle = lambda surface, rect, colour: _draw.rect(surface, colour, rect)
from pygame.constants import (
	QUIT as EVENT_QUIT,
	MOUSEWHEEL as EVENT_MOUSE_WHEEL,
	MOUSEBUTTONDOWN as EVENT_MOUSE_BUTTON_DOWN, MOUSEBUTTONUP as EVENT_MOUSE_BUTTON_UP, MOUSEMOTION as EVENT_MOUSE_MOTION,
	ACTIVEEVENT as EVENT_ACTIVE,
	KEYDOWN as EVENT_KEY_DOWN, KEYUP as EVENT_KEY_UP,
	JOYAXISMOTION as EVENT_JOY_AXIS_MOTION, JOYBALLMOTION as EVENT_JOY_BALL_MOTION, JOYHATMOTION as EVENT_JOY_HAT_MOTION,
	JOYBUTTONUP as EVENT_JOY_BUTTON_UP, JOYBUTTONDOWN as EVENT_JOY_BUTTON_DOWN,
	VIDEORESIZE as EVENT_VIDEO_RESIZE, VIDEOEXPOSE as EVENT_VIDEO_EXPOSE,
	USEREVENT as EVENT_USER,
	AUDIODEVICEADDED as EVENT_AUDIO_DEVICE_ADDED, AUDIODEVICEREMOVED as EVENT_AUDIO_DEVICE_REMOVED,
	FINGERMOTION as EVENT_FINGER_MOTION, FINGERDOWN as EVENT_FINGER_DOWN, FINGERUP as EVENT_FINGER_UP,
	MULTIGESTURE as EVENT_MULTIGESTURE,
	TEXTEDITING as EVENT_TEXT_EDITING, TEXTINPUT as EVENT_TEXT_INPUT,
	DROPBEGIN as EVENT_DROP_BEGIN, DROPCOMPLETE as EVENT_DROP_COMPLETE, DROPFILE as EVENT_DROP_FILE, DROPTEXT as EVENT_DROP_TEXT,
)
events = [
	EVENT_QUIT,
	EVENT_MOUSE_WHEEL,
	EVENT_MOUSE_BUTTON_DOWN, EVENT_MOUSE_BUTTON_UP, EVENT_MOUSE_MOTION,
	EVENT_ACTIVE,
	EVENT_KEY_DOWN, EVENT_KEY_UP,
	EVENT_JOY_AXIS_MOTION, EVENT_JOY_BALL_MOTION, EVENT_JOY_HAT_MOTION, EVENT_JOY_BUTTON_UP, EVENT_JOY_BUTTON_DOWN,
	EVENT_VIDEO_RESIZE, EVENT_VIDEO_EXPOSE,
	EVENT_USER,
	EVENT_AUDIO_DEVICE_ADDED, EVENT_AUDIO_DEVICE_REMOVED,
	EVENT_FINGER_MOTION, EVENT_FINGER_DOWN, EVENT_FINGER_UP,
	EVENT_MULTIGESTURE,
	EVENT_TEXT_EDITING, EVENT_TEXT_INPUT,
	EVENT_DROP_BEGIN, EVENT_DROP_COMPLETE, EVENT_DROP_FILE, EVENT_DROP_TEXT,
]
from pygame.display import (
	set_mode as set_size,
	set_caption as set_title,
	update as update_display,
)
from pygame.font import (
	Font as _Font
)
from pygame.time import (
	Clock,
)
from pygame.event import (
	get as get_events,
)

from vector import Vector2


def get_from_dict(d, k, default = None):
	return d[k] if k in d else default

def get_first_from_dict(d, *ks, default = None):
	for k in ks:
		v = get_from_dict(d, k)
		if v is not None:
			return v
	return default

colours = {}
def Colour(c):
	colour = c
	if type(c) == int:
		if c in colours:
			return colours[c]

		r = (c & 0xff0000) >> 16
		g = (c & 0x00ff00) >> 8
		b = c & 0x0000ff
		colour = r, g, b
		colours[c] = colour

	return colour

def rgb(r, g, b):
	return Colour((r << 16) | (g << 8) | b)

fonts = {}
def Font(family, size = None):
	if size is None:
		font = family
	else:
		font = family, size

	if font in fonts:
		return fonts[font]

	f = _Font(*font)
	fonts[font] = f
	return f

class Engine():
	TOP     = 0b000001
	CENTERv = 0b000010
	BOTTOM  = 0b000100
	LEFT    = 0b001000
	CENTERh = 0b010000
	RIGHT   = 0b100000

	TOP_LEFT,    TOP_CENTER,    TOP_RIGHT    = TOP | LEFT,     TOP | CENTERh,     TOP | RIGHT
	CENTER_LEFT, CENTER_CENTER, CENTER_RIGHT = CENTERv | LEFT, CENTERv | CENTERh, CENTERv | RIGHT
	BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT = BOTTOM | LEFT,  BOTTOM | CENTERh,  BOTTOM | RIGHT

	LEFT_MOUSE  = 1
	RIGHT_MOUSE = 3

	def __init__(self, **kwargs):

		pg_init()

		self.width  = get_from_dict(kwargs, 'width',  720)
		self.height = get_from_dict(kwargs, 'height', 640)
		self.size = Vector2(self.width, self.height)
		self.display = set_size(self.size.tuple(int))

		self.title = get_from_dict(kwargs, 'title', 'New Window')
		set_title(self.title)

		self.clock = Clock()
		self.running = False

		self.event_listeners = {}
		for event in events:
			self.event_listeners[event] = []
		self.add_event_listener(EVENT_QUIT, self.on_quit)

		self.translation = Vector2()
		self.translations = []
		# self.scale = 1 # TODO: add scale

		self.setup()
		self()

	def __call__(self):
		self.running = True
		while self.running:
			for event in get_events():
				if event.type in self.event_listeners:
					for listener in self.event_listeners[event.type]:
						d = event.dict
						if 'pos' in event.dict:
							d['pos'] = Vector2(d['pos'])
						listener(**d)

			self.display.fill(Colour(0))
			self.loop()

			update_display()
			self.clock.tick()

	def setup(self):
		raise NotImplementedError('`setup` must be implemented by apps')

	def loop(self):
		raise NotImplementedError('`loop` must be implemented by apps')

	def add_event_listener(self, event, cb):
		self.event_listeners[event].append(cb)

	def on_quit(self):
		self.running = False

	@staticmethod
	def get_Colour(kwargs, *args):
		c = get_first_from_dict(kwargs, *args)
		c = Colour(c) if c is not None else None
		return c

	@staticmethod
	def get_Vector2(kwargs, *args):
		v = get_first_from_dict(kwargs, *args)
		v = Vector2(v) if v is not None else None
		return v

	@staticmethod
	def get_Font(kwargs, *args):
		f = get_first_from_dict(kwargs, *args)
		f = Font(f) if f is not None else None
		return f

	@staticmethod
	def get_c(kwargs):
		c = Engine.get_Colour(kwargs, 'c', 'col', 'color', 'colour')
		return c

	@staticmethod
	def get_outline(kwargs):
		c = Engine.get_Colour(kwargs, 'outline')
		c = c if c is not None else Engine.get_c(kwargs)
		return c

	@staticmethod
	def get_background(kwargs):
		c = Engine.get_Colour(kwargs, 'bg', 'background')
		return c

	@staticmethod
	def get_bg(kwargs):
		return Engine.get_background(kwargs)

	def get_pos(self, kwargs):
		pos = Engine.get_Vector2(kwargs, 'pos')
		return pos + self.translation

	@staticmethod
	def get_size(kwargs):
		size = Engine.get_Vector2(kwargs, 'size')
		return size

	@staticmethod
	def get_scaled(kwargs):
		scaled = get_first_from_dict(kwargs, 'scaled', default=False)
		return scaled

	@staticmethod
	def get_font(kwargs):
		f = Engine.get_Font(kwargs, 'f', 'font')
		return f

	@staticmethod
	def get_alignment(kwargs):
		horiz_align = get_from_dict(kwargs, 'horiz_align', default=Engine.CENTERh)
		vert_align = get_from_dict(kwargs, 'vert_align', default=Engine.CENTERv)
		align = get_from_dict(kwargs, 'align', default=horiz_align | vert_align)
		return align

	def __scale(self, *args, scaled = False):
		s = self.size if not scaled else 1
		if len(args) == 1:
			return args[0] * s
		return [ a * s for a in args ]

	@staticmethod
	def not_None(**args):
		nones = [ k for k, v in args.items() if v is None ]
		if len(nones) > 0:
			raise ValueError('Must provide values for ' + str(nones)[1:-1].replace('\'', ''))

	@staticmethod
	def align(size, alignment):
		align = alignment
		s = Vector2(size)
		w, h = s.tuple()
		pos = Vector2()

		if align & Engine.TOP != 0:
			pos += (0, h/2)
		elif align & Engine.CENTERv != 0:
			pos -= (0, 0)
		elif align & Engine.BOTTOM != 0:
			pos -= (0, h/2)

		if align & Engine.LEFT != 0:
			pos += (w/2, 0)
		elif align & Engine.CENTERh != 0:
			pos -= (0, 0)
		elif align & Engine.RIGHT != 0:
			pos -= (w/2, 0)

		return pos

	@staticmethod
	def render_text(text, **kwargs):
		f = Engine.get_font(kwargs)
		c = Engine.get_c(kwargs)
		bg = Engine.get_bg(kwargs)

		Engine.not_None(font=f, colour=c)

		text_surface = f.render(text, True, c, bg)
		text_rect = text_surface.get_rect()
		return text_surface, text_rect


	def filled_rectangle(self, **kwargs):
		c = self.get_c(kwargs)
		pos = self.get_pos(kwargs)
		size = self.get_size(kwargs)
		outline = self.get_outline(kwargs)
		scaled = self.get_scaled(kwargs)

		self.not_None(colour=c, position=pos, size=size)

		pos, size = self.__scale(pos, size, scaled=scaled)

		draw.filled_rectangle(
			self.display,
			( *(pos.tuple(int)), *(size.tuple(int)) ),
			c
		)

		self.rectangle(
			c=outline, pos=pos, size=size, scaled = True
		)

	def rectangle(self, **kwargs):
		c = self.get_c(kwargs)
		pos = self.get_pos(kwargs)
		size = self.get_size(kwargs)
		scaled = self.get_scaled(kwargs)

		self.not_None(colour=c, position=pos, size=size)

		pos, size = self.__scale(pos, size, scaled=scaled)

		draw.rectangle(
			self.display,
			( *(pos.tuple(int)), *(size.tuple(int)) ),
			c
		)

	def filled_circle(self, **kwargs):
		c = self.get_c(kwargs)
		pos = self.get_pos(kwargs)
		r = get_first_from_dict(kwargs, 'r', 'radius')
		outline = self.get_outline(kwargs)
		scaled = self.get_scaled(kwargs)

		
		self.not_None(colour=c, position=pos, radius=r)

		pos, r = self.__scale(pos, r, scaled=scaled)
		r = int(r)

		draw.filled_circle(
			self.display,
			*(pos.tuple(int)),
			r,
			c
		)

		self.circle(
			c=outline, pos=pos, r=r, scaled = True
		)

	def circle(self, **kwargs):
		c = self.get_c(kwargs)
		pos = self.get_pos(kwargs)
		r = get_first_from_dict(kwargs, 'r', 'radius')
		scaled = self.get_scaled(kwargs)
		
		self.not_None(colour=c, position=pos, radius=r)

		pos, r = self.__scale(pos, r, scaled=scaled)
		r = int(r)

		draw.filled_circle(
			self.display,
			*(pos.tuple(int)),
			r,
			c
		)

	def line(self, **kwargs):
		c = self.get_c(kwargs)
		a = self.get_Vector2(kwargs, 'a')
		b = self.get_Vector2(kwargs, 'b')
		scaled = self.get_scaled(kwargs)

		self.not_None(colour=c, a=a, b=b)

		a, b = self.__scale(a, b, scaled=scaled)

		draw.line(self.display, *a.tuple(int), *b.tuple(int), c)

	def text(self, text, **kwargs):
		pos = self.get_pos(kwargs)
		align = self.get_alignment(kwargs)
		scaled = self.get_scaled(kwargs)

		pos = self.__scale(pos, scaled=scaled)

		text_surface, text_rect = self.render_text(text, **kwargs)
		pos += self.align(text_rect.size, align)
		text_rect.center = pos.tuple(int)

		self.display.blit(text_surface, text_rect)

	def translate(self, xOff, yOff=None):
		self.translation += Vector2(xOff, yOff)

	def push(self):
		self.translations.append(self.translation)

	def pop(self):
		if len(self.translations) > 0:
			self.translation = self.translations.pop()
