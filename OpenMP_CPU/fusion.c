#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

/* Algorithme séquentiel qui effectue la recherche dichotomique du flottant x dans le tableau tab et qui retourne l'indice i tel que tab[i-1] < x < tab[i]*/ 
/* Complexité séquentielle en temps O(log2(n)*/ 
int dicho(float x, float tab[], int n)
{
	int iPremier;   /* Indice du premier élément du sous-tableau analysé     */  
	int iDernier;   /* Indice du dernier élément du sous-tableau analysé     */  
	int iMilieu;    /* Indice de l'élément du milieu du sous-tableau analysé */  
	int iTrouve;    /* Booléen indiquant si l'élément est trouvé             */  
	int iFin = 1;   /* Indication de fin de saisie (0=fin)                   */ 

	    
	/* Initialisation des variables*/       
	iPremier = 0;       
	iDernier = n;       
	iTrouve = 0;       
	/* Tant qu'on a pas trouve l'élément ou que le sous-tableau contient plus de 1 élément */       
	while((iPremier <= iDernier) && (iTrouve==0))       
	{        
	/* Calcul de la position de l'élément du milieu */   
		iMilieu = (iPremier + iDernier)/2;   
		/* Si l'élément du milieu est l'élément recherché */  
		/* Normalement en générant des flottants cela est très peu probable*/  
		if(tab[iMilieu] == x) 
		{
			iTrouve = 1;   
			return iMilieu; 
		}
		else     
		{       
		/* Si la valeur recherchée est plus petite que la valeur du l'élément du milieu  Alors on regarde le sous-tableau de gauche */       
			if(tab[iMilieu] > x) iDernier = iMilieu -1;       
			/* Sinon on regarde le sous-tableau de droite*/       
			else iPremier = iMilieu +1;    
		}     
	}             
	return iPremier; /* En effet à la fin iDernier et iPremier se seront inversés, on veut en fait iDernier*/  
}

/* Programme parallèle qui renvoie la position des éléments du tableau de flottants a si on les insérait dans le tableau de flottants b*/ 
/* Compléxité en temps en O(log2(n)) à cause de la recherche dichotomique et en processeurs O(n)*/ 
int *rank(float a[],float b[],int n)
{
	/* On initialise le tableau rank_ab de taille n et on lui alloue une mémoire dynamique*/ 
	int *rank_ab;
	rank_ab = malloc(n * sizeof(float));  

	/* On réalise la recherche dichotomique pour trouver la position d'insertion de chaque élément de a dans b en parallèle*/ 
	int i; 
#pragma omp parallel for 
	for (i = 0; i < n; i++)
	{
		rank_ab[i] = dicho(a[i], b, n); 
	}
	return rank_ab; 
}

/* Programme parallèle qui renvoie un nouveau tableau de flottants c résultant de la fusion triée des tableaux de flottants a et b.*/
/* Compléxité en temps en O(log2(n)) et en nombre de processeurs en O(n)*/  
float *fusion(float a[], float b[], int n)
{

	/* On initialise le tableau c de taille 2n et on lui alloue une mémoire dynamique*/ 
	float *c;
	c = malloc(2*n * sizeof(float));


	/* On initialise et calcule les tableaux rank_ab et rank_ba de taille n*/ 
	int *rank_ab;
	rank_ab = rank(a,b,n);
	int *rank_ba;
	rank_ba = rank(b,a,n); 

	/* On réalise la fusion des tableaux a et b dans c en parallèle*/ 
	int i; 
#pragma omp parallel for 
	for (i = 0; i < n; i++)
	{
		c[i+rank_ab[i]] = a[i];
		c[i+rank_ba[i]] = b[i]; 
	}
	return c; 
}


/* Programme principal qui prend en argument une taille de tableau n, crée aléatoirement des tableaux a et b triés de cette taille, les affiche, réalise leur fusion, et l'affiche.*/ 
/* Le seul calcul signifiable est celui de la fusion. Le programme est en temps en O(log2(n)) et en nombre de processeurs O(n)*/ 
int main(int argc, char const *argv[])
{

    float *a, *b;
    int n, i;

    /* Si l'utilisateur n'a pas donné de taille n on le signal et on sort du programme*/ 
    if (argc ==1)
	{
		printf(" On attend en paramètre le nombre de valeurs à traiter.\n");
		exit(2);
	}

	/* On determine n et on alloue la mémoire pour les tableaux a et b */
	n = atoi(argv[1]);
	a = malloc(n * sizeof(float));
	b = malloc(n * sizeof(float)); 

	/* On génère des valeurs aléatoires*/ 
	/* On aurait pu le faire en parallèle en utilisant l'algorithme du précédent ou de l'écart*/ 

	a[0] = (1.0*rand())/RAND_MAX;
	b[0] = (1.0*rand())/RAND_MAX;
	for(i = 1; i < n; i++)
	{
        a[i] = a[i-1] + (1.0*rand())/RAND_MAX;
    	b[i] = b[i-1] + (1.0*rand())/RAND_MAX;
    }
	/* Affichage des valeurs initiales */
    printf("On a genere %d valeurs initales pour a :", n);
        for(i = 0; i < n; i++)
                printf(" %f", a[i]);
	printf("\n");

	printf("On a genere %d valeurs initales pour b:", n);
        for(i = 0; i < n; i++)
                printf(" %f", b[i]);
	printf("\n");

	/* Fusionner les deux tableaux*/ 
	float *c;
	c = fusion(a, b, n);

  	/* Afficher ici le tableau final. */
  	printf("On a genere %d valeurs finales :", 2*n);
        for(i = 0; i < 2*n; i++)
                printf(" %f", *(c + i));
	printf("\n");
}