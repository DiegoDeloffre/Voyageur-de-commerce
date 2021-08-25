import math
import random
from numpy import *
from matplotlib.pyplot import *
import csv
from tkinter import *

class Ville:
   def __init__(self, x, y):
       self.x = x
       self.y = y
   
   def distance(self, ville):
       distance=math.sqrt((math.pow(ville.x-self.x,2))+(math.pow(ville.y-self.y,2)))
       return distance


class Individu:
    #cree un circuit vide
    def __init__(self, individu=None):
        self.individu = []
        self.efficacite = 0.0
        self.distance = 0
        if individu is not None:
            self.individu = individu
        else:
            for i in range(0, len(Villes)):
                self.individu.append(None)
   
    def __getitem__(self, index):
        return self.individu[index]
    
    def getVille(self, pos):
        return self.individu[pos]

    def setVille(self, pos, ville):
        self.individu[pos] = ville
        self.efficacite = 0.0
        self.distance = 0
        
    def tailleIndividu(self):
        return len(self.individu)

    def contientVille(self, ville):
        return ville in self.individu

    #cree un circuit avec toutes les villes et le melange
    def genererIndividu(self):
        for indiceVille in range(0, len(Villes)):
            self.setVille(indiceVille, Villes[indiceVille])
        random.shuffle(self.individu)

    #renvoie la valeur d efficacite du circuit 
    #plus la distance du circuit est faible et plus la valeur renvoyee sera elevee
    def getEfficacite(self):
        if self.efficacite == 0:
            self.efficacite = 1/float(self.getDistance())
        return self.efficacite

    #calcule la somme des distances entre les villes
    def getDistance(self):
        if self.distance == 0:
            distanceTot = 0
            for indiceVille in range(0, len(self.individu)):
                villeOrigine = self.getVille(indiceVille)
                villeArrivee = self.getVille(0)
                if indiceVille+1 < len(self.individu):
                    villeArrivee = self.getVille(indiceVille+1)
                else:
                    villeArrivee = self.getVille(0)
                distanceTot += villeOrigine.distance(villeArrivee)
            self.distance = distanceTot
        return self.distance
    
class Population:
    #Cree un ensemble de circuit
    def __init__(self, taillePopulation, init):
        self.circuits = []
        for i in range(0, taillePopulation):
            self.circuits.append(None)
        if init:
            for i in range(0, taillePopulation):
                nouveauCircuit = Individu()
                nouveauCircuit.genererIndividu()
                self.circuits[i] = nouveauCircuit
   
    #Calcule le circuit le plus efficace
    def getMeilleur(self):
        meilleur = self.circuits[0]
        for i in range(0, len(self.circuits)):
            if meilleur.getEfficacite() <= self.circuits[i].getEfficacite():
                meilleur = self.circuits[i]
        return meilleur
       
def evoluerPopulation(pop):
    nouvellePopulation = Population(len(pop.circuits), False)
    nouvellePopulation.circuits[0]=pop.getMeilleur()
              
    for i in range(1, len(nouvellePopulation.circuits)):
        parent1 = selectionVillesParents(pop)
        parent2 = selectionVillesParents(pop)
        enfant = croisement(parent1, parent2)
        nouvellePopulation.circuits[i]=enfant
          
    for i in range(1, len(nouvellePopulation.circuits)):
        mutation(nouvellePopulation.circuits[i])
              
    return nouvellePopulation    
    
    
def croisement(parent1, parent2):
    enfant = Individu()   
    borne1 = int(random.random() * parent1.tailleIndividu())
    borne2 = int(random.random() * parent1.tailleIndividu())
          
    for i in range(0, enfant.tailleIndividu()):
        if borne1 < borne2 and i > borne1 and i < borne2:
            enfant.setVille(i, parent1.getVille(i))
        elif borne1 > borne2:
            if not (i < borne1 and i > borne2):
                enfant.setVille(i, parent1.getVille(i))
          
    for i in range(0, parent2.tailleIndividu()):
        if not enfant.contientVille(parent2.getVille(i)):
            for ii in range(0, enfant.tailleIndividu()):
                if enfant.getVille(ii) == None:
                    enfant.setVille(ii, parent2.getVille(i))
                    break
    return enfant    
    
