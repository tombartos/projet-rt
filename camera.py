import vecteur

class Camera:
	'''Camera definie par des dimensions (largeur, hauteur), une position (x,y,z), une direction (vecteur), une orientation (up vector), une distance focale (scalaire)'''
	def __init__(self, largeur, hauteur, position, direction, orientation, distance):
		self.dim = (largeur, hauteur)
		self.pos = position
		self.dir = direction
		self.ori = orientation
		self.dis = distance

	def rayon(self, plan, pplan):
		'''Renvoie le rayon du point d'origine F vers un point pplan (x,y) du plan plan (dimx, dimy)'''
		C = vecteur.Point(self.pos)
		F =  self.pos + self.dis
		l = plan[0]
		h = plan[1]
		H = vecteur.Vecteur(extremite = (0,1,0))
		D = vecteur.Vecteur(extremite = (1,0,0))
		tmp = H * (h/2 - 1/2) - D * (l/2 - 1/2)
		P0 = C.addition(tmp).extr

		if pplan == (0,0):
			return P0

		return (P0[0] + pplan[0], P0[1] - pplan[1], 0)
