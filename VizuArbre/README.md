### Fonctionnalités

- VizuArbre est une surcouche sur graphviz qui permet d'afficher rapidement et simplement un arbre binaire implémenté par une classe.

- Il est également possible d'afficher facilement des étiquettes secondaires sur les noeuds (typiquement l'ordre des visites lors d'un parcours). D'autres attributs (couleurs, forme des noeuds) sont également paramétrables facilement.

- Il est possible d'exporter les graphiques produits dans différents formats aussi bien bitmap (png, tiff) que vectoriels (svg et ps).

- Pour s'adapter à la classe d'arbre binaire définie par l'utilisateur, il faut néanmoins modifier l'en-tête du module `vizu_arbre.py` afin de spécifier l'interface implémentée par la classe :
	- la façon dont on accède au sous-arbre droit,
	- la façon dont on accède au sous-arbre gauche,
	- la façon dont on accède à l'étiquette de l'arbre,
	- la façon dont on teste l'arbre vide.

- Le dossier VizuArbre contient le module (`vizu_arbreb.py`) ainsi qu'un notebook de prise en main.
	
- Le dossier Algos_Arbres_en_NSI contient un notebook d'exemples d'utilisation de VizuArbre dans le cadre des éléments au programme de NSI.	

### Détails techniques

- Ce module nécessite de disposer du logiciel [graphviz](https://graphviz.org/download/) ainsi que du module graphviz pour python (`pip install graphviz`).

- Il a été conçu pour notebooks mais pourra aussi être utilisé dans un environnement python standard en modifiant la constante `JUPYTER_NOTEBOOK` située dans l'en-tête du fichier.

### Installation de graphviz sous Windows (méthode 1)

- On se rendra sur la page dédiée : [Downloads](https://graphviz.org/download/) de Graphviz.

	- Normalement le lien pour l'installeur de la version stable (parfois rompu lors des MAJ des dépôts) vous conduit sur cette page :
	- (https://www2.graphviz.org/Packages/stable/windows/). Il faudra ensuite suivre les liens pour parvenir à 
	- (https://www2.graphviz.org/Packages/stable/windows/10/cmake/Release/)

- Lors de l'installation du logiciel, demandez bien à actualiser le PATH Windows.

- Une fois le logiciel installé, il vous faut installer le module permettant à Python de communiquer avec le logiciel Graphviz :

	- `pip install graphviz`
	
### Installation de graphviz sous Windows (méthode 2)

- Si ce qui est indiqué sur la page [Downloads](https://graphviz.org/download/) de Graphviz conduit au dépôt Github (cela arrive parfois lorsque Graphviz effectue une MAJ sur ses serveus de dépôt) on préférera l'installeur .msi de la version 2.38 qui est toujours disponible ici :  

**[installeur MSI pour Windows](https://graphviz.gitlab.io/_pages/Download/Download_windows.html)** 


- Une fois l'installation du logiciel effectuée, on ajoutera alors graphviz au Path Windows (pour que python puisse le trouver) manuellement car la 2.38 ne le propose pas lors de l'installation :

	- Paramètres > Propriétés Système > Variables d'environnement > Variables système > Path > Modifier > Nouveau 
	
	- copier le chemin vers l'installation de graphviz (sans doute "C:\Program Files (x86)\Graphviz2.38\bin")
	
- Il suffira ensuite d'installer le module permettant à Python de communiquer avec le logiciel Graphviz :

	- `pip install graphviz`
    
### Installation de graphviz sous Debian/Ubuntu

- `sudo apt install graphviz`

- Il suffira ensuite d'installer le module permettant à Python de communiquer avec le logiciel Graphviz :

	- `pip install graphviz`