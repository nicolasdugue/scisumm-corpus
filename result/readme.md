#The result files guide
In the files titled result + Number we have multiple versions of results.

the result file contains the console output of our code when exeuted.
These files are divided into three sections.

##The first section :

in this section we have the significant words according to the contrast measure.

##The second section :

in this section we have the significant words according to the F-measure.

##The third section :

The summary of the document without using the citance.
It contains the 5 percesnt sentences of each section.

The sentences are selected using their weights on the long enough sentences, i.e the sentences which contain more than
informative words.

##The fourth section :

This section contains an analysis of matching process between the reference document and the citing ones.

for every annotation, we mention the citing sentence, the reference sentences associated to this sentence acoording
to the corpus annotation, and the same result but using our code.

Before every sentence in this section you have the **distance** of this sentence of the citing sentence using our
technique of matching.

please notice that we are talking about the dostance, not the **similarity**.

#Index of results according to numbers:

- **Result**: this file is the first version of our code result.

- **Result1**: We change the threeshold of the contrast to 1.2 instead of 1, i.e reducing the number of significant words.

    - **the number of the words has been reduced is moving from 237 to 170.**