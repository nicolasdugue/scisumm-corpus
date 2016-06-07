# Citing:P99-1061.xml 1
###Ref: C90-2039.txt
##Citing Sentences: 
**45** :  Tomabechi **avoids** these problems by simulating non-destructiveness without incurring the **overhead** necessary to support backtracking . 

**46** :  First , it performs a destructive ( but reversible ) check that the two **structures** **are** compatible , and only when that succeeds does it produce an **output** **structure** . 

**47** :  Thus , no **output** **structures** **are** built until it is certain that the **unification** will ultimately succeed . 

**48** :  While an improvement over simple destructive **unification** , Tomabechi 's **approach** still suffers from what **Kogure** ( **Kogure** , 1990 ) calls **redundant** **copying** . 

**49** :  The new **feature** **structures** produced in the second phase of **unification** **include** **copies** of all the **substructures** of the **input** **graphs** , even when these **structures** **are** unchanged . 

**50** :  This can be avoided by reusing **parts** of the **input** **structures** in the **output** **structure** ( Carroll and Malouf , 1999 ) without **introducing** **significant** bookkeeping **overhead** . 

##Reference Sentences: 
**21** :  itowever , the problem with his method is that a unitication result graph consists only of newly created structures . 

**22** :  This is unnecessary because there are often input snbgraphs that can be used as part of the result graph without any modification , or as sharable parts between one of the input graphs and the result graph . 

**23** :  Copying sharable parts is called redundant copying . 




#Citing:C92-1059.xml 2
###Ref: C90-2039.xml
##Citing Sentences: 
**41** :  In this **paper** , both these type **structures** and the type **symbol** **lattice** on which **term** **structures** **are** definedare **extended** to **treat** negative **descriptions** . 

**42** :  Nega tions of type **symbols** **are** **treated** by extending type **symbol** **lattices** , and negations of **feature** existwicesand feature-address disagreements **are** **treated** by ex **tending** **term** **structures** . 

**43** :  This **extension** can be seen as intuitionistic . 

**44** :  The **extension** is **classified** into **class** ( 1 ) above.Based on this **paper** 's formalization , **unification** al gorithms have been **developed** using **graph** unificationtechniques [ 23 , 16 ] . 

**45** :  Programs **based** on these algo rithms have been implemented in **Common** Lisp . 

**46** :  < /bodyText > < sectionHeader confidence= '' 0.650502 '' genericHeader= '' **method** '' > 

##Reference Sentences: 
**0** :  Strategic Lazy Incremental Copy Graph Unification 




#Citing:C92-1059.xml 3
###Ref: C90-2039.xml
##Citing Sentences: 
**211** :  **Unification** of two **nodes** which have each other in their dnodes yields 1 because of **tag** **inconsistency** . 

**212** :  These **computations** require negligible additional **computation** . 

**213** :  To simplify the **explanation** , the destructive version of **graph** **unification** is used above . 

**214** :  Other versions **based** on more **efficient** **graph** **unification** **methods** such as **Wroblewski** 's and **Kogure** 's **method** [ 23 , 16 ) have also been **developed** . 

