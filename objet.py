import math
import numpy as np


	
	
class Vecteur:
	'''Classe decrivant des vecteurs à 3 dimensions (x, y, z)'''
	def __init__(self, origine = (0,0,0), extremite = (0,0,0)):  #Origine et extremite sont des points (x,y,z)
		self.org = np.array(origine, dtype = float)
		self.extr = np.array(extremite, dtype = float)

	def __add__(self, vec):
		return self.addition(vec)

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
		self.org = coords
		self.extr = coords

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
		
	
class Sphere(Objet3D):
		
	def __init__(self,pos,coul,diff,spec,ref,ombre,rayon):
		
		self.centre = pos
		self.coul = coul
		self.diff = diff
		self.spec = spec
		self.ref = ref
		self.ombre = ombre
		self.rayon = rayon
		
		
	
	def intersection(self,droite):
		'''implementation de intersection pour la sous-classe sphere. Le parametre "droite" est compose d'un point (tuple a 3 dimensions) et d'une instance de Vecteur'''
		#on part du point
		D = droite.composantes()
		print("D=",D)
		#t est implicite
		M = droite.org
		print("M=",M)
		C = self.centre
		print("C=",C)
		v_eq = (M[0] - C[0], M[1] - C[1], M[2] - C[2])
		
		a = D[0]**2 + D[1]**2 + D[2]**2
		b = 2*v_eq[0]*D[0] + 2*v_eq[1]*D[1] + 2*v_eq[2]*D[2]
		c = v_eq[0]**2 + v_eq[1]**2 + v_eq[2]**2 - self.rayon
		print("a=",a,"b=",b,"c=",c)
		delta = b**2 - 4*a*c
		print("Delta=",delta)
		if delta < 0:
			return "pas de point d'intersection"
			
		elif delta == 0:
			t = -b/2*a
			
		
		else:
			t1 = (-b - delta**(1/2))/2*a
			t2 = (-b + delta**(1/2))/2*a
			t = min(t1,t2)
			
		return (M[0] + t*D[0], M[1] + t*D[1], M[2] + t*D[2])	
		
		
	def normale(self,point):
		'''implementation de normale pour la sous-classe sphere'''
	
		l,m,n = self.centre[0],self.centre[1],self.centre[2]
		xi,yi,zi = point[0],point[1],point[2]
		r = self.rayon
		return Vecteur((0,0,0),(((xi-l)/r),((yi-m)/r),((zi-n)/r))).composantes()

class Plan(Objet3D):
	def __init__(self, normale, pos, coul, diff, spec, ref, ombre):
		self.norm = normale
		self.pos = pos
		self.coul = coul
		self.diff = diff
		self.spec = spec
		self.ref = ref
		self.ombre = ombre

	def intersection(self, point, rayon_vue):
		'''Renvoie l'intersection entre le plan (self) et un rayon de vue deja calcule par camera.rayon(point) par rapport à un point'''
		#Rayon envoye depuis le point P et non la focale F !!!

		A = self.norm[0]
		B = self.norm[1]
		C = self.norm[2]
		x = self.pos[0]
		y = self.pos[1]
		z = self.pos[2]
		v = rayon_vue
		i = v[0]
		j = v[1]
		k = v[2]

		D = -1 * (A*x + B*y + C*z)
		P = point
		x1 = point[0]
		y1 = point[1]
		z1 = point[2]


		t = -1 * ((A*x1 + B*y1 + C*z1 + D) / (A*i + B*j + C*k))

		xres = x1 + v[0]*t
		yres = y1 + v[1]*t
		zres = z1 + v[2]*t

		return (xres,yres,zres)

		def normale(self):
			'''Renvoie la normale au plan'''
			return self.norm		
		
class Lumiere:
	'''Lumiere definie par une position et une couleur'''
	def __init__(self, position, couleur):
		self.pos = posiporgtion
		self.coul = couleur

class Camera:
	'''Camera definie par des dimensions (largeur, hauteur), une position (x,y,z), une direction (vecteur), une orientation (up vector), une distance focale (scalaire)'''
	def __init__(self, largeur, hauteur, position, direction, orientation, distance):
		self.dim = (largeur, hauteur)
		self.pos = position
		self.dir = direction
		self.ori = orientation
		self.dis = distance

	def rayon(self, plan, pplan):
		'''Renvoie le rayon du point d'origine F vers un point pplan (x,y) du plan plan (dimx, dimy)'''
		C = Point(self.pos)
		F =  self.pos + self.dis
		l = plan[0]
		h = plan[1]
		H = Vecteur(extremite = (0,1,0))
		D = Vecteur(extremite = (1,0,0))
		tmp = H * (h/2 - 1/2) - D * (l/2 - 1/2)
		P0 = C.addition(tmp).extr

		if pplan == (0,0):
			return P0

		return (P0[0] + pplan[0], P0[1] - pplan[1], 0)
        
class Scene:

	def __init__(self,cam,obj_list,lum_list,amb,img):
		
		self.cam = cam
		self.obj_list = obj_list
		self.lum_list = lum_list
		self.amb = amb
		self.img = img
		
sphere1 = Sphere((0,9 - 1/(2**(1/2)),-4-1/(2**(1/2))),None,None,None,None,None, 1)
rayon_vue = Vecteur((0,5,0),(0,5+ 1/(2**(1/2)),-1/(2**(1/2))))
print(sphere1.normale(sphere1.intersection(rayon_vue)))	
			
