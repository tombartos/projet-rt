import vecteur


class Objet3D:

	def __init__(self,pos,coul,diff,spec,ref,ombre):
		
		self.pos = pos
		self.coul = coul
		self.diff = diff
		self.spec = spec
		self.ref = ref
		self.ombre = ombre
	 
	
	def intersection(self,droite,camera):
		'''retourne le point d'intersection avec une droite le plus proche de la camera'''
	
		raise NotImplementedError
		
		
	def normale(self):
		'''retourne la normale d'un point a la surface de l'objet'''
		
		raise NotImplementedError
		
	


	
		



  