**215** :  Furthermore , it is easy to modify other **graph** **unification** inethods [ 21 , 61 to allow augmented 1TSs . 

**216** :  This **paper** has **proposed** an augmentation of **feature** **structures** ( **FSs** ) which **introduces** negative in formation into **FSs** in **unification-based** formalisms.Unification-based **linguistic** **formalisms** use lbs to **describe** **linguistic** **objects** and phenomena . 

##Reference Sentences: 
**0** :  Strategic Lazy Incremental Copy Graph Unification 




#Citing:C90-3046.xml 4
###Ref: C90-2039.xml
##Citing Sentences: 
**99** :  Accordingly , for example , a **compleX** , **ion** **argument** for **cases** where an inactive edge is in the chart is as follows . 

**100** :  `` membe , ' ( [ a ~ -- b 7 , i , j , a , el , Cache ) , member ( [ b , - , j , k , fl , f ] , Chart ) , **unify** ( e , [ b : f ] , g ) Is , ~ ~'°'2~ ~t~ rnember ( [ a + -- 7 , i , k , ctb , g ] , Agenda ) Isn+ , where e , f and g **are** **feature** **structures** , and .unify ( x , y , z ) **means** that z is the **result** of **unifying** x and y . **Feature** **structures** uniformly **represent** various lingtlistic **constraints** such as subcategorizations , gaps , unbounded **dependencies** , and logical **forms** . 

**101** :  A problem of this **representation** scheme is that it describes all possible **constraints** in one **structure** and deals with them at once . 

**102** :  This is inefficient with many **copy** **operations** **due** to unfications of **unnecessary** **features** that do not contribute to **successful** **unification** [ 6 ] . 

**103** :  Thus treatments such as **strategic** **unification** [ 6 ] have been **developed** . 

**104** :  It seems that a preferable **approach** is to **treat** **linguistic** **constraints** piecew'ise , taking into consider > tion abductivity of parsing , uniform integration of various **linguistic** proc~ssings , and the problem of a unificat.ion-based **approach** . 

**105** :  From this point of view , we **describe** such treatments as , especially , incorporation of word **properties** , **case** **analyses** , composition of logical **forms** , and interpretMon of noun **phrases** with adnominal particles . 

##Reference Sentences: 
**205** :  Furthermore , structure sharing increases the portion of token identical substructures of FSs which makes it efficient to keep unification results of substructures of FSs and reuse them . 

**206** :  This reduces repeated calculation of substructures . 




#Citing:P91-1031.xml 5
###Ref: C90-2039.xml
##Citing Sentences: 
**46** :  If , however , the type or template calls **are** processed on demand at run **time** , as it needs to be the **case** in FTFs with recursive types , these names can be **treated** as regular conjuncts . 

**47** :  If a conjunction is **unified** with some other **feature** **term** , every conjunct has to be **unified** . 

**48** :  Controlling the **order** in which operands **are** processed in conjunctions may save **time** if conjuncts can be processed first that **are** most likely to **fail** . 

**49** :  This **observation** is the basis for a reordering **method** **proposed** by **Kogure** [ 1990 ] . 

**50** :  If , e.g. , in syntactic **rule** **applications** , the **value** of the **attribute** **agreement** in the **representation** of nominal elements leads to clashes more often than the **value** of the **attribute** definiteneness , it would in **general** be more **efficient** to **unify** **agreement** before definiteness . 

**51** :  Every **unification** **failure** in **processing** cuts off some unsuccessful branch in the search tree . 

##Reference Sentences: 
**3** :  The other , called ti~e strategic incremental copy graph unification method , uses an early failure finding strategy which first tries to unify ; ubstructures tending to fail in unification ; this method is ; based on stochastic data on tim likelihood of failure and , 'educes unnecessary computation . 




#Citing:P91-1031.xml 6
###Ref: C90-2039.xml
##Citing Sentences: 
**59** :  However , the **failure** potential , as it is **defined** here , may **depend** on the **processing** scheme and on the **order** of subterms in the **grammar** . 

**60** :  If , e.g. , the **value** of the **agreement** **feature** **person** in the definition of the type Verb leads to **failure** more often than the **value** of the **feature** number , this may simply be **due** to the **order** in which the two subterms **are** processed . 

**61** :  Assume the unlikely situation that the **value** of number would have led to failure-if the **order** had been reversed-in all the **cases** in which the **value** of **person** did in the oM **order** . 

**62** :  Thus for any automatic counting scheme some **constant** shuffling and reshuffling of the conjunct **order** needs to be **applied** until the **order** stabilizes ( see also [ **Kogure** 1990 ] ) . 

**63** :  There is a second criterion to consider . 

**64** :  Some **unifications** with conjuncts build a lot of **structure** whereas others do not . 

##Reference Sentences: 
**186** :  in this method , theretbre , the failure tendency information is acquired by a learning process . 

**187** :  That is , the SING unification method applied in an analysis system uses the failure tendency information acquired by a learning analysis process . 

**188** :  in the learning process , when FS unification is applied , feature treatment orders are randomized for the sake of random extraction . 




#Citing:E93-1008.xml 7
###Ref: C90-2039.xml
##Citing Sentences: 
**46** :  The point here is that the parser tries to **combine** the **result** _18 of this step more than once with different other **structures** , but **unification** is a destructive **operation** ! 

**47** :  So , instead of directly **unifying** the **structures** of say _7 and _18 ( _11 and _18 , . . ) , _7 and _18 **are** inherited into the new **structure** of _20 . 

**48** :  This way virtual **copies** of the **structures** **are** produced , and these **are** unified It is essential for **efficiency** that a virtual **copy** does not **mean** that the **structure** of the type has to be **copied** . 

**49** :  The **lazy** **copying** **approach** ( [ **Kogure** , 1990 ] , and [ Emele , 1991 ] for **lazy** **copying** in **TFS** with historical backtracking ) **copies** only overlapping **parts** of the **structure** . 

**50** :  CFS **avoids** even this by **structure-** and constraint-sharing . 

**51** :  For **common** **sentences** in German , which tend to be rather long , a lot of types will be generated They supply only a **small** **part** of **structure** themselves ( just the **path** from the functor to the filler and a simple slot-filler combination **structure** ) . 

##Reference Sentences: 
**39** :  This paper proposes an FS unification method that allows structure sharing with constant m'der node access time . 

**40** :  This method achieves structure sharing by introducing lazy copying to Wroblewski 's incremental copy graph unification method . 

**78** :  Then , the unification of tl anti t2 is defined as their greatest lower bound or the meet . 




#Citing:C92-2068.xml 8
###Ref: C90-2039.xml
##Citing Sentences: 
**14** :  19901 . 

**15** :  and eliminated Over **Copying** and **Early** **Copying** ( as **defined** in [ Tomabechi , 1991 ] 2 ) and ralt about twice the speed of [ **Wroblewski** . 

**16** :  1987 ] 's **algorithm** , a In this pal ) er we proi ) ose another design principle f ( n ' **graph** **unification** bmsed upon yet another accepted **observation** that : Unmodified **subgraphs** can be **shared** . 

**17** :  At lemst two schelnes have been **proposed** recently ] ) a.~ed Ul ) OU this **observation** ( namely [ **Kogure** . 

**18** :  1990 ] and [ Emele , 1991 ] ) ; however , both schemes **are** I ) ased upon the increlllent'al Col ) yiug sehellle all ( l ~-LS ( [ e- scribed in [ Tomal ) eehi , 1991 ] **incremental** **copying** schemes inherently suffcr fi'om **Early** **Copying** as **defined** in that article . 

