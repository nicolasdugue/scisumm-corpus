'''
Created on Apr 1, 2016

@author: dugue
'''

import matplotlib.pyplot as plt

def plotDistrib(distrib):
    plt.hist(distrib)
    plt.show()
    
def write(distrib, path):
    fw=open(path, "w")
    for d in distrib:
        fw.write(d.encode("UTF-8")+ "\t"+str(distrib[d])+"\n")
    fw.close()
    
    