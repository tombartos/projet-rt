import Vecteur
import Couleur
import Sphere
import Plan
import Lumiere
import Camera

class Scene:

	def __init__(self,cam,obj_list,lum_list,amb,img):
		
		self.cam = cam
		self.obj_list = obj_list
		self.lum_list = lum_list
		self.amb = amb
		self.img = img
		
	
	def ajouter_sphere(self,pos,coul,diff,spec,ref,ombre,rayon):
		'''ajoute une sphere a la scene'''
		self.obj_list.append(Sphere(pos,coul,diff,spec,ref,ombre,rayon))
		
	
	def ajouter_plan(self,pos,coul,diff,spec,ref,ombre,rayon):
		'''ajoute un plan a la scene'''
		self.obj_list.append(Plan(normale, pos, coul, diff, spec, ref, ombre))
	
	def ajouter_lumiere(self, position, couleur):
		'''ajoute une source lumineuse a la scene'''
		self.lum_list.append(Lumiere(position, couleur))
	
	def plus_proche_intersection(self,obj,point,rayon_vue):
		'''calcule l'intersection entre une droite et un objet de la scene la plus proche de la camera'''
		return obj.intersection(point,rayon_vue)
	
	#def construrire_image():
		
	
