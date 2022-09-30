#! /bin/python3

#from mpi4py import MPI


import numpy as np
import random
import time


nx = 100
ny = 100
nb_tirages = 100
valeurs_aux_bords = np.array([0.0,1.0,2.0,3.0])  # valeurs de la solution sur les bords y=0, x=nx, y=ny et x=0

def conditions_aux_bords(grille):  # Initialisation de la solution sur les bords
	for i in range(0,nx): # y = 0
		grille[i][0] = valeurs_aux_bords[0]

	for i in range(0,ny): # x = nx
		grille[nx-1][i] = valeurs_aux_bords[1]

	for i in range(0,nx): # y = ny
		grille[i][ny-1] = valeurs_aux_bords[2]

	for i in range(0,ny): # x = 0
		grille[i][0] = valeurs_aux_bords[3]

def calcul_solution(grille):
	random.seed(time.gmtime(0))
	for i in range(1, nx-1):
		for j in range(1, ny-1):
			for n in range(0,nb_tirages):
				#print(f"i = {i}, j = {j}, n = {n}\n")
				pos_x = i  # initialisation de la position x de la particule
				pos_y = j  # initialisation de la position y de la particule
				valeur = 0.0
				stop = 0   # vaudra 1 si un bord est atteint

				while stop != 1:
					decision = random.randrange(2)  # 0 ou 1
					if decision == 0:
						pos_x += 1
					else:
						pos_x -= 1 

					decision = random.randrange(2)  # 0 ou 1
					if decision == 1:
						pos_y += 1
					else:
						pos_y -= 1

					if (pos_x == 0) | (pos_x == nx - 1) | (pos_y == 0) | (pos_y == ny - 1):
						valeur = grille[pos_x][pos_y]
						stop = 1

				grille[i][j] += valeur
	grille /= nb_tirages

def ecriture(grille):
	fichier = open("monte_carlo.vtk","w")
	Nbnoe = nx*ny
	dx = 1.0/(nx-1);
	dy = 1.0/(ny-1);

	fichier.write("# vtk DataFile Version 2.0\n")
	fichier.write("Laplacien stochastique\n")
	fichier.write("ASCII\n")
	fichier.write("DATASET STRUCTURED_POINTS\n")
	fichier.write("DIMENSIONS %d %d 1\n" %(nx,ny))
	fichier.write("ORIGIN 0 0 0\n")
	fichier.write("SPACING %f %f 1\n" %(dx,dy))
	fichier.write("POINT_DATA %d\n" % Nbnoe)
	fichier.write("SCALARS Concentration float\n")
	fichier.write("LOOKUP_TABLE default\n")

	for i in range(0,nx):
		for j in range(0,ny):
			fichier.write("%f\n" % grille[i][j])
	fichier.close();			

def main():
	grille = np.zeros((nx,ny),dtype=float) # Initialisation de la solution
	t0 = time.time() 
	conditions_aux_bords(grille)
	calcul_solution(grille)
	t1 = time.time() 
	ecriture(grille)
	#print(grille)
	print(t1-t0)

	

main()
