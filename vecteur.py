import numpy as np


class Vecteur:
	'''Classe decrivant des vecteurs à 3 dimensions (x, y, z)'''
	def __init__(self, origine = (0,0,0), extremite = (0,0,0)):  #Origine et extremite sont des points (x,y,z)
		self.org = np.array(origine, dtype = float)
		self.extr = np.array(extremite, dtype = float)

	def __str__(self):
		return "Vecteur : origine = " + str(self.org) + ", extremite = " + str(self.extr) + ", composantes = " + str(self.composantes())
	
	def __add__(self, vec):
		if type(vec) == type(Vecteur):
			return self.addition(vec)
		else:
			return Vecteur(self.org, self.extr + vec)   #Addition par un scalaire

	def __sub__(self, vec):
		return self.soustraction(vec)

	def __mul__(self, scal):
		return self.mult_scal(scal)

	def __rmul__(self, scal):
		return self.mult_scal(scal)

	def composantes(self):
		'''Renvoie les composantes du vecteur self'''
		tmp = []
		for i in range(3):
			tmp.append(self.extr[i] - self.org[i])
		return np.array(tmp, dtype = float)


	def addition(self, vec):
		'''Renvoie le vecteur self + vec'''
		tmp = self.composantes()
		tmp2 = vec.composantes()

		tmp3 = np.add(tmp, tmp2)
		for i in range(3):
			tmp3[i] = self.org[i] + tmp3[i]
		return Vecteur(self.org, tmp3)

	def soustraction(self, vec):
		'''Renvoie le vecteur self - vec'''
		tmp = self.composantes()
		tmp2 = vec.composantes()
		tmp3 = np.subtract(tmp, tmp2)
		for i in range(3):
			tmp3[i] = self.org[i] + tmp3[i]
		return Vecteur(self.org, tmp3)

	def mult_scal(self, scal):
		'''Renvoie le vecteur self * scal (scalaire)'''
		comp = self.composantes()
		comp = comp * scal
		extremite = np.add(self.org, comp)
		return Vecteur(self.org, extremite)

	def prod_scal(self, vec):
		'''Renvoie le produit scalaire'''
		return np.dot(self.composantes(), vec.composantes())

	def norme(self):
		'''Renvoie la norme du vecteur'''
		return np.linalg.norm(self.composantes())

	def normalisation(self):
		'''Renvoie un nouveau vecteur qui est la normalisation de self'''
		norme = self.norme()
		comp = self.composantes()
		comp /= norme
		return Vecteur(self.org, self.org + comp)


class Point(Vecteur):
	def __init__(self, coords):
		Vecteur.__init__(self, coords, coords)

	def addition(self, vec):
		tmp = self.extr
		tmp2 = vec.composantes()

		tmp3 = np.add(tmp, tmp2)
		return Point(tmp3)
	
	def soustraction(self, vec):
		'''Renvoie le vecteur self - vec'''
		tmp = self.extr
		tmp2 = vec.composantes()
		tmp3 = np.subtract(tmp, tmp2)
		return Point(tmp3)
	

if __name__ == "__main__":
	vec = Vecteur((0,0,0), (2, 2, 2))
	vec2 = -1*vec
	print(vec2)