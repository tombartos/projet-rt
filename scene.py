import vecteur
import couleur
import sphere
import plan
import lumiere
import camera
import numpy as np
from PIL import Image as im

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
				distmin = self.dist_euclid(point.extr, intermin)
				if distmin > 1:							#Securite pour les approximations des points, si a cause d'une approximation on a un point censé etre a la surface d'un objet
					imin = i							#Mais qui se retrouve en fait a l'interieur de cet objet, et trouve donc une intersection avec ce meme objet
														#On verifie que la distance soit superieur a un certain seuil, ici 1 pour considerer que c'est une vraie intersection
			i+=1										#Et pas une erreur d'approximation

		while i<n:				#On parcourt les objets qu'il reste
			intertmp = self.obj_list[i].intersection(point.extr,rayon_vue.composantes())
			if intertmp :
				disttmp = self.dist_euclid(point.extr, intertmp)
				if (disttmp > 1) and (disttmp < distmin):							#On garde que la plus proche intersection
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
	
	def correction_gamma(self, coul_list):
		"""Renvoie la liste des couleurs contenues dans coul_list mais auquelles on a appliqué une correction gamma ENTRE 0 ET 1"""
		print("gamma")
		coul_list = np.array(coul_list)
		n = len(coul_list)
		max = np.max(coul_list)		#On cherche le max 
		res = coul_list / max
		res = res ** 2.2
		return res

	
	def lum_diffuse(self, inter, obj):
			"""Renvoie les 3 cmposantes de la lumiere diffuse du point inter sur l'objet obj"""
			ray_lum_list = []				#Liste des lumieres dont les rayons vont intersecter l'objet
			#inter = np.round(inter)
			#print(inter)
			for lum in self.lum_list:
				ray_obj_lum = vecteur.Vecteur(inter, lum.pos).normalisation()

				jobj, jinter = self.plus_proche_intersection(vecteur.Point(inter), ray_obj_lum) #On cherche si un objet se trouve sur le rayon de lumiere dans le sens objet -> lumiere
				#print(jobj, jinter)
				if jobj == -1 :										#Pas d'objet entre notre point et notre lumiere, on est bon
					ray_lum_list.append(lum)
				else:											#Un objet est sur la demi droite, il faut verifier si il est avant ou apres la lumiere par rapport au point
					a = self.dist_euclid(inter, lum.pos)
					b = self.dist_euclid(inter, jinter)
					if a < b : 			#Lumiere plus proche que l'autre objet, on est bon
						ray_lum_list.append(lum)
			if len(ray_lum_list) > 0:	#Calcul de la lumiere diffuse
				kd = obj.diff
				N = obj.normale(inter)
				somme = np.zeros(3, dtype = float)
				coul_list = []
				for lum in ray_lum_list:
					coul_list.append(lum.intens)
				if len(coul_list) > 1:			#On applique la correction gamma si on a plusieurs lumieres
					coul_list = self.correction_gamma(coul_list)		

				for i in range(len(ray_lum_list)):
    					Ii = np.array(coul_list[i])
    					L = vecteur.Vecteur(ray_lum_list[i].pos, inter).normalisation()
    					#print(L.composantes())
    					dot_product = max(L.prod_scal(N),0)
    					somme += Ii * kd * dot_product			#somme est un triplet
				res = somme * kd
				print(res)
				return res
			return np.zeros(3, dtype = float)		#On renvoie 0 0 0 si aucune lumiere n'atteint le point
				



	def phong(self, obj, inter, rayon_vue = None, n=100):  		
		'''Applique le modèle d'illumination de Phong à l'objet'''
		diffus = vecteur.Vecteur(extremite = self.lum_diffuse(inter, obj))
		ambiant = self.Ia.mult_scal(self.ka)
		spec = vecteur.Vecteur(extremite = (0, 0, 0)) #Speculaire a 0 pour l'instant donc rayon_vue et n ne servent pas pour l'instant
		return (ambiant.addition(diffus).addition(spec)).composantes()	* obj.coul				#Idee pour spec : calculer les R de L directement dans self.lum_diff et les retourner

	def lancer_rayon(self, point, rayon):
		"""Algorithme de lancer de rayon, point est le point du plan de l'espace mathematique duquel part le rayon de vue rayon, mat_px est la matrice de pixels,
		Renvoie la couleur du pixel du point d'intersection si il existe"""
		iobj, inter = self.plus_proche_intersection(point, rayon) # Deuxieme etape : calcul des intersections (indice de l'objet qui a la plus proche intersection avec la cam)
		if iobj > -1 :
			obj = self.obj_list[iobj]
			return self.phong(obj, inter, rayon) * 255
		else:
			return None


	def construire_image(self):
		"""Algorithme principal qui construit l'image"""
		mat_px = np.full((self.cam.dim[1], self.cam.dim[0], 3), (0, 0, 0), dtype = np.uint8)  #On initialise la matrice de pixels à tout noir														#On doit inverser i et j dans la matrice de pixels a cause de PIL
		for i in range (self.cam.dim[0]):
			for j in range(self.cam.dim[1]):
				point, ray = self.cam.rayon((i,j))				#Premiere etape : calcul des rayons de vue
				px = self.lancer_rayon(point, ray)
				if np.any(px) != None:
					mat_px[j][i] = px						#On doit inverser i et j dans la matrice de pixels a cause de PIL

		data = im.fromarray(mat_px) #On prend la transposee car PIL et Numpy n'ont pas le meme systeme d'indicage
		data.save('output.png')





if __name__ == "__main__":
	#dim = (600,400)			#Dimensions de l'image

	cam=camera.Camera(320,240,(0,0,0),(1,0,0),(0,1,0),700) #Création de la Caméra
	list_obj=[sphere.Sphere((-100,0, -200), (0,1,0), 0.7, 0.1, 0, 0, 100), sphere.Sphere((100,0,-200), (1,0,0), 0.7, 0.1, 0, 0, 150)] #Création de la liste d'objets
	#list_obj.append(plan.Plan((0,0,1), (0, 0, 100), (0, 0, 1), 0.7, 0.1, 0, 0))
	lumlist=[lumiere.Lumiere((0,400,-200),(0.9, 0.1, 0.1))] #Lumière blanche
	scen=Scene(vecteur.Vecteur(extremite = (0.7,0.7,0.7)), 0.2, cam, list_obj, lumlist) #Création de la Scène
	scen.construire_image() #appel fonction pour construire image

	#scene.construire_image()
