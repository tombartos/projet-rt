import vecteur
import couleur
import sphere
import plan
import lumiere
import camera

class Scene:

	def __init__(self, cam = None,obj_list = [], lum_list = [], amb = None, img = None):
		
		self.cam = cam
		self.obj_list = obj_list
		self.lum_list = lum_list
		self.amb = amb
		self.img = img
		
	
	def ajouter_sphere(self,pos,coul,diff,spec,ref,ombre,rayon):
		'''ajoute une sphere a la scene'''
		self.obj_list.append(sphere.Sphere(pos,coul,diff,spec,ref,ombre,rayon))
		
	
	def ajouter_plan(self,pos,coul,diff,spec,ref,ombre,normale):
		'''ajoute un plan a la scene'''
		self.obj_list.append(plan.Plan(normale, pos, coul, diff, spec, ref, ombre))
	
	def ajouter_lumiere(self, position, couleur):
		'''ajoute une source lumineuse a la scene'''
		self.lum_list.append(lumiere.Lumiere(position, couleur))
	
	def plus_proche_intersection(self,obj,point,rayon_vue):
		'''calcule l'intersection entre une droite et un objet de la scene la plus proche de la camera'''
		#Pas sur du tout qu'il faut faire ca
		return obj.intersection(point,rayon_vue)
	

	def modifier_camera(self, largeur, hauteur, position, direction, orientation, distance):
		"""Modifie la camera de la scene"""
		self.cam = camera.Camera(largeur, hauteur, position, direction, orientation, distance)

	def construrire_image(self):
		"""Algorithme principal qui construit l'image"""
		tab_ray_vue = []		#Premiere etape : calcul des rayons de vue
		for i in range (600):
			for j in range(400):
				tab_ray_vue.append(self.cam.rayon((i,j)))
		print(tab_ray_vue)

if __name__ == "__main__":
	scene = Scene()
	dim = (600,400)			#Dimensions de l'image
	scene.modifier_camera(dim[0], dim[1], (0,0,0), (0,0,-1), (0,1,0), 5)
	scene.ajouter_sphere((0, 9-(1/(2**0.5)), -4-(1/(2**0.5))), (0,255,0), None, None, None, False, 1)
	scene.construrire_image()
	
	