**19** :  This is I ) eeause , when a **unification** **falls** , the **copies** that were ( : reated up to the point of **failure** **are** w~Lste ( l if **copies** **are** **created** increment ; ally , By way of definition we would like to categorize the **sharing** of struetul'eS in gral ) hs into Feature- **Structure** **Sharing** ( FS-Sharing ) ~nd Data-Structure **Sharing** ( DS-Sharing ) . 

**20** :  Below **arc** our definitions :  Feature-Structure **Sharing** : Two or more distinct i ) ~ , ths within a **graph** **share** the same sub-graph by ( : onwwging ( 111 the same **node** equivalent to the notion of **structure** **sharing** or reenlrancy in **linguistic** theories ( such ~ in [ **Pollard** and **Sag** , 1987 ] ) . 

##Reference Sentences: 
**0** :  Strategic Lazy Incremental Copy Graph Unification 




#Citing:C92-2068.xml 9
###Ref: C90-2039.xml
##Citing Sentences: 
##Reference Sentences: 
**23** :  Copying sharable parts is called redundant copying . 

**205** :  Furthermore , structure sharing increases the portion of token identical substructures of FSs which makes it efficient to keep unification results of substructures of FSs and reuse them . 




#Citing:P91-1041.xml 10
###Ref: C90-2039.xml
##Citing Sentences: 
**13** :  Earley 's **algorithm** , 2 . 

**14** :  active chartparsing , 3 . 

**15** :  **generalized** LR parsing . 

**16** :  2In the large-scale HPSG-based **spoken** **Japanese** **analysis** **system** **developed** at ATR , sometimes 98 percent of the **elapsed** **time** is devoted to **graph** **unification** ( [ **Kogure** , 1990 ] ) . 

**17** :  ATR Interpreting Telephony Research Laboratories* Seikacho , Sorakugun , Kyoto 61902 **JAPAN** grow so quickly . 

**18** :  Thus , it **makes** sense to speed up the **unification** **operations** to improve the **total** speed performance of the **natural** **language** **systems** . 

##Reference Sentences: 
**205** :  Furthermore , structure sharing increases the portion of token identical substructures of FSs which makes it efficient to keep unification results of substructures of FSs and reuse them . 




#Citing:P91-1041.xml 11
###Ref: C90-2039.xml
##Citing Sentences: 
**227** :  Since our **algorithm** is essentially parallel , patallelization is one logical choice to pursue further speedup . 

**228** :  Parallel processes can be continuously **created** as unifyl reeurses deeper and deeper without creating any **copies** by simply looking for a possible **failure** of the **unification** ( and preparing for successive **copying** in ease **unification** succeeds ) . 

**229** :  So far , we have completed a preliminary implementation on a **shared** **memory** parallel hardware with about 75 percent of effective parallelization rate . 

**230** :  With the **simplicity** of our **algorithm** and the ease of implementing it ( compared to both **incremental** **copying** schemes and **lazy** schemes ) , **combined** with the demonstrated speed of the **algorithm** , the **algorithm** could be a viable alternative to **existing** **unification** **algorithms** used in **current** ~That is , unless some new scheme for reducing excessive **copying** is **introduced** such as scucture-sharing of an unchanged shared-forest ( [ **Kogure** , 1990 ] ) . 

**231** :  Even then , our criticism of the cost of delaying **evaluation** would still be valid . 

**232** :  Also , although different in methodology from the way suggested by **Kogure** for **Wroblewski** 's **algorithm** , it is possible to at~in structure-sharing of an unchanged forest in our scheme as well . 

##Reference Sentences: 
**11** :  For example , a spoken Present . 

**14** :  Japanese analysis system based on llPSG [ Kogure 891 uses 90 % - 98 % of the elapsed time in FS unification . 




#Citing:C94-2143.xml 12
###Ref: C90-2039.xml
##Citing Sentences: 
**53** :  Although the **overhead** for this **copying** is **significant** , it is **impossible** to **represent** a resul.-taut unitied **graph** without creating any new strut tures . 

**54** :  **Unnecessary** **copying** , though , must be **identified** and minimized . 

**55** :  **Wroblewski** ( 1987 ) delined two **kinds** of **unnecessary** copying- over-copying ( **copying** **structures** not **needed** to **represent** resultant **graphs** ) and early-copying ( **copying** **structures** even though unitication **fails** ) -but this account is flawed because the resultant **graph** is assumed to **consist** only of **newly** **created** **structures** even if **parts** of the **inputs** that **are** not changed during mtitication could be **shared** with the resultant **graph** . 

**56** :  A more eNcient **unification** **algorithm** would **avoid** this **redundant** **copying** ( **copying** **structures** that can be **shared** by the **input** and resultant **graphs** ) ( **Kogure** , 1990 ) . 

**57** :  To distinguish **structure** **sharing** at the implementation level fl'om that at the logical lew'l ( that is , coreference relations between feature-addresses ) , the lbrmer is **called** data-structure **sharing** and the latter is **called** feature-structure **sharing** ( Tomabechi , 1992 ) . 

**58** :  ' [ 'he **key** **approaches** to reducing the amount of **structures** **copied** **are** **lazy** **copying** and data-structure **sharing** . 

##Reference Sentences: 
**203** :  The LING unification method achieves structure sharing without the O ( log d ) data access overhead of Pereira 's method . 

**22** :  This is unnecessary because there are often input snbgraphs that can be used as part of the result graph without any modification , or as sharable parts between one of the input graphs and the result graph . 

**23** :  Copying sharable parts is called redundant copying . 

**24** :  A better method would nfinimize the copying of sharable varts . 




#Citing:C94-2143.xml 13
###Ref: C90-2039.xml
##Citing Sentences: 
**66** :  The link is meaningflfl during only one **unification** process and thus enables **nondestructive** **modification** . 

**67** :  4 Using an **idea** similar to Karttunen 's , Tomabechi ( 1991 ) **proposed** a quasi-destructive **unification** that uses **node** **structures** with fields for keeping update **information** that survives only during the **unification** process . 

**68** :  5 **Unification** **algorithms** allowing data-structure **sharing** ( DSS **unification** **algorithms** ) **are** **based** on two **approaches** : the Boyer and **Moore** **approach** , which was originally **developed** for **term** **unification** in theorem-proving ( Boyer & **Moore** , 1972 ) and was adopted by **Pereira** ( 1985 ) ; and the **lazy** **copying** suggested by Karttnnen ~nd **Kay** ( 1985 ) . 

**69** :  Recent **lazy** **copying** **unification** **algorithms** **are** **based** on **Wroblewski** 's or Tomabeehi 's schema : Godden ( 1990 ) **proposed** a **unification** **algorithm** that uses active data **structures** , **Kogure** ( 1990 ) **proposed** a **lazy** **incremental** **copy** **graph** ( **LING** ) **unification** that uses dependency-directed eol ) yiug , and Emeie ( 1991 ) **proposed** a lazy-incremental **copying** ( LIC ) **unification** that uses chronological **dereference** . 

**70** :  These **algorithms** **are** b0 , sed on **Wroblewski** 's **algorithm** , and Tomabechi ( 1992 ) has **proposed** a data-structure-sharing version of his quasi-destructive **unification** . 

**71** :  3.2 The **Structure** **Sharing** Problem . 

##Reference Sentences: 
**22** :  This is unnecessary because there are often input snbgraphs that can be used as part of the result graph without any modification , or as sharable parts between one of the input graphs and the result graph . 

**23** :  Copying sharable parts is called redundant copying . 

**24** :  A better method would nfinimize the copying of sharable varts . 




#Citing:P91-1042.xml 14
###Ref: C90-2039.xml
##Citing Sentences: 
**34** :  Only those **copies** **are** destructively **modified** . 

**35** :  **Finally** , the **copy** of the **newly** constructed **root** will be returned in **case** of success , and all the **copy** pointers will be invalidated in **constant** **time** by increment- **ing** a **global** **generation** counter without traversing the **arguments** again , leaving the **arguments** unchanged . 

**36** :  **Redundant** **Copying** A problem arises with **Wroblewski** 's account , because the resulting DG **consists** only of **newly** **created** **structures** even if **parts** of the **input** **DGs** that **are** not changed could be **shared** with the resultant DG . 

**37** :  A better **method** would **avoid** ( eliminate ) such **redundant** **copying** as it is **called** by [ **Kogure** 90 ] . 

**38** :  **Structure** **Sharing** The **concept** of **structure** **sharing** has been **introduced** to **minimize** the amount of **copying** by allowing **DGs** to **share** **common** **parts** of their **structure** . 

**39** :  The Boyer and **Moore** **approach** uses a skeleton/environment **representation** for **structure** **sharing** . 

##Reference Sentences: 
**23** :  Copying sharable parts is called redundant copying . 

**24** :  A better method would nfinimize the copying of sharable varts . 




#Citing:P91-1042.xml 15
###Ref: C90-2039.xml
##Citing Sentences: 
**113** :  This holds , in particular , if it **takes** much more **time** to **create** new **structures** than to update old reclaimed **structures** . 

**114** :  Comparison with other Approaches Karttunen 's Reversible **Unification** [ Karttunen 86 ] does not use **structure** **sharing** at M1 . 

**115** :  A new DG is **copied** from the **modified** **arguments** after **successful** **unification** , and the **argument** **DGs** **are** then restored to their **original** state by undoing all the changes made during **unification** hence requiring a second pass through the DG to assemble the **result** and adding a **constant** **time** for the save **operation** before each **modification** . 

**116** :  As it has been noticed by [ Godden 90 ] and [ **Kogure** 90 ] , the **key** **idea** of **avoiding** `` **redundant** **copying** '' is to do **copying** lazily . 

**117** :  **Copying** of **nodes** will be delayed until a destructive change is about to **take** place . 

**118** :  Godden uses active data **structures** ( Lisp closures ) to implement **lazy** **evaluation** of **copying** , and **Kogure** uses a **revised** **copynode** **procedure** which maintains **copy** **dependency** **information** in **order** to **avoid** immediate **copying** . 

**119** :  327 ~ . 

**120** :  **procedure** **unify** ( nodel , node2 : **CopyNode** ) nodel * -- deref ( nodel ) node2 ~-deter ( node2 ) IF node1 = node2 THEN **return** ( nodel ) ELSE newtype ~-nodel.type A node2.type IF newtype = I THEN **return** ( l ) ELSE < SharedArcsl , SharedArcs2 > ~-SharedArcs ( nodel , node2 ) < UniqueArcsl , UniqueArcs2 > ~-UniqueArcs ( nodel , node2 ) IF ActiveP ( nodel ) THEN **node** ~-nodel node.arcs ~-node.arcs U UniqueArcs2 node2.copy ~-node ELSE IF ActiveP ( node2 ) THEN **node** ~-node2 node.arcs ~-node.arcs LJ UniqueArcsl nodel , **copy** *- **node** ELSE **node** ~-CreateCopyNode nodel.copy *- **node** node2.copy ~-node node.arcs ~-UniqueArcsl U SharedArcsl U UniqueArcs2 **ENDIF** **ENDIF** node.type ~-newtype FOR EACH < SharedArcl , SharedArc2 > IN < SharedArcsl , SharedArcs2 > DO **unify** ( SharedArcl.dest , SharedArc2.dest ) **return** ( **node** ) **ENDIF** **ENDIF** END **unify** **Figure** 4 : The **unification** **procedure** **approach** naive **Pereira** 85 Karttunen/Kay 85 Karttunen 86 **Wroblewski** 87 Godden 90 **Kogure** 90 LIC **methods** **early** over **redundant** incr . 

**121** :  **lazy** **copying** **copying** **copying** **copying** **copying** yes yes yes no no no no no no no no no yes no yes no no yes no no no yes yes yes no no no yes no yes no yes yes no yes no yes no yes yes **Figure** 5 : Comparison of **unification** **approaches** **structure** **sharing** no yes yes no no yes yes yes Both of these **approaches** suffer from difficulties of their own . 

**122** :  In Godden 's **case** , **part** of the **copying** is substituted/traded for by the creation of active data **structures** ( Lisp closures ) , a potentially very costly **operation** , even where it would turn out that those closures remain unchanged in the final **result** ; hence their creation is **unnecessary** . 

**123** :  In addition , the search for already **existing** instances of active data **structures** in the **copy** **environment** and **merging** of **environments** for successive **unifications** causes an additional **overhead** . 

**124** :  Similarly , in **Kogure** 's **approach** , not all **redundant** **copying** is avoided in **cases** where there **exists** a **feature** **path** ( a **sequence** of **nodes** connected by **arcs** ) to a **node** that needs to be **copied** . 

**125** :  All the **nodes** along such a **path** must be **copied** , even if they **are** not affected by the **unification** **procedure** . 

**126** :  Furthermore , **special** **copy** **dependency** **information** has to be maintained while **copying** **nodes** in **order** to trigger **copying** of such **arc** **sequences** leading to a **node** where **copying** is **needed** later in the process of **unification** . 

##Reference Sentences: 
**23** :  Copying sharable parts is called redundant copying . 

**141** :  5 disables structure sharing , ttowever , this whole copying is not necessary if a lazy evaluation method is used . 

**142** :  With such a method , it is possible to delay copying a node until either its own contents need to change ( e.g. , node G3/Ka c ! 7 > ) or until it is found to have an arc ( sequence ) to a node t , hat needs to be copied ( e.g. , node X G3/ < a c > in Fig . 
