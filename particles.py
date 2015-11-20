"""Basic objects for managing and rendering different sprite-based particles
"""

from pyglet import gl
from hypyr import scene, data

class Sprite(scene.Thing):
	isFirstPassRender = True
	def __init__(self):
		super(Sprite,self).__init__()
		self.material.addTexture(data.get_path('textures/dot.png'))
		self.material.addShader(data.get_path('shaders/sprite.v.glsl'), data.get_path('shaders/sprite.f.glsl'))
		self.size = 0.1

	def render(self):
		s = self.size
		gl.glDisable(gl.GL_DEPTH_TEST)
		gl.glDisable(gl.GL_LIGHTING)
		gl.glBegin(gl.GL_TRIANGLES)
		gl.glNormal3f(1.,0.,0.)
		gl.glTexCoord2f(0.,0.)
		gl.glVertex3f(0.,-s,-s)
		gl.glTexCoord2f(1.,0.)
		gl.glVertex3f(0.,s,-s)
		gl.glTexCoord2f(1.,1.)
		gl.glVertex3f(0.,s,s)
		gl.glTexCoord2f(0.,0.)
		gl.glVertex3f(0.,-s,-s)
		gl.glTexCoord2f(1.,1.)
		gl.glVertex3f(0.,s,s)
		gl.glTexCoord2f(0.,1.)
		gl.glVertex3f(0.,-s,s)
		gl.glEnd()
		gl.glEnable(gl.GL_LIGHTING)
		gl.glEnable(gl.GL_DEPTH_TEST)
	
class BgSprite(Sprite):
	pass
	
class Particle(Sprite):
	pass
	
class Emitter(scene.Thing):
	pass
