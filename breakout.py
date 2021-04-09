# import des librairies
from tkinter import*
import random as rd

fenetre=Tk()
canvas=Canvas(fenetre,width=500,height=400,bd=0,bg='#A49172')       # crétion de la fenètre
canvas.pack(padx=10,pady=10)

#--------------------------------------------------------------------------------------------------#

class Balle:
    # création de balle
    def __init__(self,raquette,brick):
        self.xb1,self.yb1=240,350         
        self.xb2,self.yb2=self.xb1+20,self.yb1+20               # coordonnées et taille de la balle
        self.v=4         # vitesse de la balle
        
        if rd.randint(0,1)==0:
            self.dx=-self.v
        else:
            self.dx=self.v
        if rd.randint(0,1)==0:
            self.dy=-self.v
        else:
            self.dy=self.v
        self.balle=canvas.create_oval(self.xb1,self.yb1,self.xb2,self.yb2,fill='#D6CDBF')           # affichage de la balle
        self.raquette=raquette
        self.bricks=brick
    
    def animation_balle(self):
        # animation de la balle
        if self.bricks.fin==True:
            return self.victory()
        play=True
        coord_b=canvas.coords(self.balle)
        if coord_b[1]<0:
            self.dy=-self.dy
        if coord_b[0]<0 or coord_b[2]>500:
            self.dx=-self.dx
        if len(canvas.find_overlapping(coord_b[0],coord_b[1],coord_b[2],coord_b[3]))>1:
            self.dy=-self.dy
        if coord_b[3]>self.raquette.yr2+30:
            play=False
            self.defeat()
        
        canvas.move(self.balle,self.dx,self.dy)
        if play:
            self.bricks.destroy_brick()
            fenetre.after(20,self.animation_balle)
           
    def victory(self):
        # la partie est gagnée
        victory_text = Label(fenetre, text="Well done, you've won !", font=("Arial",20))
        victory_text.pack()
        btn=Button(fenetre, text="Quit", command=fenetre.destroy)
        btn.pack()

    def defeat(self):
        # la partie est perdu
        defeat_text = Label(fenetre, text="Game Over", font=("Arial",20))
        defeat_text.pack()
        btn=Button(fenetre, text="Quit", command=fenetre.destroy)
        btn.pack()

#--------------------------------------------------------------------------------------------------#

class Raquette:
    # création de la raquette
    def __init__(self):
        self.xr1,self.yr1,self.xr2,self.yr2=175,380,325,390                     # coordonnées et taille de la raquette
        self.raquette = canvas.create_rectangle(self.xr1,self.yr1,self.xr2,self.yr2,fill='#605645')         # affichage de la raquette
    
    def avance_raquette(self,event):
        # déplace la raquette vers la droite tant qu'elle ne dépasse pas les bordures de l'écran
        if canvas.coords(self.raquette)[2]<495:
            canvas.move(self.raquette,10,0)
    
    def recule_raquette(self,event):
        # déplace la raquette vers la gauche tant qu'elle ne dépasse pas les bordures de l'écran
        if canvas.coords(self.raquette)[0]>5:
            canvas.move(self.raquette,-10,0)

#--------------------------------------------------------------------------------------------------#

class Brick:
    # création des briques
    def __init__(self):
        self.bricks=[]
        self.wall=[]
        self.fin=False

    def draw_brick(self):
        # créé toutes les briques
        for i in range(50,150,30):
            for j in range(15,485,60):
                self.bricks.append((j,i))
        
    def put_brick(self):
        # place les briques sur l'écran
        for coord in self.bricks:
            xbr1=coord[0]
            ybr1=coord[1]
            xbr2=coord[0]+50
            ybr2=coord[1]+20                # coordonnées des briques
            brick=canvas.create_rectangle(xbr1,ybr1,xbr2,ybr2,fill='#91B483')       # affichage des briques
            self.wall.append({"brick":brick,"level":2})           # stocke les briques dans des dictionnaires composés des briques et de leur niveau égal à deux

    def destroy_brick(self):
        # change le niveau des briques à chaque collision avec la balle et les détruit lorsque le niveau est égal à zéro
        for dico_brick in self.wall:
            if len(canvas.find_overlapping(canvas.coords(dico_brick["brick"])[0],canvas.coords(dico_brick["brick"])[1],canvas.coords(dico_brick["brick"])[2],canvas.coords(dico_brick["brick"])[3]))>1:
                dico_brick["level"]-=1
            if dico_brick["level"]==0:
                canvas.delete(dico_brick["brick"])
                self.wall.pop(self.wall.index(dico_brick))
            if dico_brick["level"]==1:
                canvas.itemconfigure(dico_brick["brick"], fill="#B9E7A6")
            if self.wall==[]:
                self.fin=True

r=Raquette()  
brick=Brick()
b=Balle(r,brick)

brick.draw_brick()
b.animation_balle()
brick.put_brick()

fenetre.bind('<Left>',r.recule_raquette)
fenetre.bind('<Right>',r.avance_raquette)

fenetre.mainloop()