def selectionVillesParents(pop):
    selec = Population(nbVillesaComparer, False)
    for i in range(0, nbVillesaComparer):
        randomId = int(random.random() * len(pop.circuits))
        selec.circuits[i]=pop.circuits[randomId]
    meilleur = selec.getMeilleur()
    return meilleur
    
def mutation(circuit):
        for circuitPos1 in range(0, circuit.tailleIndividu()):
            if random.random() < tauxMutation:
                circuitPos2 = int(circuit.tailleIndividu() * random.random())
               
                ville1 = circuit.getVille(circuitPos1)
                ville2 = circuit.getVille(circuitPos2)
               
                circuit.setVille(circuitPos2, ville1)
                circuit.setVille(circuitPos1, ville2) 

def villes_aleatoires():
    random.seed(10)
    tabz=random.rand(nbvilles,2)
    for i in range (0,nbvilles):
        Villes.append(Ville(tabz[i][0], tabz[i][1]))
        
def defi_villes():
    Tableau = []
    cr = csv.reader(open('defi250.csv','rb'))
    for row in cr:
        Tableau.append(row)
        
    for i in range (1, 250):
        Villes.append(Ville(float(Tableau[i][0].split(';')[0]), float(Tableau[i][0].split(';')[1])))
    
def setNbvilles(var):
    global nbvilles
    nbvilles= int(var)
    
def setNbpops(var):
    global nbpops
    nbpops= int(var)
    
def setNbtours(var):
    global nbtours
    nbtours= int(var)
    
def setTauxMutation(var):
    global tauxMutation
    tauxMutation= float(var)
    
def setNbvillesAComparer(var):
    global nbVillesaComparer
    nbVillesaComparer= int(var)    

def choix():
    global choix
    choix =2
    fenetre.destroy()
    fen=Tk()
    cadre2 = Frame(fen, padx="500", height=500, borderwidth=1)
    
    label_nbv = Label(fen, text="Nombre d'individus (villes)")
    nbv = Scale(fen, orient='horizontal', from_=0, to=100,resolution=10, tickinterval=20, length=500,command=setNbvilles)

    label_nbp = Label(fen, text="Nombre de populations (circuits de villes)")
    nbp = Scale(fen, orient='horizontal', from_=0, to=100,resolution=10, tickinterval=20, length=500,command=setNbpops)
    
    label_nbt = Label(fen, text="Nombre de générations")
    nbt = Scale(fen, orient='horizontal', from_=0, to=500, resolution=10, tickinterval=100,length=500,command=setNbtours)
    
    label_tm = Label(fen, text="Taux de mutation")
    tm = Scale(fen, orient='horizontal', from_=0, to=0.5, resolution=0.01, tickinterval=0.1, length=500,command=setTauxMutation)
    
    label_nbvac = Label(fen, text="Nombre de villes à comparer pour sélectionner les parents")
    nbvac = Scale(fen, orient='horizontal', from_=0, to=20, resolution=1, tickinterval=5, length=500,command=setNbvillesAComparer)

    bouton_valider = Button(fen, text="Valider", command=fen.destroy)
    
    label_nbv.pack(pady=20)
    nbv.pack()
    label_nbp.pack(pady=20)
    nbp.pack()
    label_nbt.pack(pady=20)
    nbt.pack()
    label_tm.pack(pady=20)
    tm.pack()
    label_nbvac.pack(padx=100, pady=20)
    nbvac.pack()
    bouton_valider.pack(pady=20)

    fen.mainloop()
    
