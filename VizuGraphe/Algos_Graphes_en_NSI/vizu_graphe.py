import graphviz as gv
from copy import copy, deepcopy

JUPYTER_NOTEBOOK = True

class VizuGraphe:
    
    def __init__(self, type_structure, structure_adjacence,
                                            oriente = False,
                                            moteur = 'neato',
                                            etiquettes_secondaires = None, 
                                            couleurs = None,
                                            etiquettes_principales = None,
                                            formes = None):
        '''
        - type_structure : représentation utilisée pour le graphe:
        
                 - 'liste'       : liste d'adjacence sous forme d'un dictionnaire dont les valeurs 
                                       sont les listes des sommets adjacents
                                              
                 - 'liste_pond'   : liste d'adjacence pondérée sous forme d'un dictionnaire dont les
                                       valeurs sont des dictionnaires ayant pour clefs les sommets 
                                       adjacents et pour valeurs les poids des arêtes
                                     
                 - 'matrice_bool' : matrice d'adjacence dont les éléments sont des bool False ou True
                 
                 - 'matrice_bin'  : matrice d'adjacence dont les éléments sont des int 0 ou 1
                 
                 - 'matrice_pond' : matrice d'adjacence pondérée dont les éléments sont des int (ou des float)
                 
        - structure_adjacence : la matrice ou le dictionnaire servant de liste d'adjacence
        
        - oriente [ = False] : booléen indiquant si le graphe est orienté ou pas ?
        
        - moteur [ = 'neato']             : moteur de placement des sommets utilisé par graphviz. 
                                    Autres choix :'circo', 'dot', 'fdp', 'neato', 'osage', 
                                    'patchwork', 'sfdp','twopi'
                                     https://graphviz.org/documentation/ 
        
        - etiquettes_secondaires [ = None] : dictionnaire ayant pour clefs des étiquettes
                                                       du graphe et pour valeurs les étiquette secondaires
                                                       à afficher.
                                                  
        - couleurs [ = None] : dictionnaire ayant pour clefs des étiquettes du graphe et pour 
                                        valeurs les couleurs des sommets au format (H, S, V) avec H, S, V
                                        de type float entre 0 et 1.
                                                       
        - formes [ = None] : dictionnaire ayant pour clefs des étiquettes du graphe et pour valeurs les formes
                                 des sommets ('rect', 'rectangle', 'folder', 'house', 'ellipse', 'egg', 
                                 'triangle', 'diamond' [...] 
                                 https://graphviz.org/doc/info/shapes.html
                                 
        - etiquettes_principales [ = None] : pour les *matrices d'adjacence* de taille NxN, dictionnaire ayant 
                                                       pour clefs les indices des sommets (entre 0 et N-1)
                                                       et pour valeurs les étiquettes principales à afficher
                                                       si on souhaite ne pas utiliser les indices des sommets
        '''          
        
        self.type_structure = type_structure
        self.structure = structure_adjacence
        self.etiquettes_secondaires = deepcopy(etiquettes_secondaires)
        self.couleurs = copy(couleurs)
        self.etiquettes_principales = deepcopy(etiquettes_principales)
        self.formes = copy(formes)
        self.oriente = oriente
        self.moteur = moteur
        self._initialiser_parametres_dessin() 
        
        self._creer_objet_graphviz()           
            
            
    def _initialiser_parametres_dessin(self):
        
        self.size = '10'                              #taille maximale de l'image générée
        self.label = 'Graphe'                         #titre du graphique
        
        self.node_style = 'filled'                    #remplissage des noeuds
        self.node_shape = 'circle'                    #forme des noeuds
        self.node_fontsize = '12'                     #taille de la police des noeuds
        self.node_small_fontsize = '11'               #taille de la police secondaire des noeuds
        self.node_color = (0.5, 0.2, 1.0)             #couleur par défaut au format HSV
        self.node_width = '0.35'                      #largeur des noeuds
        self.node_height = '0.35'                     #hauteur des noeuds
        
        self.edge_style = 'solid'                     #flèches en traits pleins
        self.edge_arrowhead = 'open' if self.oriente == True else 'none'  #forme des têtes de flèches
        self.edge_arrowsize = '0.5'                   #taille des têtes de flèches        
        self.edge_fontsize = '12'                     #taille de la police pour les arêtes
        
    def _creer_objet_graphviz(self):
        graph_maker = gv.Digraph if self.oriente else gv.Graph
        self.G = graph_maker('graphe', strict = 'True', engine = self.moteur)
        self._injecter_parametres_dessin_dans_graphviz()
        self._dessiner_graphe()
        if JUPYTER_NOTEBOOK : 
            display(self.G)
        else :
            self.G.render(view=True)                 
        
    def _injecter_parametres_dessin_dans_graphviz(self): 
        self.G.attr(root = '',
                    size = self.size,
                    label = self.label)
        
        self.G.node_attr.update(style = self.node_style,
                                fontsize = self.node_fontsize,
                                width = self.node_width,
                                height = self.node_height,
                                fixedsize = 'False',
                                margin = '0, 0')
        
        self.G.edge_attr.update(style = self.edge_style,
                                arrowhead = self.edge_arrowhead,
                                arrowsize = self.edge_arrowsize,
                                fontsize = self.edge_fontsize)               
                    
    def _tuple_to_string(couleur):
        return ' '.join([str(round(c, 4)) for c in couleur])
    
    def _donner_couleur(self, sommet_ou_numero):
        if self.couleurs == None or sommet_ou_numero not in self.couleurs:
            return VizuGraphe._tuple_to_string(self.node_color)
        else:
            return VizuGraphe._tuple_to_string(self.couleurs[sommet_ou_numero])
        
    def _donner_label(self, sommet, numero):
        clef_pour_etiquette_secondaire = sommet if self.type_structure in ('liste', 'liste_pond') else numero
        if self.etiquettes_secondaires == None or clef_pour_etiquette_secondaire not in self.etiquettes_secondaires:
            S = '<<B>' + str(sommet) + '</B>>'
            return S
        else:
            e_princ = str(sommet)
            e_secon = str(self.etiquettes_secondaires[clef_pour_etiquette_secondaire])
            small = str(self.node_small_fontsize)
            S = '<<B>' + e_princ + '</B><I><FONT POINT-SIZE="' + small + '"><BR/>' + e_secon + '</FONT></I>>'
            return S
        
    def _donner_forme(self, sommet_ou_numero):
        if self.formes == None or sommet_ou_numero not in self.formes:
            return self.node_shape
        else:
            return self.formes[sommet_ou_numero]       
        
    def _dessiner_graphe(self): 
        dico = { 'liste'         : self._dessiner_liste,
                 'liste_pond'    : self._dessiner_liste_pond,
                 'matrice_bool'  : self._dessiner_matrice_bool,
                 'matrice_bin'   : self._dessiner_matrice_bin,
                 'matrice_pond'  : self._dessiner_matrice_pond}
        
        dico[self.type_structure]()

    
    def _dessiner_liste(self):           
        sommets = list(self.structure.keys())
        som_num = self._creer_noeuds_graphviz_liste(sommets)
        for sommet, successeurs in self.structure.items():
            for succ in successeurs :
                self.G.edge(som_num[sommet], som_num[succ])

    def _dessiner_liste_pond(self): 
        sommets = list(self.structure.keys())
        som_num = self._creer_noeuds_graphviz_liste(sommets)
        for sommet, successeurs in self.structure.items():
            for succ in successeurs :
                p = str(self.structure[sommet][succ])
                if p != '0':
                    self.G.edge(som_num[sommet], som_num[succ], label = p)  
    
    def _dessiner_matrice_bool(self): 
        sommets  = self._recuperer_liste_sommets_matrice()
        self._creer_noeuds_graphviz_matrice(sommets)
        for lig in range(len(self.structure)):
            for col in range(len(self.structure[0])):
                if self.structure[lig][col]: 
                    self.G.edge(str(lig), str(col))
                    
    def _dessiner_matrice_bin(self): 
        sommets  = self._recuperer_liste_sommets_matrice()
        self._creer_noeuds_graphviz_matrice(sommets)
        for lig in range(len(self.structure)):
            for col in range(len(self.structure[0])):
                if self.structure[lig][col] == 1: 
                    self.G.edge(str(lig), str(col))
                            
    def _dessiner_matrice_pond(self):
        sommets  = self._recuperer_liste_sommets_matrice()
        self._creer_noeuds_graphviz_matrice(sommets)
        for lig in range(len(self.structure)):
            for col in range(len(self.structure[0])):
                if self.structure[lig][col] != 0: 
                    p = str(self.structure[lig][col]) + ' '
                    self.G.edge(str(lig), str(col), label = p)  
                    
    def _recuperer_liste_sommets_matrice(self):
        if self.etiquettes_principales== None:
            sommets = list(range(len(self.structure))) 
        elif type(self.etiquettes_principales) == list:
            sommets = self.etiquettes_principales
        elif type(self.etiquettes_principales) == dict:    
            sommets = [self.etiquettes_principales[i] for i in range(len(self.etiquettes_principales))]
        return sommets
    
    def _creer_noeuds_graphviz_matrice(self, liste_sommets):
        som_num = dict()
        numero = 0
        for sommet in liste_sommets:
            som_num[sommet] = str(numero)
            self.G.node( som_num[sommet], label = self._donner_label(sommet, numero), 
                                          color = self._donner_couleur(numero),
                                          shape = self._donner_forme(numero))
            numero = numero + 1
           
    def _creer_noeuds_graphviz_liste(self, liste_sommets):
        som_num = dict()
        numero = 0
        for sommet in liste_sommets:
            som_num[sommet] = str(numero)
            self.G.node( som_num[sommet], label = self._donner_label(sommet, numero), 
                                          color = self._donner_couleur(sommet),
                                          shape = self._donner_forme(sommet))
            numero = numero + 1
        return som_num

    def modifier(self, **kwargs):
        '''
        Une fois un graphique créé et représenté, permet de modifier les paramètres de dessin. 
        
        - REINITIALISATION  :
        
            - reset  [ = False]               : booléen indiquant si on réinitialise les modifications
                                                   de paramètres déjà prises en compte auparavant 
                                                   (sauf 'moteur' et 'oriente')  
        
        - PARAMETRES DU GRAPHE EN ENTIER :
        
            - size [ = 10]                    : taille maximale de l'image générée
            
            - label [ = 'Graphe']             : titre du graphique
            
            - oriente [ = False]              : est-ce que le graphe est orienté ou pas
            
            - moteur [ = 'neato']             : moteur de placement des sommets utilisé par graphviz. 
                                                Autres choix :'circo', 'dot', 'fdp', 'neato', 'osage', 
                                                'patchwork', 'sfdp','twopi'
                                                 https://graphviz.org/documentation/ 
                                                 
        - PARAMETRES INDIVIDUELS :
        
            - etiquettes_secondaires [ = None] : dictionnaire ayant pour clefs des étiquettes
                                                   du graphe et pour valeurs les étiquette secondaires
                                                   à afficher.

            - couleurs [ = None] : dictionnaire ayant pour clefs des étiquettes du graphe et pour 
                                     valeurs les couleurs des sommets au format (H, S, V) avec H, S, V
                                     de type float entre 0 et 1.

            - formes [ = None] : dictionnaire ayant pour clefs des étiquettes du graphe et 
                                    pour valeurs les formes des sommets ('rect', 'rectangle', 
                                    'folder', 'house', 'ellipse', 'egg', 'triangle', 'diamond' [...] 
                                    https://graphviz.org/doc/info/shapes.html

            - etiquettes_principales [ = None] : pour les *matrices d'adjacence* de taille NxN, 
                                                    dictionnaire ayant pour clefs les indices des 
                                                    sommets (entre 0 et N-1) et pour valeurs les 
                                                    étiquettes principales à afficher si on souhaite 
                                                    ne pas utiliser les indices des sommets
                                                    
                                                 
            
        - PARAMETRES DES NOEUDS PAR DEFAUT :
        
            - node_shape [ = 'circle']        : forme des noeuds dessinés. Autres formes disponibles
                                                   rect, ellipse, folder, star [...]. 
                                                   https://graphviz.org/doc/info/shapes.html
                                                  
            - node_width [ = 0.35]          : largeur des noeuds
            
            - node_height [ = 0.35]         : hauteur des noeuds
            
            - node_color [ = (0.5, 0.2, 1)]   : couleur des noeuds au format HSV 
            
            - node_fontsize [ = 12]         : taille de police de l'étiquette principale des noeuds
            
            - node_small_fontsize [ = 11]   : taille de police de l'étiquette secondaire des noeuds
            
            - node_style [ = 'filled']        : style de remplissage. Au choix parmi 'solid', 'dashed', 
                                                   'dotted', 'bold', 'rounded', 'filled' [...]
                                                   https://graphviz.org/doc/info/attrs.html#k:style
        
        - PARAMETRES DES ARCS PAR DEFAUT :
        
            - edge_fontsize [ = 12]         : taille de la police dans le cas d'un graphe pondéré
        
            - edge_style [ = 'solid']         : style du tracé, au choix parmi 'solid', 'dashed', 
                                                   'dotted', 'bold'
            
            - edge_arrowhead [= 'empty']      : forme de la tête de la flèche. Au choix parmi 'normal', 
                                                   'none', 'invempty', 'open' [...]
                                                   https://graphviz.org/doc/info/attrs.html#k:arrowType
                                                  
            - edge_arrowsize [= 0.5]        : taille de la tête de la flèche
        '''
        
        legal_args = ("size", "label", "node_style", "node_shape", "node_fontsize", 
                      "node_small_fontsize","node_color", "node_width", "node_height", 
                      "edge_style", "edge_arrowhead", "edge_arrowsize", "edge_fontsize",
                      "moteur", "oriente", "reset", "etiquettes_secondaires", "couleurs", 
                      "formes", "etiquettes_principales")
        
        if "reset" in kwargs.keys():
            if kwargs["reset"] == True:
                self._initialiser_parametres_dessin()
                self.etiquettes_secondaires = None
                self.etiquettes_principales = None
                self.couleurs = None
                self.formes = None
        for key, val in kwargs.items():
            if key in legal_args:
                if type(val) == int or type(val) == float:
                    setattr(self, key, str(val))
                elif type(val) == dict or type(val) == list:
                    setattr(self, key, deepcopy(val))
                else:
                    setattr(self, key, val)
        self._creer_objet_graphviz()  
           
        
    def enregistrer(self, nom_fichier = 'mon_graphe', format_image = 'png'):        
        '''
         Permet d'enregistrer le graphe au format texte 'graphviz' et au format image choisi.
         Il y a donc deux fichiers qui sont générés.
         
          - nom_fichier [ = 'mon_graphe'] : nom des deux fichiers sauvegardés dont l'un sera
                                                   suffixé avec l'extension correspondant au format image choisi
                                                  
          
          - format_image [ = 'png']              : format de fichier de l'image générée. Au choix parmi : 
                                                   'ps', 'eps', 'svg', 'jpg', 'tiff' [...]
                                                   https://graphviz.org/doc/info/output.html
        '''                                              
        self.G.render(filename = nom_fichier, format = format_image)