#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

/* Fonction qui renvoie 1 si le tableau est trié et 0 sinon*/ 
/*Compléxité en O(1) en temps et en O(N) en nombre de processeurs*/
int test_trie(float a[],int N)
{
	int i, j ;  
	int boolean = 1; 

	/*En parallèle, si le suivant est plus petit que le précédent dans a alors le programme retournera 0 = faux*/ 
	#pragma omp parallel for 
		for  (i = 1; i<N; i++)
		{
			if (a[i] < a[i-1])
				boolean = 0; 
		}
	return boolean;  
}

/* Programme principal qui prend en argument la taille n de tableau, demande ensuite les valeurs du tableau de flottants à l'utilisateur, les affiche, et affiche si celui-ci est trié ou non*/ 
/* Complèxité en temps en O(1) et en nombre de processeurs en O(n)*/ 
int main(int argc, char const *argv[])
{

    float *a;
    int n, i;

    if (argc ==1)
	{
		printf(" On attend en paramètre le nombre de valeurs à traiter.\n");
		exit(2);
	}

	/* on determine n et on alloue la mémoire pour le tableau */
	n = atoi(argv[1]);
	a = malloc(n * sizeof(float));

	/* on demande les valeurs pour le tableau*/ 
	printf("Donner les valeurs"); 
	for(i=0; i < n; i++)
        scanf("%f", &a[i]);

	/* affichage des valeurs initiales */
    printf("Voici le tableau initial");
    for(i=0; i < n; i++)
        printf(" %f", a[i]);
	printf("\n");

	/* mettre ici le traitement du tableau */ 
	int test; 
	test = test_trie(a, n); 

  	/* Dire si le tableau est trié ou non */
  	if (test == 1)
  		{
  		printf("le tableau est trié\n");
  		return 1;
  		} 
  	else 
  		{
  		printf("le tableau n'est pas trié\n");
  		return 0;
  		}  
}