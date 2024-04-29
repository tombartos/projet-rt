import vecteur
import couleur
import sphere
import plan
import lumiere
import camera
import numpy as np
from PIL import Image as im 

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

	def dist_euclid(self, point1, point2):
		"""Retourne la distance euclidienne entre les deux points (x, y, z)"""
		return ((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2 + (point2[2]-point1[2])**2)**0.5
	
	def plus_proche_intersection(self,point,rayon_vue):
		'''Renvoie l'indice de l'objet dans la liste d'objets qui a le point d'intersection le plus proche entre le rayon rayon_vue qui part du point point (eviter la focale) et le point
		point, -1 si aucun point d'intersection n'est trouve, renvoie aussi les coords du point d'intersection'''
		#Il faut parcourir tous les objets, calculer intersection et prendre le point d'intersection avec la plus petite
		#Distance euclidienne avec la camera
		imin = -1
		intermin = None			#On initialise comme si il n'y avait pas d'intersection
		i = 0
		n = len(self.obj_list)
		while (imin == -1) and (i < n):					#On cherche le premier objet de la liste qui intersecte le rayon
			intermin = self.obj_list[i].intersection(point.extr,rayon_vue.composantes())
			if intermin:
				imin = i
				distmin = self.dist_euclid(point.extr, intermin)
			i+=1

		while i<n:				#On parcourt les objets qu'il reste
			intertmp = self.obj_list[i].intersection(point.extr,rayon_vue.composantes())
			if intertmp :
				disttmp = self.dist_euclid(point.extr, intertmp)
				if disttmp < distmin:							#On garde que la plus proche intersection
					imin = i
					intermin = intertmp
					distmin = disttmp
			i+=1
		return imin, intermin

	

	def modifier_camera(self, largeur, hauteur, position, direction, orientation, distance):
		"""Modifie la camera de la scene"""
		self.cam = camera.Camera(largeur, hauteur, position, direction, orientation, distance)

	def ray_reflechi(self, I, N):
		"""Renvoie le rayon reflechi de I par rapport a la normale N"""
		return I.addition(2 * ((-1 * I).prod_scal(N)) * N)
	
	def phong(self, obj, Ii, L, inter, rayon_vue=None, n=100, R=None):
		'''Applique le modèle d'illumination de Phong à l'objet'''
		N = obj.normale(inter)			#inter = point d'intersection
		Ia = self.Ia
		ka = self.ka
		kd = obj.diff
		ks = obj.spec
		V = rayon_vue
		print((Ia.mult_scal(ka)).composantes())
		print((Ii.mult_scal(kd*L.prod_scal(N) + ks*((R.prod_scal(V))**100))).composantes())
		return (Ia.mult_scal(ka)).addition(Ii.mult_scal(kd*L.prod_scal(N) + ks*((R.prod_scal(V))**100)))
	
	def lancer_rayon(self, point, rayon):
		"""Algorithme de lancer de rayon, point est le point du plan de l'espace mathematique duquel part le rayon de vue rayon, mat_px est la matrice de pixels,
		Renvoie la couleur du pixel du point d'intersection si il existe"""
		iobj, inter = self.plus_proche_intersection(point, rayon) # Deuxieme etape : calcul des intersections (indice de l'objet qui a la plus proche intersection avec la cam)
		if iobj > -1 :
			lum = self.lum_list[0]						#On prend que la première lumière pour l'instant, il faudra faire le mélange de toutes les lumieres
			ray_lum_list = []				#Liste des rayons de lumiere qui vont intercepter l'objet
			for lum in self.lum_list:
				ray_obj_lum = vecteur.Vecteur(inter.extr, lum.extr)
				#TODO: Chercher les rayons de lumiere qui interceptent l'obj
			
			#R = self.ray_reflechi(L, N)

			#return self.obj_list[iobj].coul			
		else:
			return None


	def construire_image(self):
		"""Algorithme principal qui construit l'image"""		
		mat_px = np.full((self.cam.dim[1], self.cam.dim[0], 3), (0, 0, 0), dtype = np.uint8)  #On initialise la matrice de pixels à tout noir														#On doit inverser i et j dans la matrice de pixels a cause de PIL
		for i in range (self.cam.dim[0]):
			for j in range(self.cam.dim[1]):
				point, ray = self.cam.rayon((i,j))				#Premiere etape : calcul des rayons de vue
				px = self.lancer_rayon(point, ray)
				if px:
					mat_px[j][i] = px							#On doit inverser i et j dans la matrice de pixels a cause de PIL
		
		data = im.fromarray(mat_px) #On prend la transposee car PIL et Numpy n'ont pas le meme systeme d'indicage
		data.save('output.png') 


			


if __name__ == "__main__":
	scene = Scene()
	#dim = (600,400)			#Dimensions de l'image
	
	cam=camera.Camera(320,240,(0,0,0),(1,0,0),(0,1,0),500) #Création de la Caméra 
	list_obj=[sphere.Sphere((0,0,-200),(0,255,0),0,0,0, 0, 100), sphere.Sphere((150,0,-200),(255,0,0),0,0,0,0, 50)] #Création de la liste d'objets
	lum=lumiere.Lumiere((-300,0,-50),0)   
	scen=Scene(cam,list_obj,0) #Création de la Scène
	scen.construire_image() #appel fonction pour construire image
	
	# scene.modifier_camera(dim[0], dim[1], (0,0,0), (1,0,0), (0,1,0), 200)
	# scene.ajouter_sphere((200, 200, -100), (0,255,0), None, None, None, False, 70)
	#scene.ajouter_sphere((0, 9-(1/(2**0.5)), -15-(1/(2**0.5))), (0,255,0), None, None, None, False, 1)
	
	#scene.construire_image()
	
	#TODO: il me trouve que deux points d'inter, à voir si c'est normal
