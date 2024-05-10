import vecteur

class Camera:
    '''Camera definie par des dimensions (largeur, hauteur), une position (x,y,z), une direction (vecteur), une orientation (up vector), une distance focale (scalaire)'''
    def __init__(self, largeur, hauteur, position, direction, orientation, distance):
        self.dim = (largeur, hauteur)
        self.pos = vecteur.Point(position)
        self.dir = vecteur.Vecteur(direction)
        self.ori = orientation
        self.dis = distance
        self.F = None

    def calcul_F(self):
        """Calcule F le point focal et le met dans self.F"""
        tmp = self.dir.mult_scal(self.dis)
        self.F = self.pos.addition(tmp)
        

    def rayon(self, pplan):
        '''Renvoie le point (x, y z) et le rayon du point d'origine F vers un point pplan (x,y) du plan des dimensions de la camera'''
        C = self.pos
        
        #centre = vecteur.Point((0,0,0))
        #direct = vecteur.Vecteur(C.extr,self.dir)#.normalisation()
        #print(self.dir)
                                                                             #Si on veut pouvoir faire pivoter la camera
        l = self.dim[0]                                #Calcul du point Pxy 
        h = self.dim[1]
        H = vecteur.Vecteur(extremite = (0,1,0))
        D = vecteur.Vecteur(extremite = (1,0,0))
        P0 = C.addition(H * (h/2 - 0.5) - D * (l/2 - 0.5))

        Pxy = P0.soustraction((H * pplan[1])).addition(D * pplan[0])

        #V = vecteur.Vecteur(C.extr,centre.extr).normalisation()    
        
        #print(V)
        

        res = vecteur.Vecteur(self.F.extr, Pxy.extr)
        #print(res)
        return Pxy, res.normalisation()
    
if __name__ == "__main__":
    cam = Camera(11, 11, (0,0,0), (0,0,-1), (0,1,0), 5)
    cam.calcul_F()
    a = cam.rayon((5,0))
    print(a[0].extr, a[1].composantes())
    