"""Basic shapes for scene rendering, extended from base object (Thing) class
"""

from pyglet import gl, graphics
from math import pi, sin, cos, sqrt
from hypyr import scene, linal

def frange(xMin, dx, xMax):
	vals = [xMin]
	while xMin <= xMax:
		xMin += dx
		vals.append(min(xMin,xMax))
	return vals
	
class Sphere(scene.Thing):
	def __init__(self, r=1., slices=32):
		super(Sphere, self).__init__()
		self.batch = graphics.Batch()
		vertices = []
		normals = []
		textureuvw = []
		tangents = []
		indices = []
		tht_rad = frange(0., 2 * pi / (slices - 1.), 2 * pi)
		phi_rad = frange(-0.5 * pi, pi / (slices - 1.), 0.5 * pi)
		for t in tht_rad:
			for p in phi_rad:
				vertices.extend([
					r * cos(t) * cos(p),
					r * sin(t) * cos(p),
					r * sin(p)])
				normals.extend([
					cos(t) * cos(p),
					sin(t) * cos(p),
					sin(p)])
				textureuvw.extend([
					t / (2 * pi),
					(p + pi / 2) / pi,
					0.])
				tangents.extend([
					int(round(255 * (0.5 - 0.5 * sin(p)))),
					int(round(255 * (0.5 - 0.5 * 0))),
					int(round(255 * (0.5 - 0.5 * -cos(t) * cos(p))))])
		for i in range(slices - 1):
			for j in range(slices - 1):
				p = i * slices + j
				indices.extend([p, p + slices, p + slices + 1])
				indices.extend([p, p + slices + 1, p + 1])
		self.vertex_list = self.batch.add_indexed(len(vertices)//3, gl.GL_TRIANGLES, None, indices, ('v3f/static', vertices), ('n3f/static', normals), ('t3f/static', textureuvw), ('c3B/static', tangents))

	def delete(self):
		self.vertex_list.delete()

	def render(self):
		self.batch.draw()
