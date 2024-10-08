import objet3D
import vecteur

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

		denom = (A*i + B*j + C*k)
		if denom == 0:
			return False
		t = -1 * ((A*x1 + B*y1 + C*z1 + D) /denom )
		if t<1:
			return False		#pas de point d'intersection, le plan est derriere le point d'origine du rayon

		xres = x1 + v[0]*t
		yres = y1 + v[1]*t
		zres = z1 + v[2]*t

		return (xres,yres,zres)

	def normale(self, point):  #Je mets point ici pour eviter les problemes avec la methode normale pour les spheres
		'''Renvoie la normale au plan'''
		return vecteur.Vecteur(extremite = self.norm)	
