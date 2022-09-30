import numpy as np
import matplotlib.pyplot as plt
import os
#Fichier qui exécute les fonctions de filtre en fonction de différents paramètres 
#et trace leur influence sur le temps de calcul ! 


#Ecarsement des fichiers existants 
data_mean= open('filtermean.txt',"w")
data_mean.close()
data_mean_improved= open('filtermeanimproved.txt',"w")
data_mean_improved.close()
data_gaussian= open('filtergaussian.txt',"w")
data_gaussian.close()
data_gaussian_improved= open('filtergaussianimproved.txt',"w")
data_gaussian_improved.close()

#Ecriture dans le terminal 
os.system("echo calcul filtre moyenneur sur gpu")
os.system("echo '...compilation'")
#os.system('module load cuda/10.1')
#os.system('scl enable devtoolset-8 bash')
os.system('cmake -g .')
os.system('make')

inff = 3 
supf = 26

#Execution pour différentes tailles de filtres 
os.system("echo '...execution pour filtre mean et filtre mean amélioré en fonction de différentes tailles du filtre'")
for f in range(inff,supf,2):
	command = './imageCopyFilter -k filtermean -s %02d' %f
	os.system(command)
	command = './imageCopyFilter -k filtermeanimproved -s %02d' %f
	os.system(command)

os.system("echo '...execution pour filtre gaussian et filtre gaussian amélioré en fonction de la taille du filtre'")
for f in range(inff,supf,2):
	command = './imageCopyFilter -k filtergaussian -s %02d' %f
	os.system(command)
	command = './imageCopyFilter -k filtergaussianimproved -s %02d' %f
	os.system(command)

#Execution pour différentes tailles de workgroup 
os.system("echo '...execution pour filtre mean et filtre mean amélioré en fonction de différentes tailles du workgroup'")
wtableau = [2,4,8,16,32] 
for w in wtableau:
	command = './imageCopyFilter -k filtermean -w %02d' %w
	os.system(command)
	command = './imageCopyFilter -k filtermeanimproved -w %02d' %w
	os.system(command)

os.system("echo '...execution pour filtre gaussian et filtre gaussian amélioré en fonction de différentes tailles du workgroup'")
for w in wtableau:
	command = './imageCopyFilter -k filtergaussian -w %02d' %w
	os.system(command)
	command = './imageCopyFilter -k filtergaussianimproved -w %02d' %w
	os.system(command)

#Analyse des résultats 
os.system("echo '...analyse des resultats'")
#Ouverture des fichiers 
data_mean=np.loadtxt('./filtermean.txt')
data_mean_improved=np.loadtxt('./filtermeanimproved.txt')
data_gaussian=np.loadtxt('./filtergaussian.txt')
data_gaussian_improved=np.loadtxt('./filtergaussianimproved.txt')
print("shape",data_mean.shape)
dimdata=data_mean.shape
nblines  =dimdata[0]
nbthreads=dimdata[1]

endf = (supf - inff)//2 + 1 
beginw = endf + 1 

#figure 1 est temps en fonction de la taille du filtre, filtre mean
mycol=['red','blue','green','orange','cyan','purple','red','blue','black']
plt.figure(1)
plt.clf()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('$\log(N)$')
plt.ylabel('$\log(t [s])$')
plt.plot(data_mean[:endf,1],data_mean[:endf,2],'ro-',label='non improved')
plt.plot(data_mean_improved[:endf,1],data_mean_improved[:endf,2],'go-',label='improved')

plt.title("Mean Filter - Excecution time depending \n on the filter size (workgroup = 32)")
plt.legend(loc='best')
plt.savefig('time_mean_filter.png',dpi=400)
plt.close(1)

#figure 2 est temps en fonction de la taille du filtre, filtre gaussian
plt.figure(2)
plt.clf()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('$\log(N)$')
plt.ylabel('$\log(t [s])$')
plt.plot(data_gaussian[:endf,1],data_gaussian[:endf,2],'ro-',label='non improved')
plt.plot(data_gaussian_improved[:endf,1],data_gaussian_improved[:endf,2],'go-',label='improved')

plt.title("Gaussian Filter - Excecution time depending \n on the filter size (workgroup = 32)")
plt.legend(loc='best')
plt.savefig('time_gaussian_filter.png',dpi=400)
plt.close(2)


#figure 3 est temps en fonction de la taille du workgroup, filtre mean
plt.figure(3)
plt.clf()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('$\log(N)$')
plt.ylabel('$\log(t [s])$')
plt.plot(data_mean[beginw:,0],data_mean[beginw:,2],'ro-',label='non improved')
plt.plot(data_mean_improved[beginw:,0],data_mean_improved[beginw:,2],'go-',label='improved')

plt.title("Mean Filter - Excecution time depending \n on the size of the workgroup (filter size = 3)")
plt.legend(loc='best')
plt.savefig('time_mean_workgroup.png',dpi=400)
plt.close(3)

#figure 4 est temps en fonction de la taille du workgroup, filtre gaussian
plt.figure(4)
plt.clf()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('$\log(N)$')
plt.ylabel('$\log(t [s])$')
plt.plot(data_gaussian[beginw:,0],data_gaussian[beginw:,2],'ro-',label='non improved')
plt.plot(data_gaussian_improved[beginw:,0],data_gaussian_improved[beginw:,2],'go-',label='improved')

plt.title("Gaussian Filter - Excecution time depending \n on the size of the workgroup (filter size = 3)")
plt.legend(loc='best')
plt.savefig('time_gaussian_workgroup.png',dpi=400)
plt.close(4)

os.system("echo")
os.system("echo '----script ended'")
