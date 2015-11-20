"""Basic linear algebra library streamlined for dynamics applications
"""

import warnings
from math import sqrt, acos, sin, cos
from pyglet import gl

def raw(*args):
	return (gl.GLfloat * len(args))(*args)
	
def frange(start, inc, end=None):
	if end is None:
		end = inc
		inc = 1.
	n = int((end - start) / inc + 1.)
	L = []
	for i in range(n):
		L.append(start + inc * i)
	return L
	
def getMachEps():
	return 7./3 - 4./3 - 1.

class Vec3:
	def __init__(self, x=None, y=None, z=None):
		if x is None:
			self.values = [0,0,0]
		elif y is None:
			self.values = x
		else:
			self.values = [x,y,z]
			
	def __len__(self):
		return 3

	def __str__(self):
		return "[%f, %f, %f]'" % (self.values[0], self.values[1], self.values[2])
		
	def __getitem__(self, index):
		return self.values[index]
		
	def __setitem__(self, index, value):
		self.values[index] = value
		
	def __add__(self, rhs):
		if isinstance(rhs, Vec3):
			return Vec3(self.values[0] + rhs.values[0], self.values[1] + rhs.values[1], self.values[2] + rhs.values[2])
		else:
			return Vec3(self.values[0] + rhs, self.values[1] + rhs, self.values[2] + rhs)

	def __radd__(self, lhs):
		return self + lhs
		
	def __sub__(self, rhs):
		return self + (rhs * -1)
		
	def __rsub__(self, lhs):
		return -1 * self + lhs
		
	def __mul__(self, rhs):
		# Scalar or dot product
		if isinstance(rhs, Vec3):
			return self[0] * rhs[0] + self[1] * rhs[1] + self[2] * rhs[2]
		else:
			return Vec3(rhs * self[0], rhs * self[1], rhs * self[2])
		
	def __rmul__(self, lhs):
		return self * lhs
		
	def __pow__(self, rhs):
		# Cross product
		x = self[1] * rhs[2] - rhs[1] * self[2]
		y = self[2] * rhs[0] - rhs[2] * self[0]
		z = self[0] * rhs[1] - rhs[0] * self[1]
		return Vec3(x,y,z)
		
	def __div__(self, rhs):
		return self * (1.0 / rhs)
		
	def __truediv__(self, rhs):
		return self.__div__(rhs)
		
	def norm(self):
		return sqrt(self * self)
		
	def normalize(self):
		m = self.norm()
		return self / m
		
	def dot(self, rhs):
		return self * rhs
		
	def cross(self, rhs):
		return self ** rhs
		
	def ang(self, rhs):
		return acos(self * rhs / self.norm() / rhs.norm())
		
	def proj(self, rhs):
		# Returns the projection of self against the RHS
		return self * rhs / rhs.norm()
		
	@staticmethod
	def ones():
		return Vec3(1.,1.,1.)

