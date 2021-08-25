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


if __name__ == '__main__':
    
    #Creation d un ensemble de villes
    Villes = []
    distancesTots=[]
    
    nbvilles=40
    nbpops=100
    nbtours=200
    tauxMutation=0.02
    nbVillesaComparer=10
    
    villes_aleatoires()
    #defi_villes()

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