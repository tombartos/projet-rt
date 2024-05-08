import objet3D
import vecteur

class Sphere(objet3D.Objet3D):
		
	def __init__(self,pos,coul,diff,spec,ref,ombre,rayon):
		
		self.centre = pos
		self.coul = coul
		self.diff = diff
		self.spec = spec
		self.ref = ref
		self.ombre = ombre
		self.rayon = rayon
		
		
	
	def intersection(self,point,rayon_vue):
		'''implementation de intersection pour la sous-classe sphere. Le parametre "droite" est compose d'un point (tuple a 3 dimensions) et d'une instance de Vecteur
		Renvoie les coordonnees du point d'intersection si il existe, None sinon'''
		#on part du point
		D = rayon_vue
		#print("D=",D)
		#t est implicite
		M = point
		#print("M=",M)
		C = self.centre
		#print("C=",C)
		v_eq = (M[0] - C[0], M[1] - C[1], M[2] - C[2])
		
		a = D[0]**2 + D[1]**2 + D[2]**2
		b = 2*v_eq[0]*D[0] + 2*v_eq[1]*D[1] + 2*v_eq[2]*D[2]
		c = v_eq[0]**2 + v_eq[1]**2 + v_eq[2]**2 - (self.rayon**2)
		#print("a=",a,"b=",b,"c=",c)
		delta = b**2 - 4*a*c
		#print("Delta=",delta)
		if delta < 0:
			return False					#pas de point d'intersection
			
		elif delta == 0:
			t = -b/(a<<1)
			if t<1:
				return False
			
		
		else:
			t1 = (-b - delta**(0.5))/(2*a)
			t2 = (-b + delta**(0.5))/(2*a)
			if (t1 < 1) and (t2 < 1):
				return False
			elif t1 < 1:
				t = t2
			elif t2 < 1:
				t = t1
			else: 
				t = min(t1,t2)
			
		return (M[0] + t*D[0], M[1] + t*D[1], M[2] + t*D[2])	
		
		
	def normale(self, point):
		'''implementation de normale pour la sous-classe sphere'''
		l,m,n = self.centre[0],self.centre[1],self.centre[2]
		xi,yi,zi = point[0],point[1],point[2]
		r = self.rayon
		return vecteur.Vecteur((0,0,0),(((xi-l)/r),((yi-m)/r),((zi-n)/r))).normalisation()


if __name__ == '__main__':
	test = Sphere((200, 200, -100), (0,255,0), None, None, None, False, 70)
	print(test.normale())
