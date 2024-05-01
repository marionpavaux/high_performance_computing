from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nb_proc = comm.Get_size()

import numpy as np
import random
import time

# define the mesh
nx = 100
ny = 100
# define the number of monte carlo iterations
nb_tirages = 100

valeurs_aux_bords = np.array([0.0, 1.0, 2.0, 3.0])  # valeurs de la solution sur les bords y=0, x=nx, y=ny et x=0


def partitionnement(n, bornes):
    bornes[0] = rank * n // nb_proc  # début
    bornes[1] = (rank + 1) * n // nb_proc - 1  # fin

    print(f"Process {rank}, début = {bornes[0]}, fin = {bornes[1]}\n")


def conditions_aux_bords(grille, bornesx, bornesy):  # Initialisation de la solution sur les bords
    for i in range(0, nx):  # de 0 à 100 exclu
        grille[0][i] = valeurs_aux_bords[0]  # y = 0
        grille[ny - 1][i] = valeurs_aux_bords[2]  # y = ny

    for i in range(0, ny):  # de 0 à 100 exclu
        grille[i][nx - 1] = valeurs_aux_bords[1]  # x = nx
        grille[i][0] = valeurs_aux_bords[3]  # x = 0


def calcul_solution(grille_partielle, bornesx):
    random.seed(time.gmtime(0))
    TAG = 20
    for j in range(bornesx[0], bornesx[1] + 1):  # d
        if (j != 0) and (j != nx - 1):
            for i in range(1, ny - 1):  # de 1 à 98
                for n in range(0, nb_tirages):
                    # print(f"i = {i}, j = {j}, n = {n}\n")
                    pos_x = i  # initialisation de la position x de la particule
                    pos_y = j  # initialisation de la position y de la particule
                    stop = 0  # vaudra 1 si un bord est atteint

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

                        if (pos_x == 0) or (pos_x == nx - 1) or (pos_y == 0) or (pos_y == ny - 1):
                            valeur = grille_partielle[pos_x][pos_y]  # valeur aux bords
                            stop = 1

                    grille_partielle[i][j] += valeur
                grille_partielle[i][j] = grille_partielle[i][j] / nb_tirages


def communication_optimale(grille_partielle):
    inc = 1
    dernier = nb_proc - 1
    grille = grille_partielle.copy()
    TAG = 1

    while inc <= nb_proc // 2:
        if (rank % (2 * inc) == inc) & (rank <= dernier):
            comm.Send([grille_partielle, MPI.FLOAT], dest=rank - inc, tag=TAG)
        elif (rank + inc <= dernier) & (rank % (2 * inc) == 0):
            grillerecue = np.empty((nx, ny), dtype=float)
            comm.Recv([grillerecue, MPI.FLOAT], source=rank + inc, tag=TAG)
            grille[1 : ny - 1, 1 : nx - 1] += grillerecue[1 : ny - 1, 1 : nx - 1]

        # Cas du dernier processus
        if dernier % (2 * inc) == inc:
            dernier -= inc
        else:
            TAG2 = 2
            if rank == dernier:
                comm.Send([grille_partielle, MPI.FLOAT], dest=0, tag=TAG2)
            if rank == 0:
                grillerecue = np.empty((nx, ny), dtype=float)
                comm.Recv([grillerecue, MPI.FLOAT], source=dernier, tag=TAG2)
                grille[1 : ny - 1, 1 : nx - 1] += grillerecue[1 : ny - 1, 1 : nx - 1]
            dernier -= 2 * inc
        inc *= 2

    # Distribution dans l'autre sens
    inc = inc / 2
    dernier = 0
    while inc >= 1:
        if (rank % (2 * inc) == 0) & (rank <= dernier) & (rank + inc < nb_proc):
            comm.Send([grille_partielle, MPI.FLOAT], dest=rank + inc, tag=TAG)
        elif (rank - inc <= dernier) & (rank % (2 * inc) == inc):
            grillerecue = np.empty((nx, ny), dtype=float)
            comm.Recv([grillerecue, MPI.FLOAT], source=rank - inc, tag=TAG)

        dernier += inc
        if dernier + inc < nb_proc:
            dernier += inc
            TAG2 = 2
            if rank == 0:
                comm.Send([grille_partielle, MPI.FLOAT], dest=dernier, tag=TAG2)

            if rank == dernier:
                grillerecue = np.empty((nx, ny), dtype=float)
                comm.Recv([grillerecue, MPI.FLOAT], source=0, tag=TAG2)
        inc = inc // 2

    return grille


def ecriture(grille):
    fichier = open("monte_carlo.vtk", "w")
    Nbnoe = nx * ny
    dx = 1.0 / (nx - 1)
    dy = 1.0 / (ny - 1)

    fichier.write("# vtk DataFile Version 2.0\n")
    fichier.write("Laplacien stochastique\n")
    fichier.write("ASCII\n")
    fichier.write("DATASET STRUCTURED_POINTS\n")
    fichier.write("DIMENSIONS %d %d 1\n" % (nx, ny))
    fichier.write("ORIGIN 0 0 0\n")
    fichier.write("SPACING %f %f 1\n" % (dx, dy))
    fichier.write("POINT_DATA %d\n" % Nbnoe)
    fichier.write("SCALARS Concentration float\n")
    fichier.write("LOOKUP_TABLE default\n")

    bornesx = [0, 0]
    bornesx = partitionnement(nx, bornesx)
    # for i in range(bornesx[0],bornesx[1] +1):
    for i in range(0, nx):
        for j in range(0, ny):
            fichier.write("%f\n" % grille[i][j])
    fichier.close()


def main():

    grille_partielle = np.zeros((nx, ny), dtype=float)  # Initialisation de la solution
    bornesx = [0, 0]
    t0 = MPI.Wtime()
    partitionnement(nx, bornesx)

    bornesy = [0, 0]
    partitionnement(ny, bornesy)

    conditions_aux_bords(grille_partielle, bornesx, bornesy)
    # print(f'Process {rank}, grille_partielle = {grille_partielle}')
    comm.Barrier()

    calcul_solution(grille_partielle, bornesx)

    print(f"Process {rank}, grille_partielle = {grille_partielle}")
    comm.Barrier()

    grille = np.zeros_like(grille_partielle)
    comm.Reduce([grille_partielle, MPI.DOUBLE], [grille, MPI.DOUBLE], MPI.SUM, root=0)
    conditions_aux_bords(grille, bornesx, bornesy)
    # grille = communication_optimale(grille_partielle)
    t1 = MPI.Wtime()
    comm.Barrier()
    if rank == 0:
        print(f"Communication optimale, process {rank}, grille = {grille}, temps = {t1-t0} s\n")
        ecriture(grille)

    Result = open("results/result.dat", "a")
    Result.write("%2d,%2d, %12.6e\n" % (nb_proc, rank, (t1 - t0)))
    Result.close()

    comm.Barrier()


main()
