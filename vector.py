from math import sqrt

class Vector2:
	def __init__(self, x=0, y=0):
		if type(x) in (tuple, list):
			x, y = x
			
		elif type(x) == Vector2:
			x, y = x.tuple()

		self.x = x
		self.y = y

	def tuple(self, t=float):
		return t(self.x), t(self.y)

	def copy(self):
		return Vector2(self.x, self.y)

	def __str__(self):
		return f'({self.x},{self.y})'

	@staticmethod
	def to_vector(other):
		if type(other) in (int, float):
			return Vector2(other, other)
		return other

	def __add__(self, other):
		v = self.copy()
		v += other
		return v

	def __radd__(self, other):
		return self + other

	def __iadd__(self, other):
		other = Vector2.to_vector(other)

		self.x += other.x
		self.y += other.y
		return self

	def __sub__(self, other):
		return self + (-other)

	def __rsub__(self, other):
		return other + (-self)

	def __isub__(self, other):
		self += -other
		return self

	def __mul__(self, other):
		v = self.copy()
		v *= other
		return v

	def __rmul__(self, other):
		return self * other

	def __imul__(self, other):
		other = Vector2.to_vector(other)
		self.x *= other.x
		self.y *= other.y
		return self

	def __truediv__(self, other):
		v = self.copy()
		v /= other
		return v

	def __rtruediv__(self, other):
		v = self.copy()
		v.x = 1 / v.x
		v.y = 1 / v.y
		return other * v

	def __itruediv__(self, other):
		other = Vector2.to_vector(other)
		self.x /= other.x
		self.y /= other.y
		return self

	def __floordiv__(self, other):
		v = self.copy()
		v //= other
		return v

	def __rfloordiv__(self, other):
		v = self.copy()
		v.x = 1 // v.x
		v.y = 1 // v.y
		return other * v

	def __ifloordiv__(self, other):
		other = Vector2.to_vector(other)
		self.x //= other.x
		self.y //= other.y
		return self

	def __neg__(self):
		return Vector2(-self.x, -self.y)

	def __pos__(self):
		return Vector2(+self.x, +self.y)

	def __abs__(self):
		return sqrt(self.mag_sq())

	def mag_sq(self):
		return self.x ** 2 + self.y ** 2

Vector2.zero = Vector2()
Vector2.one = Vector2(1, 1)


if __name__ == "__main__":
	v1 = Vector2(1, 2)
	v2 = Vector2(2, 1)
	
	print(v1 // v2)
