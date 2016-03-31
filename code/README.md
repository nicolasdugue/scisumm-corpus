## Python Code

dans le dossier code du repo

*   /exemple_isko contient les fichiers qui représentent l'exemple utilisé dans nos articles pour expliquer la feature f-mesure (homme/femme avec tailles pieds, cheveux, nez)

*   /pyfmax contient le module python avec un "__init__.py" qui indique que c'est un module (on peut donc faire "import pyfmax") et "fmax.py" qui contient la classe qui nous servira à calculer la feature f-mesure

*   /test_isko.py utilise pyfmax/fmax.py pour charger le contenu de /exemple_isko dans une matrice

@hazemalsaied Tu peux donc compléter pyfmax/fmax.py et créer des fonctions qui calculent la feature f-mesure (en créant d'abord des fonction pour obtenir la somme des valeurs d'un cluster etc), puis utiliser test_isko.py pour tester si cela fonctionne.

Pour cela, il te faudra installer Python, numpy et scipy (prends matplotlib aussi) :
http://www.scipy.org/install.html
sudo apt-get install python-numpy python-scipy python-matplotlib


