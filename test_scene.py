import vecteur
import couleur
import sphere
import plan
import lumiere
import test_camera
import numpy as np
from PIL import Image as im

red = (1,0,0)
green = (0,0,1)
blue = (0,0,1)
yellow = (1,1,0)
purple = (1,0,1)
white = (1,1,1)
black = (0,0,0)
grey = (0.5,0.5,0)
orange = (1,0.64,0)
pink = (1,0.75,0.8)
brown = (0.59,0.29,0)
#couleurs

class Scene:

	def __init__(self, Ia = None, ka = None,cam = None,obj_list = [], lum_list = [], img = None):
		#I1 et ka sont respectivement les composantes et le coef. de la lumiere ambiante dans la scene
		self.Ia = Ia
		self.ka = ka
		self.cam = cam
		self.obj_list = obj_list
		self.lum_list = lum_list
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
		'''Renvoie l'indice de l'objet dans la liste d'objets qui a le point d'intersection le plus proche sur la demi droite rayon_vue qui part du point point,
		  -1 si aucun point d'intersection n'est trouve, renvoie aussi les coords du point d'intersection'''
		#Il faut parcourir tous les objets, calculer intersection et prendre le point d'intersection avec la plus petite
		#Distance euclidienne avec la camera
		imin = -1
		intermin = None			#On initialise comme si il n'y avait pas d'intersection
		i = 0
		n = len(self.obj_list)
		while (imin == -1) and (i < n):					#On cherche le premier objet de la liste qui intersecte le rayon
			intermin = self.obj_list[i].intersection(point.extr,rayon_vue.composantes())
			if intermin:
				distmin = self.dist_euclid(point.extr, intermin)										#Securite pour les approximations des points, si a cause d'une approximation on a un point censé etre a la surface d'un objet
				imin = i							#Mais qui se retrouve en fait a l'interieur de cet objet, et trouve donc une intersection avec ce meme objet
														#On verifie que la distance soit superieur a un certain seuil, ici 1 pour considerer que c'est une vraie intersection
			i+=1										#Et pas une erreur d'approximation

		while i<n:				#On parcourt les objets qu'il reste
			intertmp = self.obj_list[i].intersection(point.extr,rayon_vue.composantes())
			if intertmp :
				disttmp = self.dist_euclid(point.extr, intertmp)
				if (disttmp < distmin):							#On garde que la plus proche intersection
					imin = i
					intermin = intertmp
					distmin = disttmp
			i+=1
		return imin, intermin



	def modifier_camera(self, largeur, hauteur, position, direction, orientation, distance):
		"""Modifie la camera de la scene"""
		self.cam = test_camera.Camera(largeur, hauteur, position, direction, orientation, distance)

	def ray_reflechi(self, I, N):
		"""Renvoie le rayon reflechi de I par rapport a la normale N"""
		return (I.addition(2 * ((-1 * I).prod_scal(N)) * N)).normalisation()
	
	def correction_gamma(self, coul_list):
		"""NE FONCTIONNE PAS, Renvoie la liste des couleurs contenues dans coul_list mais auquelles on a appliqué une correction gamma ENTRE 0 ET 1"""
		#print("gamma")
		coul_list = np.array(coul_list)
		max = np.max(coul_list)		#On cherche le max 
		res = coul_list / max
		res = res ** 2  #res ** 2.2
		return res

	def recherche_ray_lum(self, inter):
		"""Renvoie la liste des rayons de lumiere qui touchent le point inter ainsi que la liste des couleurs de chacuns avec correction gamma"""
		lum_list_inter = []				#Liste des lumieres dont les rayons vont intersecter l'objet
		ray_lum_list = []
		for lum in self.lum_list:
			ray_obj_lum = vecteur.Vecteur(inter, lum.pos).normalisation()

			jobj, jinter = self.plus_proche_intersection(vecteur.Point(inter), ray_obj_lum) #On cherche si un objet se trouve sur le rayon de lumiere dans le sens objet -> lumiere
			#print(jobj, jinter)
			if jobj == -1 :										#Pas d'objet entre notre point et notre lumiere, on est bon
				lum_list_inter.append(lum)
				ray_lum_list.append(ray_obj_lum)
			else:											#Un objet est sur la demi droite, il faut verifier si il est avant ou apres la lumiere par rapport au point
				a = self.dist_euclid(inter, lum.pos)
				b = self.dist_euclid(inter, jinter)
				if a < b : 			#Lumiere plus proche que l'autre objet, on est bon
					lum_list_inter.append(lum)
					ray_lum_list.append(ray_obj_lum)
		
		coul_list = []
		if len(lum_list_inter) > 0:	
			for lum in lum_list_inter:
				coul_list.append(np.array(lum.intens))
			# if len(coul_list) > 1:			#On applique la correction gamma si on a plusieurs lumieres
			# 	coul_list = self.correction_gamma(coul_list)
		return ray_lum_list, coul_list
	

	def lum_diffuse(self, obj, ray_lum_list, coul_list, normale):
			"""Renvoie les 3 cmposantes de la lumiere diffuse du point inter sur l'objet obj """
			if len(ray_lum_list) == 0:
				return (np.zeros(3, dtype = float))		#On renvoie 0 0 0 si aucune lumiere n'atteint le point
			somme = np.zeros(3, dtype = float)
			for i in range(len(ray_lum_list)):			#Calcul de la lumiere diffuse
					L = ray_lum_list[i]
					#print(L.composantes())		
					somme += coul_list[i] * L.prod_scal(normale)	#somme est un triplet
			return somme * obj.diff
			
				

	def lum_spec(self, ray_vue, obj, normale, ray_lum_list, coul_list, n):
		"""Renvoie les 3 composantes de la lumiere speculaire au point inter pour le ray_vue sur obj avec la liste des rayons de lumiere qui touchent le point ray_lum_list"""
		if len(ray_lum_list) == 0:
			return (np.zeros(3, dtype = float))		#On renvoie 0 0 0 si aucune lumiere n'atteint le point
		
		somme = np.zeros(3, dtype = float)
		for i in range(len(ray_lum_list)):
			lum_r = self.ray_reflechi(ray_lum_list[i] * -1, normale)
			somme += (lum_r.prod_scal(ray_vue)**n) * coul_list[i]
		return somme * obj.spec



	def phong(self, obj, inter, rayon_vue, n=100):  		
		'''Applique le modèle d'illumination de Phong à l'objet'''
		ray_lum_list, coul_list = self.recherche_ray_lum(inter)
		normale = obj.normale(inter)
		diffus = vecteur.Vecteur(extremite = self.lum_diffuse(obj, ray_lum_list, coul_list, normale))
		ambiant = self.Ia.mult_scal(self.ka)
		spec = vecteur.Vecteur(extremite = self.lum_spec(rayon_vue, obj, normale, ray_lum_list, coul_list, n)) #Speculaire a 0 pour l'instant donc rayon_vue et n ne servent pas pour l'instant
		
		res = ((ambiant.addition(diffus) * obj.coul).addition(spec)).composantes()
		for i in range(3):	
			if res[i] > 1:			#Corretion Gamma Moche
				res[i] = 1
		return res	

	def lancer_rayon(self, point, rayon):
		"""Algorithme de lancer de rayon, point est le point du plan de l'espace mathematique duquel part le rayon de vue rayon, mat_px est la matrice de pixels,
		Renvoie la couleur du pixel du point d'intersection si il existe"""
		iobj, inter = self.plus_proche_intersection(point, rayon) # Deuxieme etape : calcul des intersections (indice de l'objet qui a la plus proche intersection avec la cam)
		if iobj > -1 :
			obj = self.obj_list[iobj]
			return self.phong(obj, inter, rayon, 70) * 255
		else:
			return None


	def construire_image(self):
		"""Algorithme principal qui construit l'image"""
		self.cam.calcul_F()         #calul de F
		mat_px = np.full((self.cam.dim[1], self.cam.dim[0], 3), (0, 0, 0), dtype = np.uint8)  #On initialise la matrice de pixels à tout noir														#On doit inverser i et j dans la matrice de pixels a cause de PIL
		for i in range (self.cam.dim[0]):
			for j in range(self.cam.dim[1]):
				point, ray = self.cam.rayon((i,j))				#Premiere etape : calcul des rayons de vue
				px = self.lancer_rayon(point, ray)
				if np.any(px) != None:
					mat_px[j][i] = px						#On doit inverser i et j dans la matrice de pixels a cause de PIL

		data = im.fromarray(mat_px) #On prend la transposee car PIL et Numpy n'ont pas le meme systeme d'indicage
		data.save('test2.png')





