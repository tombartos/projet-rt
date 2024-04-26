import numpy as np

class Couleur:
	
	
	def __init__(self,r,g,b):
	
		self.r = r
		self.g = g
		self.b = b
		
	
	def mod_r(self,val):
		'''mutateur de la composante rouge'''	
		self.r = val
	
		
	def mod_g(self,val):
		'''mutateur de la composante verte'''	
		self.g = val
	
		
	def mod_b(self,val):
		'''mutateur de la composante rouge'''	
		self.b = val
		
		
	def addition(self,coul):
		'''addition entre 2 vecteurs''''
		
		r,g,b = np.add((self.r,self.g,self.b),(coul.r,coul.g,coul.b)) % 256
		res = Couleur(r,g,b)
		#norm = math.sqrt(pow(res.r,2) + pow(res.g,2) + pow(res.b,2))
		#res.r, res.g, res.b = res.r/norm, res.g/norm, res.b/norm
		return res
		
		
	def multiplication_v(self,coul):
		'''produit vectoriel'''
	
		r,g,b = np.multiply((self.r,self.g,self.b),(coul.r,coul.g,coul.b)) % 256
		res = Couleur(r,g,b)
		#norm = math.sqrt(pow(res.r,2) + pow(res.g,2) + pow(res.b,2))
		#res.r, res.g, res.b = res.r/norm, res.g/norm, res.b/norm
		return res
	
	
	def multiplication_s(self,scal):
		'''produit scalaire-vecteur'''
	
		r,g,b = np.multiply((self.r,self.g,self.b),scal) % 256
		res = Couleur(r,g,b)
		#norm = math.sqrt(pow(res.r,2) + pow(res.g,2) + pow(res.b,2))
		#res.r, res.g, res.b = res.r/norm, res.g/norm, res.b/norm
		return res
		
