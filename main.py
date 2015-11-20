"""Pyglet/GLSL aliasing demo, evolved from pythonstuff.org
"""

from math import pi, sin, cos, sqrt
from random import random
from pyglet import gl, window, image, resource, clock, text, event, app
from os import path
from hypyr import particles, linal, shader, scene, data, solids

class HypyrApp(window.Window):
	def __init__(self):
		config = gl.Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
		try:
			super(HypyrApp, self).__init__(resizable=True, config=config, vsync=False, width=800, height=600)
		except pyglet.window.NoSuchConfigException:
			super(HypyrApp, self).__init__(resizable=True)
		self.scene = scene.Thing()
		self.camera = scene.Camera()
		clock.schedule(self.update)
		self.setupOpenGL()
		
	def setupOpenGL(self):
		gl.glClearColor(0., 0., 0., 1.)
		gl.glColor4f(1.0, 0.0, 0.0, 0.5)
		gl.glEnable(gl.GL_DEPTH_TEST)
		#gl.glEnable(gl.GL_CULL_FACE)
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		#gl.glPolygonMode(gl.GL_FRONT, gl.GL_FILL)

	def on_resize(self, width, height):
		if height == 0:
			height = 1
		gl.glViewport(0, 0, width, height)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()
		self.camera.yFov_rad = self.camera.xFov_rad * height / width
		self.camera.apply()
		gl.glMatrixMode(gl.GL_MODELVIEW)
		return event.EVENT_HANDLED

	def update(self, dt):
		self.scene.update(dt)

	def on_draw(self):
		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
		gl.glLoadIdentity()
		self.camera.apply()
		self.scene.chain()

	def on_key_press(self, symbol, modifiers):
		k = window.key
		if symbol == k.R:
			rot = linal.Vec3()
		elif symbol == k.ESCAPE or symbol == k.Q:
			app.exit()
			return event.EVENT_HANDLED
		elif symbol == k.A:
			self.camera.sphericalRotation(-0.1, 0.)
			particles.Sprite.isFirstPassRender = True
		elif symbol == k.S:
			self.camera.sphericalRotation(0., -0.1)
		elif symbol == k.W:
			self.camera.sphericalRotation(0., 0.1)
		elif symbol == k.D:
			self.camera.sphericalRotation(0.1, 0.)
		elif symbol == k.EQUAL:
			self.camera.zoom(0.9)
		elif symbol == k.MINUS:
			self.camera.zoom(1.1)

if __name__ == "__main__":
	a = HypyrApp()
	a.camera.eye = linal.Vec3(3., -1., 1.)
	for i in range(16):
		s = particles.Sprite()
		s.position = linal.Vec3((i/8.-1.),random()-0.5,random()-0.5)
		s.material.ambient_rgb = linal.Vec3(random(),random(),random())
		s.size = 0.1 * random()
		a.scene.children.append(s)
	app.run()