# [row][col]		
class Mat3:
	def __init__(self, v00=None, v10=None, v20=None, v01=None, v11=None, v21=None, v02=None, v12=None, v22=None):
		# Default to identity
		self.values = [[1,0,0],[0,1,0],[0,0,1]]
		if v00 is not None:
			if v10 is None:
				# Single-argument constructor supports Mat3 and [[],[],[]] (the
				# latter being a list of row vectors)
				if isinstance(v00, Mat3):
					self.set_row(0, v00.get_row(0))
					self.set_row(1, v00.get_row(1))
					self.set_row(2, v00.get_row(2))
				else:
					self.set_row(0, v00[0])
					self.set_row(1, v00[1])
					self.set_row(2, v00[2])
			elif v01 is None:
				# Three-argument constructor supports Vec3,Vec3,Vec3 (as column
				# vectors) [],[],[] (as column vectors), and any combination
				self.set_col(0, v00)
				self.set_col(1, v10)
				self.set_col(2, v20)
			else:
				# Nine-argument constructor gives values by row-column indices
				# used in argument variable names
				self.set_row(0, [v00,v01,v02])
				self.set_row(1, [v10,v11,v12])
				self.set_row(2, [v20,v21,v22])
		
	def __len__(self):
		return 3

	def __str__(self):
		r1 = "[%f, %f, %f\n" % (self.values[0][0], self.values[0][1], self.values[0][2])
		r2 = " %f, %f, %f\n" % (self.values[1][0], self.values[1][1], self.values[1][2])
		r3 = " %f, %f, %f]" % (self.values[2][0], self.values[2][1], self.values[2][2])
		return r1 + r2 + r3
		
	def __getitem__(self, row_ndx):
		return self.get_row(row_ndx)
		
	def __setitem__(self, row_ndx, row_vec):
		self.set_row(row_ndx, row_vec)
		
	def get_row(self, ndx):
		return Vec3(self.values[ndx])
		
	def set_row(self, ndx, vec):
		if isinstance(vec, Vec3):
			self.values[ndx] = vec
		else:
			self.values[ndx] = Vec3(vec)
		
	def get_col(self, ndx):
		return Vec3(self.values[0][ndx], self.values[1][ndx], self.values[2][ndx])
		
	def set_col(self, ndx, vec):
		self.values[0][ndx] = vec[0]
		self.values[1][ndx] = vec[1]
		self.values[2][ndx] = vec[2]
		
	def __add__(self, rhs):
		return Mat3(self[0] + rhs[0], self[1] + rhs[1], self[2] + rhs[2])
		
	def __sub__(self, rhs):
		return self + (rhs * -1)
		
	def __mul__(self, rhs):
		if isinstance(rhs, Mat3):
			# Matrix product
			r0 = self.get_row(0)
			r1 = self.get_row(1)
			r2 = self.get_row(2)
			c0 = rhs.get_col(0)
			c1 = rhs.get_col(1)
			c2 = rhs.get_col(2)
			return Mat3(r0 * c0, r1 * c0, r2 * c0, r0 * c1, r1 * c1, r2 * c1, r0 * c2, r1 * c2, r2 * c2)
		elif isinstance(rhs, Vec3):
			# Vector product
			return Vec3(self.get_row(0) * rhs, self.get_row(1) * rhs, self.get_row(2) * rhs)
		else:
			# Scalar product
			return Mat3(self.get_row(0) * rhs, self.get_row(1) * rhs, self.get_row(2) * rhs)
		
	def __rmul__(self, lhs):
		if isinstance(lhs, Mat3):
			return lhs.__mul__(self)
		elif isinstance(lhs, Vec3):
			raise Exception("[3x1] cannot be multiplied by [3x3]; inner dimensions must match")
		else:
			return self * lhs
		
	def __pow__(self, rhs):
		if type(rhs) == type(0):
			lhs = Mat3(self.values)
			if rhs < 0:
				rhs = -rhs
				lhs = lhs.inv()
			res = Mat3()
			n = 0
			while n < rhs:
				res = res * lhs
				n = n + 1
			return res
		else:
			raise Exception("Only integer powers supported for real-valued matrices")
			
	def __div__(self, rhs):
		if isinstance(rhs, Mat3):
			# Matrix division
			return self * (rhs.inv())
		elif isinstance(rhs, Vec3):
			# Solve equation using inverse (not stable)
			warnings.warn("Inverse-based algorithm is not stable")
			return self.inv() * rhs
		else:
			return self * (1.0 / rhs)
	
	def __truediv__(self, rhs):
		return self.__div__(rhs)
		
	def trans(self):
		return Mat3(self.get_row(0), self.get_row(1), self.get_row(2))
		
	def inv(self):
		d = self.det()
		A = self[1][1] * self[2][2] - self[1][2] * self[2][1]
		B = self[1][2] * self[2][0] - self[1][0] * self[2][2]
		C = self[1][0] * self[2][1] - self[1][1] * self[2][0]
		D = self[0][2] * self[2][1] - self[0][1] * self[2][2]
		E = self[0][0] * self[2][2] - self[0][2] * self[2][0]
		F = self[0][1] * self[2][0] - self[0][0] * self[2][1]
		G = self[0][1] * self[1][2] - self[0][2] * self[1][1]
		H = self[0][2] * self[1][0] - self[0][0] * self[1][2]
		I = self[0][0] * self[1][1] - self[0][1] * self[1][0]
		return Mat3(A, B, C, D, E, F, G, H, I).trans() / d
		
	def trace(self):
		return self[0][0] + self[1][1] + self[2][2]
		
	def det(self):
		a = self[0][0] * (self[1][1] * self[2][2] - self[1][2] * self[2][1])
		b = self[0][1] * (self[1][0] * self[2][2] - self[1][2] * self[2][0])
		c = self[0][2] * (self[1][0] * self[2][1] - self[1][1] * self[2][0])
		return a - b + c
		
	@staticmethod
	def fromQuat(q):
		m = Mat3()
		qr, qi, qj, qk = q
		m[0][0] = 1 - 2 * qj**2 - 2 * qk**2
		m[0][1] = 2 * (qi * qj - qk * qr)
		m[0][2] = 2 * (qi * qk + qj * qr)
		m[1][0] = 2 * (qi * qj + qk * qr)
		m[1][1] = 1 - 2 * qi**2 - 2 * qk**2
		m[1][2] = 2 * (qj * qk - qi * qr)
		m[2][0] = 2 * (qi * qk - qj * qr)
		m[2][1] = 2 * (qj * qk + qi * qr)
		m[2][2] = 1 - 2 * qi**2 - 2 * qj**2
		return m

class Rot:
	# Lower-case applies a rotation to a vector
	# Upper-case is a frame transformation A => B (A + rotation = B, column vectors = unit vectors of A as evaluated in B)
	@staticmethod
	def x(ang_rad):
		return Mat3([1., 0., 0.], [0., cos(ang_rad), sin(ang_rad)], [0., -sin(ang_rad), cos(ang_rad)])
		
	@staticmethod
	def y(ang_rad):
		return Mat3([cos(ang_rad), 0., -sin(ang_rad)], [0., 1., 0.], [sin(ang_rad), 0., cos(ang_rad)])
		
	@staticmethod
	def z(ang_rad):
		return Mat3([cos(ang_rad), sin(ang_rad), 0.], [-sin(ang_rad), cos(ang_rad), 0.], [0., 0., 1.])

	@staticmethod
	def X(ang_rad):
		return Mat3([1., 0., 0.], [0., cos(ang_rad), sin(ang_rad)], [0., -sin(ang_rad), cos(ang_rad)]).trans()
		
	@staticmethod
	def Y(ang_rad):
		return Mat3([cos(ang_rad), 0., -sin(ang_rad)], [0., 1., 0.], [sin(ang_rad), 0., cos(ang_rad)]).trans()
		
	@staticmethod
	def Z(ang_rad):
		return Mat3([cos(ang_rad), sin(ang_rad), 0.], [-sin(ang_rad), cos(ang_rad), 0.], [0., 0., 1.]).trans()
		
	@staticmethod
	def q(ang_rad, axis):
		s = sin(0.5 * ang_rad)
		return [cos(0.5 * ang_rad), s * axis[0], s * axis[1], s * axis[2]]
