## Python Code

Pour faire tourner le code, il faut installer Python, numpy et scipy :
http://www.scipy.org/install.html

    sudo apt-get install python-numpy python-scipy
    
mais également nltk (présuppose d'avoir installé pip) :

    sudo pip install -U nltk


*   /exemple_isko contient les fichiers qui représentent l'exemple utilisé dans nos articles pour expliquer la feature f-mesure (homme/femme avec tailles pieds, cheveux, nez)

*   /pyfmax est un package qui contient le module "fmax.py" qui introduit la classe qui nous servira à calculer la feature f-mesure

*   /test_isko.py utilise pyfmax/fmax.py pour charger le contenu de /exemple_isko dans une matrice

*   /pycorpus est un package qui contient le module loader qui permet de charger des fichiers du corpus

*   /test_load_file utilise pycorpus pour charger un fichier


@hazemalsaied Tu peux donc compléter pyfmax/fmax.py et créer des fonctions qui calculent la feature f-mesure (en créant d'abord des fonction pour obtenir la somme des valeurs d'un cluster etc), puis utiliser test_isko.py pour tester si cela fonctionne.




