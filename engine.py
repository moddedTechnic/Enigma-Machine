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
	USER_EVENT as EVENT_USER,
	AUDIODEVICEADDED as EVENT_AUDIO_DEVICE_ADDED, AUDIODEVICEREMOVED as EVENT_AUDIO_DEVICE_REMOVED,
	FINGERMOTION as EVENT_FINGER_MOTION, FINGERDOWN as EVENT_FINGER_DOWN, FINGERUP as EVENT_FINGER_UP,
	MULTIGESTURE as EVENT_MULTIGESTURE,
	TEXTEDITING as EVENT_TEXT_EDITING, TEXTINPUT as EVENT_TEXT_INPUT,
	DROPBEGIN as EVENT_DROP_BEGIN, DROPCOMPLETE as EVENT_DROP_COMPLETE, DROPFILE as EVENT_DROP_FILE, DROPTEXT as EVENT_DROP_TEXT,
	MIDIIN as EVENT_MIDI_IN, MIDIOUT as EVENT_MIDI_OUT,
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
	EVENT_MIDI_IN, EVENT_MIDI_OUT,
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

fonts = {}
def Font(family, size = None):
	if size is None:
		font = family
	else:
		font = family, size

	if (family, size) in fonts:
		return fonts[family, size]

	f = _Font(family, size)
	fonts[font] = f
	return f

class Engine():
	TOP     = 0b000001
	CENTERv = 0b000010
	BOTTOM  = 0b000100
	LEFT    = 0b001000
	CENTERh = 0b010000
	RIGHT   = 0b100000

	TOP_LEFT,    TOP_CENTER,    TOP_RIGHT    = TOP | LEFT,     TOP | CENTERv,     TOP | RIGHT
	CENTER_LEFT, CENTER_CENTER, CENTER_RIGHT = CENTERh | LEFT, CENTERh | CENTERv, CENTERh | RIGHT
	BOTTOM_LEFT, BOTTOM_CENTER, BOTTOM_RIGHT = BOTTOM | LEFT,  BOTTOM | CENTERv,  BOTTOM | RIGHT

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

		self.setup()

	def __call__(self):
		self.running = True
		while self.running:
			for event in get_events():
				for listener in self.event_listeners[event]:
					d = event.dict
					if 'pos' in event.dict:
						d['pos'] = Vector2(d['pos'])
					listener(**d)

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
