import vecteur
import couleur
import sphere
import plan
import lumiere
import camera
import numpy as np

class Scene:

	def __init__(self, cam = None, Ia = None, ka = None, img = None):
		
		self.cam = cam
		self.obj_list = []
		self.lum_list = []
		self.Ia = Ia
		self.ka = ka
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
		'''Retourne la distance euclidienne entre les deux points (x, y, z)'''
		return ((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2 + (point2[2]-point1[2])**2)**0.5
	
	def plus_proche_intersection(self,point,rayon_vue):
		'''Renvoie l'indice de l'objet dans la liste d'objets qui a le point d'intersection le plus proche entre le rayon rayon_vue qui part du point point (eviter la focale) et la camera, 
		-1 si aucun point d'intersection n'est trouve'''
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
				distmin = self.dist_euclid(self.cam.pos.extr, intermin)
			i+=1

		while i<n:				#On parcourt les objets qu'il reste
			intertmp = self.obj_list[i].intersection(point,rayon_vue)
			if intertmp :
				disttmp = self.dist_euclid(self.cam.pos.extr, intertmp)
				if disttmp < distmin:							#On garde que la plus proche intersection
					imin = i
					intermin = intertmp
					distmin = disttmp
			i+=1
		return imin

	

	def modifier_camera(self, largeur, hauteur, position, direction, orientation, distance):
		'''Modifie la camera de la scene'''
		self.cam = camera.Camera(largeur, hauteur, position, direction, orientation, distance)
	
	def ray_reflechi(self, I, N):
		return I.addition(2 * ((-1 * I).prod_scal(N)) * N)
	
	def phong(self,obj,Ii,L,N,rayon_vue=None,n=100,R=None):
		'''applique le modèle d'illumination de Phong à l'objet'''
		Ia = self.Ia
		ka = self.ka
		kd = obj.diff
		ks = obj.spec
		V = rayon_vue
		print((Ia.mult_scal(ka)).composantes())
		print((Ii.mult_scal(kd*L.prod_scal(N) + ks*((R.prod_scal(V))**100))).composantes())
		return (Ia.mult_scal(ka)).addition(Ii.mult_scal(kd*L.prod_scal(N) + ks*((R.prod_scal(V))**100)))
		
	
	
	def construire_image(self):
		'''Algorithme principal qui construit l'image'''
		#tab_ray_vue = []		#Premiere etape : calcul des rayons de vue
		mat_px = np.full((self.cam.dim[0], self.cam.dim[1], 3), (255, 255, 255), dtype = list)  #On initialise la matrice de pixels à tout noir
		for i in range (self.cam.dim[0]):
			for j in range(self.cam.dim[1]):
				point, ray = self.cam.rayon((i,j))
				print("point = ", point, "rayon = ", ray)
				iobj = self.plus_proche_intersection(point, ray) #indice de l'objet qui a la plus proche intersection
				if iobj > -1 :
					print("-------------OUI--------------")
					mat_px[i][j] = self.obj_list[iobj].coul
		print(mat_px)


				


if __name__ == "__main__":
	# scene = Scene(Ia = vecteur.Vecteur(extremite = (0.7,0.7,0.7)), ka = 0.2)
	# scene.ajouter_sphere((0, 9-(1/(2**0.5)), -4-(1/(2**0.5))), (0,255,0), 0.7, 0.1, None, False, 1)
	# obj = scene.obj_list[0]
	# rayon_vue = vecteur.Vecteur(extremite = (0,0,-1))
	# Ii = vecteur.Vecteur(extremite = (0.9,0.1,0.1))
	# L = vecteur.Vecteur(extremite = (0,-3/(34**0.5),5/(34**0.5)))
	# N = vecteur.Vecteur(extremite = (0,1/(2**0.5),1/(2**0.5)))
	# R = scene.ray_reflechi(L, N)
	# #print(R.composantes())
	# #print ((scene.phong(obj = obj,rayon_vue = rayon_vue,Ii = Ii,L = L, R = R, N = N).composantes()))
	
	lum1 = lumiere.Lumiere((0,0,0), (1,1,1))
	lum2 = lumiere.Lumiere((0,0,0), (2,2,2))
	tab = [lum1, lum2]
	print(tab[0].coul)
	lum1.coul = (3,3,3)
	print(tab[0].coul)	
	

