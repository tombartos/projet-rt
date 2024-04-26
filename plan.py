import objet3D

class Plan(objet3D.Objet3D):
	def __init__(self, normale, pos, coul, diff, spec, ref, ombre):
		self.norm = normale
		self.pos = pos
		self.coul = coul
		self.diff = diff
		self.spec = spec
		self.ref = ref
		self.ombre = ombre

	def intersection(self, point, rayon_vue):
		'''Renvoie l'intersection entre le plan (self) et un rayon de vue deja calcule par camera.rayon(point) par rapport à un point'''
		#Rayon envoye depuis le point P et non la focale F !!!

		A = self.norm[0]
		B = self.norm[1]
		C = self.norm[2]
		x = self.pos[0]
		y = self.pos[1]
		z = self.pos[2]
		v = rayon_vue
		i = v[0]
		j = v[1]
		k = v[2]

		D = -1 * (A*x + B*y + C*z)
		P = point
		x1 = point[0]
		y1 = point[1]
		z1 = point[2]


		t = -1 * ((A*x1 + B*y1 + C*z1 + D) / (A*i + B*j + C*k))

		xres = x1 + v[0]*t
		yres = y1 + v[1]*t
		zres = z1 + v[2]*t

		return (xres,yres,zres)

		def normale(self):
			'''Renvoie la normale au plan'''
			return self.norm	
