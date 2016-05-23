from os import listdir
from os.path import join
from supervised import AnnotationFile
from nltk.tokenize import RegexpTokenizer
from sets import Set

dico=Set()

if __name__ == '__main__':
    path="../data"
    trainset=[f for f in listdir(path)]
    train_files=[]
    tokenizer = RegexpTokenizer(r'\w+')
    for train in trainset:
        train_file=join(path, train, "annotation", train.split("_")[0]+".annv3.txt")
        train_files.append(train_file)
        annf= AnnotationFile(train_file)
        print join(path, train, "annotation", train.split("_")[0]+".annv3.txt")
        for ann in annf.getAnnotations():
            sentences=ann.getSentences()
            s_tokens=tokenizer.tokenize(sentences)
            for t in s_tokens:
                dico.add(t.lower())
dictionnaire=open("words", "w")
for d in dico:
    try:
        dictionnaire.write(d+"\n")
    except:
        pass
dictionnaire.close()
            