def defi():
    choix =1
    fenetre.destroy()
    fen=Tk()
    cadre2 = Frame(fen, padx="500", height=500, borderwidth=1)

    label_nbp = Label(fen, text="Nombre de populations (circuits de villes)")
    nbp = Scale(fen, orient='horizontal', from_=0, to=100,resolution=10, tickinterval=20, length=500,command=setNbpops)
    
    label_nbt = Label(fen, text="Nombre de générations")
    nbt = Scale(fen, orient='horizontal', from_=0, to=500, resolution=10, tickinterval=100,length=500,command=setNbtours)
    
    label_tm = Label(fen, text="Taux de mutation")
    tm = Scale(fen, orient='horizontal', from_=0, to=0.5, resolution=0.01, tickinterval=0.1, length=500,command=setTauxMutation)
    
    label_nbvac = Label(fen, text="Nombre de villes à comparer pour sélectionner les parents")
    nbvac = Scale(fen, orient='horizontal', from_=0, to=20, resolution=1, tickinterval=5, length=500,command=setNbvillesAComparer)

    bouton_valider = Button(fen, text="Valider", command=fen.destroy)

    label_nbp.pack(pady=20)
    nbp.pack()
    label_nbt.pack(pady=20)
    nbt.pack()
    label_tm.pack(pady=20)
    tm.pack()
    label_nbvac.pack(padx=100, pady=20)
    nbvac.pack()
    bouton_valider.pack(pady=20)

    fen.mainloop()


if __name__ == '__main__':
    
    #Creation d un ensemble de villes
    Villes = []
    distancesTots=[]
    
    fenetre = Tk()  
    cadre = Frame(fenetre,borderwidth=1)
    champ_label = Label(fenetre, text="Voulez-vous faire le défi des 250 villes")
    champ_label2 = Label(fenetre, text="ou générer des villes aléatoires ?")
    bouton_defi = Button(fenetre, text="Faire le defi", command=defi)
    bouton_choix = Button(fenetre, text="Generer les villes", command=choix)
    
    champ_label.pack(pady=30)
    champ_label2.pack()
    bouton_defi.pack(side=LEFT,padx=70,pady=30)
    bouton_choix.pack(side=RIGHT,padx=70)
    fenetre.mainloop()
    
     
    if(choix==2):
        villes_aleatoires()
    else:
        defi_villes()

    #on initialise la population avec 20 circuits
    pop = Population(nbpops, True)
    print "Distance initiale : " + str(pop.getMeilleur().getDistance())
   
    #Affiche le trajet du premier circuit
    figure(1)
    xpop = []
    ypop = []
    for ville in pop.circuits[0]:
        xpop.append(ville.x)
        ypop.append(ville.y)
    xpop.append(xpop[0])
    ypop.append(ypop[0])
    plot(xpop,ypop, color='r')
    title('Premier circuit')
    legend()
   
   
    # On fait evoluer notre population sur nbTours generations
    popFinales = evoluerPopulation(pop)
    
    for i in range(0, nbtours):
        popFinales = evoluerPopulation(popFinales)
        distancesTots.append(popFinales.getMeilleur().getDistance())
   
    print "Distance finale : " + str(popFinales.getMeilleur().getDistance())
    meilleurePopulation = popFinales.getMeilleur()

    #Affiche le trajet du meilleur circuit
    figure(2)
    xPopFinales = []
    yPopFinales = []
    for ville in meilleurePopulation.individu:
        xPopFinales.append(ville.x)
        yPopFinales.append(ville.y)
    xPopFinales.append(xPopFinales[0])
    yPopFinales.append(yPopFinales[0])
    plot(xPopFinales,yPopFinales, color='k')
    title('Dernier circuit')
    legend()

    c = 0
    m = 0
    while(distancesTots[m] <> meilleurePopulation.getDistance()):
        m = m + 1
        c = m
    print('Generation a partir de laquelle on atteint la meilleure distance : ' + str(c))
    
    #Affiche l evolution de la meilleure distance des circuits
    figure(3)
    nbTours = range(0,nbtours)
    plot(nbTours,distancesTots)
    title('Evolution des distances')
    xlabel("Nombre de generations")
    ylabel("Distance")
    legend() 
    grid()
    axvline(c, color='red')
    show()