if __name__ == "__main__":


	test = vecteur.Vecteur(extremite = (0.7,0.7,0.7))
	cam=test_camera.Camera(640,480,(-300,0,0),(-0.64279,0,-0.76604),(0,1,0),300) #Création de la Caméra
	list_obj=[sphere.Sphere((-300,0, -400), white, 0.7, 0.7, 0, 0, 250), sphere.Sphere((300,0, -400), brown, 0.7, 0.9, 0, 0, 300)] #Création de la liste d'objets
	list_obj.append(plan.Plan((0,0,1), (0, 0, -1000), (1, 1, 1), 0.7, 0.1, 0, 0))
	lumlist=[lumiere.Lumiere((0,0, -1),(0.9, 0.9, 0.9))] #Lumière blanche
	scen=Scene(vecteur.Vecteur(extremite = (0.7,0.7,0.7)), 0.2, cam, list_obj, lumlist) #Création de la Scène
	scen.construire_image() #appel fonction pour construire image


	#La scene de Nino

	# cam=camera.Camera(1280,720,(0,0,0),(1,0,0),(0,1,0),500) #Création de la Caméra
	# list_obj=[sphere.Sphere((0,0, -1200), (1,1,1), 0.7, 0.1, 0, 0, 1000), sphere.Sphere((-400,400,-400), (1,0,0), 0.7, 0.1, 0, 0, 150),sphere.Sphere((400,400, -400), (1,0,0), 0.7, 0.1, 0, 0, 150)] #Création de la liste d'objets
	# list_obj.append(plan.Plan((0,0,1), (0, 0, -3000), (0, 1, 1), 0.7, 0.1, 0, 0))
	# lumlist=[lumiere.Lumiere((0,0, -1),(0.9, 0.9, 0.9))] #Lumière blanche
	# scen=Scene(vecteur.Vecteur(extremite = (0.7,0.7,0.7)), 0.2, cam, list_obj, lumlist) #Création de la Scène
	# scen.construire_image() #appel fonction pour construire image

	#scene.construire_image()