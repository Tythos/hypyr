"""Fundamental elements for scene management
"""

from linal import Vec3, Mat3, Rot, raw
from shader import Shader
from pyglet import resource, gl
from os import path
from math import sin, cos, atan2, sqrt, pi

class Camera(object):
	def __init__(self):
		self.eye = Vec3(1.,0.,0.)
		self.tgt = Vec3(0.,0.,0.)
		self.up = Vec3(0.,0.,1.)
		self.yFov_rad = 45. * pi/180
		self.xFov_rad = 45. * pi/180
		self.zNear = 1.0
		self.zFar = 10.
		
	def apply(self):
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()
		gl.gluPerspective(self.yFov_rad * 180/pi, self.xFov_rad / self.yFov_rad, self.zNear, self.zFar)
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
		gl.gluLookAt(self.eye[0], self.eye[1], self.eye[2], self.tgt[0], self.tgt[1], self.tgt[2], self.up[0], self.up[1], self.up[2])
		
	def sphericalRotation(self, dTht_rad, dPhi_rad):
		polarMargin_rad = 0.01
		drXyz = self.tgt - self.eye
		dr = drXyz.norm()
		tht_rad = atan2(drXyz[1], drXyz[0])
		phi_rad = atan2(drXyz[2], sqrt(drXyz[0]**2 + drXyz[1]**2))
		tht_rad = (tht_rad + dTht_rad) % (2 * pi)
		phi_rad = phi_rad + dPhi_rad
		if phi_rad > 0.5 * pi - polarMargin_rad:
			phi_rad = 0.5 * pi - polarMargin_rad
		if phi_rad < -0.5 * pi + polarMargin_rad:
			phi_rad = -0.5 * pi + polarMargin_rad
		drXyz = dr * Vec3(cos(tht_rad) * cos(phi_rad), sin(tht_rad) * cos(phi_rad), sin(phi_rad))
		self.eye = self.tgt - drXyz
		
	def zoom(self, pct):
		min = 0.1
		drXyz = self.tgt - self.eye
		dr = max(pct * drXyz.norm(), min)
		drXyz = dr * drXyz.normalize()
		self.eye = self.tgt - drXyz
		
class Material(object):
	def __init__(self):
		self.ambient_rgb = 0.1 * Vec3.ones()
		self.diffuse_rgb = 0.6 * Vec3.ones()
		self.specular_rgb = 0.3 * Vec3.ones()
		self.shininess = 1.
		self.textures = []
		self.shaders = []
		self.parameters = {}
		
	def addShader(self, vertexPath, fragmentPath):
		with open(vertexPath, 'r') as h:
			v = h.read()
		with open(fragmentPath, 'r') as h:	
			f = h.read()
		self.shaders.append(Shader([v], [f]))
		
	def addTexture(self, imgPath):
		dir, file = path.split(imgPath)
		if dir not in resource.path:
			resource.path.append(dir)
			resource.reindex()
		texture = resource.texture(file)
		self.textures.append(texture)
		gl.glBindTexture(texture.target, texture.id)
		gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST_MIPMAP_LINEAR)
	
	def apply(self):
		gl.glEnable(gl.GL_LIGHTING)
		for s in self.shaders:
			s.bind()
		for i, t in enumerate(self.textures):
			gl.glActiveTexture(gl.GL_TEXTURE0+i)
			gl.glEnable(gl.GL_TEXTURE_2D)
			gl.glBindTexture(gl.GL_TEXTURE_2D, t.id)
			self.parameters['tex[%u]' % i] = i
		for k in self.parameters.keys():
			if type(self.parameters[k]) == type(0):
				for s in self.shaders:
					s.uniformi(k, self.parameters[k])
			if type(self.parameters[k]) == type(0.):
				for s in self.shaders:
					s.uniformf(k, self.parameters[k])
		a = self.ambient_rgb
		d = self.diffuse_rgb
		s = self.specular_rgb
		gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, raw(a[0], a[1], a[2], 1.))
		gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, raw(d[0], d[1], d[2], 1.))
		gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, raw(s[0], s[1], s[2], 1.))
		gl.glMaterialf(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, self.shininess)
	
	def unapply(self):
		for i in range(len(self.textures)):
			gl.glActiveTexture(gl.GL_TEXTURE0+i)
			gl.glDisable(gl.GL_TEXTURE_2D)
		for s in self.shaders:
			s.unbind()
	
class Thing(object):
	def __init__(self):
		self.material = Material()
		self.position = Vec3()
		self.rotation = Mat3()
		self.linVel = Vec3()
		self.angVel = Vec3()
		self.children = []
	
	def update(self, dt_s):
		self.position = self.position + dt_s * self.linVel
		ang_rad = self.angVel.norm() * dt_s
		if ang_rad > 0:
			axis = self.angVel.normalize()
			q = Rot.q(ang_rad, axis)
			self.rotation = Mat3.fromQuat(q) * self.rotation
		for c in self.children:
			c.update(dt_s)
		
	def render(self):
		# By default, a frame renders its axis as unit RGB line segments
		gl.glDisable(gl.GL_TEXTURE_2D)
		gl.glDisable(gl.GL_LIGHTING)
		gl.glBegin(gl.GL_LINES)
		gl.glColor3f(1.,0.,0.)
		gl.glVertex3f(0.,0.,0.)
		gl.glVertex3f(1.,0.,0.)
		gl.glColor3f(0.,1.,0.)
		gl.glVertex3f(0.,0.,0.)
		gl.glVertex3f(0.,1.,0.)
		gl.glColor3f(0.,0.,1.)
		gl.glVertex3f(0.,0.,0.)
		gl.glVertex3f(0.,0.,1.)
		gl.glEnd()
		
	def chain(self):
		gl.glPushMatrix()
		p = self.position
		r = self.rotation
		gl.glMultMatrixf(raw(r[0][0], r[1][0], r[2][0], 0., r[0][1], r[1][1], r[2][1], 0., r[0][2], r[1][2], r[2][2], 0., p[0], p[1], p[2], 1.))
		self.material.apply()
		self.render()
		self.material.unapply()
		for c in self.children:
			c.chain()
		gl.glPopMatrix()

class Light(Thing):
	nLights = 0
	
	def __init__(self):
		super(Light, self).__init__()
		self.id = Light.nLights
		Light.nLights = Light.nLights + 1
		
	def render(self):
		p = self.position
		a = self.material.ambient_rgb
		d = self.material.diffuse_rgb
		s = self.material.specular_rgb
		id = gl.GL_LIGHT0 + self.id
		gl.glEnable(gl.GL_LIGHTING)
		gl.glEnable(id)
		gl.glLightfv(id, gl.GL_POSITION, raw(p[0], p[1], p[2], 1.))
		gl.glLightfv(id, gl.GL_AMBIENT, raw(a[0], a[1], a[2], 1.))
		gl.glLightfv(id, gl.GL_DIFFUSE, raw(d[0], d[1], d[2], 1.))
		gl.glLightfv(id, gl.GL_SPECULAR, raw(s[0], s[1], s[2], 1.))
