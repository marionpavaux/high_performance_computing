# -*- coding: utf-8 -*-
"""
Created on Thu May  6 19:52:32 2021

@author: mario
"""

import matplotlib.pyplot as plt
import numpy as np


temps_seq = 1082

fichier = open("results/result.dat", "r")
p = []
temps = []
for ligne in fichier:
    donnee = [str(d) for d in ligne.split(",")]
    nb_proc, rank, t = float(donnee[0]), float(donnee[1]), float(donnee[2])
    p.append(nb_proc)
    temps.append(t)


fichier.close()


temps = np.array(temps)
speed_up = np.array(temps_seq / temps)
efficacite = np.array(speed_up / p)

print(speed_up)
print(efficacite)

# afficher les images
plt.figure()

# afficher le speed_up
plt.subplot(2, 1, 1)

plt.plot(p, p, "r", label="y=p")
plt.plot(p, speed_up, label="Speed up")

plt.grid()
plt.legend()
plt.title("Speed_up(p)")

# afficher l'efficacité
plt.subplot(2, 1, 2)
plt.plot(p, efficacite)
plt.grid()
plt.title("Efficacite(p)")

plt.show()
