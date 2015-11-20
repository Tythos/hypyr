"""Models and renders basic star
"""

import enum
import csv
from pyglet import gl
from math import sin, cos
import colorsys

class HarvardSpectralClass(enum.Enum):
	unknown = 0
	O = 1
	B = 2
	A = 3
	F = 4
	G = 5
	K = 6
	M = 7
	
	@classmethod
	def getFromKey(cls, key):
		return cls.__members__[key]
		
	def getHueSat(self):
		hues = [0.,266/360.,226/360.,224/360.,240/360.,33/360.,31/360.,29/360.]
		saturations = [0.,38/100.,35/100.,24/100.,6/100.,9/100.,28/100.,51/100.]
		return (hues[self.value],saturations[self.value])
		
class Star(object):
	def __init__(self):
		self.sao = 0
		self.ra_rad = 0.
		self.dec_rad = 0.
		self.apparent_vm = 0.
		self.spec = HarvardSpectralClass.unknown
		
	def getRgb(self):
		# Hue, saturation determined by classification; value scales between 0.2 and 0.8 w.r.t. VM
		h, s = self.spec.getHueSat()
		vMin, vMax = 0.5, 1.0
		v = vMin + (vMax - vMin) * (self.apparent_vm - 7.0) / (-1.6 - 7.0)
		return colorsys.hsv_to_rgb(h, s, v)
		
	def getSize(self):
		# Returns size estimate, in pixels, scaled from VM
		sMin, sMax = 1.0, 4.0
		return sMin + (sMax - sMin) * (self.apparent_vm - 7.0) / (-1.6 - 7.0)
	
	@staticmethod
	def getCatalog(name):
		cat = []
		with open(name) as f:
			reader = csv.DictReader(f)
			for row in reader:
				star = Star()
				star.sao = int(row['sao'])
				star.ra_rad = float(row['ra_rad'])
				star.dec_rad = float(row['dec_rad'])
				star.apparent_vm = float(row['apparent_vm'])
				star.spec = HarvardSpectralClass.getFromKey(row['spec'])
				cat.append(star)
		return cat
		
	@staticmethod
	def renderCatalog(cat, far):
		gl.glDisable(gl.GL_LIGHTING)
		for s in cat:
			c = s.getRgb()
			gl.glPointSize(s.getSize())
			gl.glBegin(gl.GL_POINTS)
			gl.glColor3f(c[0], c[1], c[2])
			gl.glVertex3f(far * cos(s.ra_rad) * cos(s.dec_rad), far * sin(s.ra_rad) * cos(s.dec_rad), far * sin(s.dec_rad))
			gl.glEnd()
		gl.glEnable(gl.GL_LIGHTING)
