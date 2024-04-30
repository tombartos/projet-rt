import vecteur

class Camera:
	'''Camera definie par des dimensions (largeur, hauteur), une position (x,y,z), une direction (vecteur), une orientation (up vector), une distance focale (scalaire)'''
	def __init__(self, largeur, hauteur, position, direction, orientation, distance):
		self.dim = (largeur, hauteur)
		self.pos = vecteur.Point(position)
		self.dir = direction
		self.ori = orientation
		self.dis = distance

	def rayon(self, pplan):
		'''Renvoie le point (x, y z) et le rayon du point d'origine F vers un point pplan (x,y) du plan des dimensions de la camera'''
		C = self.pos
		F = vecteur.Point((self.pos.extr[0], self.pos.extr[1],self.pos.extr[2] + self.dis)) #TEMPORAIRE, Ne marche que si direction = (0,0,+-1), faire le calcul en entier
																			 #Si on veut pouvoir faire pivoter la camera
		l = self.dim[0]								#Calcul du point Pxy 
		h = self.dim[1]
		H = vecteur.Vecteur(extremite = (0,1,0))
		D = vecteur.Vecteur(extremite = (1,0,0))
		P0 = C.addition(H * (h/2 - 0.5) - D * (l/2 - 0.5)).extr
			
		Pxy = vecteur.Point((P0[0] + pplan[0], P0[1] - pplan[1], 0))  #Attention au 0 quand on voudra faire des rotations de caméra

		res = vecteur.Vecteur(F.extr, Pxy.extr)

		return Pxy, res.normalisation()
	
if __name__ == "__main__":
	cam = Camera(11, 11, (0,0,0), (0,0,-1), (0,1,0), 5)
	a = cam.rayon((5,0))
	print(a[0].extr, a[1].composantes())