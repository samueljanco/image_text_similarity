# image_text_similarity

## Inštalácia

## Uživateľský manuál

Aplikácia má veľmi jednoduché uživateľské rozhranie a ľahko sa používa.
Po spustení sa užívateľovi zobrazí UI pozostávajúce z troch častí.
V ľavej časť okna sa nachádza textové poľe, do ktorého uživateľ zadáva vstupný text.
Text je možné odsadzovať, členiť do odsekov a inak upravovať pomocou whitespacov.
Pravá strana je vyhradená pre vloženie vstupného obrázku.
Pokiaľ nie je zvolený žiaden obrázok, uživateľovi je zobrazované tlačidlo s ikonkou.
Po kliknutí na tlačidlo sa otvorí aplikácia na prezeranie súborov, pomocou ktorej užívateľ môže svoj obrázok vybrať.
Aktuálne zvolený obrázok sa zobrazuje na pravej strane okna namiesto tlačidla pre výber obrázkov.
To je teraz posunuté pod obrázok a jeho stlačením môže užívateľ zmeniť svoju voľbu vstupného obrázku.
V spondej časti okna sa nachádza tlačidlo s nápisom "Compare", ktoré spustí proces porovnávania zadaného textu a obrázku.
Po vyhodnotení podobnosti sa používateľovi zobrazí menšie okno s výsledkom uvedením v percentách.
V pravom hornom rohu menšieho okna bude ikonka "X" pomocou, ktorej je možné okno zavrieť a začať porovnávať novú dvojicu.

## Dataset

Model je trénovaný na datasete MS-COCO a jeho rozšírení o skóre sémantickej podobnosti Crisscrossed Captions (CxC).

MS COCO (Microsoft Common Objects in Context) bsahuje obrázky a príslušné anotácie.
Tento dataset je navrhnutý tak, aby slúžil na trénovanie a testovanie algoritmov strojového učenia na úlohy ako detekcia objektov, segmentácia obrázkov a generovanie popisov obrázkov.
MS COCO obsahuje viac ako 300 tisíc obrázkov s viac ako 2,5 miliónmi anotácií, ktoré zahrňujú popisy objektov, ich polohy a iné atribúty.
Obrázky v tomto datasete obsahujú rôzne typy scén, ako napríklad interiéry, exteriéry a mestské scenérie.
Dataset je veľký a rozmanitý, čo z neho robí užitočný nástroj pre výskum a vývoj.

CxC dataset obsahuje takmer 250-tisíc anotácii obsahujúce pozitívne a negatívne associácie medzi pármi dvoch obrázkov, dvoch popisov alebo obrázku a poipisu.
Práve tieto anotácie umožnujú modelu dosahovať lepšie výsledky.

Pri trénovaní modelu je použitá iba "SITS" (semantic image-text similarity) časť dátasetu, ktorá obsahuje približne 88 tisíc (44000 v sits_val a 44000 v sits_test) párov obrázkov a textov s mierou podobnosti v rozsahu od 0 do 5.
Model je trénovaný na približne 80 tisíc z týchto párov.
Zvyšok dát je použitý na následnú evaluáciu. 


## Model 

### Generovanie obrazových rysov

Obrazové rysy sa zo vstupných trénovacich obrázkov generujú pomocou modelu VGG16. Ide o konvolučnú neurónovú sieť, ktorá vznikla v roku 2014 pri súťaži ILSVR(ImageNet), no stále patrí medzi často používané modely.

Model sa učí hierarchické reprezentácie dát v obrázkoch prostredníctvom viecerých konvolučných vrstiev a pooling operácii. 
Model začína niekoľkými konvolučnými vrstvami, ktoré na vstupný obraz aplikujú viacero filtrov a efektívne zisťujú rôzne funkcie obrazu, ako napríklad hrany, textúry a časti objektov.
Každý filter v konvolučnej vrstve sa aplikuje na celý obraz a výstupom je nová obrazová mriežka, ktorá zachytáva konkrétne funkcie v obraze. 
Filtre sú parametre modelu a sú vopred naučené tak, aby detekovali špecifické funkcie v obraze.
Konvolučné vrstvy nasledujú pooling vrstvy, ktoré znižujú výstup z konvolučných vrstiev, znižujú priestorové rozmery a zachovávajú najdôležitejšie funkcie.
Pooling vrstvy fungujú tak, že pre každý blok výstupu z konvolučnej vrstvy zvolia najväčšiu hodnotu alebo priemernú hodnotu a výsledkom je zmenšený výstup, ktorý zachováva najdôležitejšie funkcie z konvolučných máp.
Tento proces konvolúcie a poolingu sa v modeli opakuje niekoľkokrát, čo umožňuje učiť sa stále komplexnejšie funkcie dát obrazu na vyšších úrovniach abstrakcie. 
Posledné vrstvy modelu sú vo všeobecnosti plne prepojené vrstvy, ktoré využívaju už naučené funkcie, aby vykonali konečnú klasifikáciu obrazu. 
Tie sú však z modelu odstránené aby výstupom siete bol vektor rysov so 4096 dimenziami.

Architektúra:

- Vstupná vrstva
- Konvolučná vrstva 1 (64 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 2 (64 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- MaxPooling vrstva (2x2 pooling)
- Konvolučná vrstva 3 (128 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 4 (128 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- MaxPooling vrstva (2x2 pooling)
- Konvolučná vrstva 5 (256 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 6 (256 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 7 (256 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- MaxPooling vrstva (2x2 pooling)
- Konvolučná vrstva 8 (512 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 9 (512 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 10 (512 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- MaxPooling vrstva (2x2 pooling)
- Konvolučná vrstva 11 (512 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 12 (512 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- Konvolučná vrstva 13 (512 filtre, 3x3 jadro, ReLU aktivácia, padding=1)
- MaxPooling vrstva (2x2 pooling)


### Vnorenie slov (word embedding)

Vektory sú generované pomocou Universal Sentence Encoder.
Model USE je postavený na architektúre Transformer a používa multi-head self-attention ako hlavný mechanismus na získavanie informácií z danej vety.
Multi-head self-attention umožňuje modelu vyhľadávať informácie z celej vety v rovnakom čase a zohľadniť tieto informácie pri určovaní vektora reprezentujúceho danú vetu.
USE tiež využíva techniku pre-trainingu na veľkých korpusoch textov, čo mu umožňuje získať širšie pochopenie jazyka a jeho kontextu.
Výsledkom je vektorová reprezentácia, ktorá zachováva významové vlastnosti daného textu.
Následne je tréning modelu ešte doladený na menšom korpuse zostavenom s popiov obrázkov v datasete MS-COCO. 

Word embeddings majú viacero výhod oproti iným technikám na reprezentáciu slov, ako napríklad one-hot encoding alebo bag-of-words modely.
Word embeddings používajú tzv. husté (dense) vektory, čo znamená, že zachytávajú viac informácií v menšom počte dimenzií.
Taktiež, môžu zachytiť sémantické vzťahy medzi slovami, čo je užitočné pre porovnávanie s obrázkami.

### Predikovanie podobnosti

## Implementácia

### ImageEncoder

Trieda ImageEncoder používa predtrénovaný model VGG16 na extrakciu rysov z vstupných obrázkov.
Pri inicializácií trieda načíta model VGG16 predtrénovaný na datasete ImageNet a vytvorí nový model typu Sequential, ktorý sa skladá zo všetkých vrstiev s výnimkou poslednej klasifikačnej vrstvy.
Tento nový model sa potom uloží ako atribút triedy z názvom "model".

Metóda "encode" prijíma zoznam vstupných obrázkov, načíta každý obrázok pomocou metódy load_img z Keras, zmenší ho na (224, 224) a prevedie na numpy pole.
Numpy pole sa potom predspracuje pomocou funkcie preprocess_input modelu VGG16 a predá sa do predtrénovaného modelu VGG16 na extrakciu rysov.
Extrahované rysy sa potom preformátujú a uložia sa do zoznamu.
Nakoniec, metóda vráti numpy pole všetkých extrahovaných rysov zo vstupných obrázkov.
Trieda je užitočná pre ďalšie triedy, ktoré potrebujú zakódovať obrazové vstupy do vektorového priestoru pre ďalšie spracovanie, ako napríklad trieda SimilarityScore.


### TextEncoder

Trieda TextEncoder sa používa na zakódovanie textových rysov pomocou pretrénovanej neurónovej siete.
Pri vytvorení inštancie triedy TextEncoder sa pomocou metódy hub.load načíta model Universal Sentence Encoder vo verzii 4 od spoločnosti Google.
Metóda encode prijíma ako argument zoznam textových vstupov, ktoré pomocou modelu zakóduje a vráti ich ako numpy pole.
Trieda je užitočná pre ďalšie triedy, ktoré potrebujú zakódovať textové vstupy do vektorového priestoru pre ďalšie spracovanie, ako napríklad trieda SimilarityScore.

### SimilarityScore

Trieda SimilarityScore vykonáva predikciu podobnosti medzi vstupným obrázkom a textom.
Využíva natrénovaný model a  triedy ImageEncoder a TextEncoder na kódovanie obrazových a textových rysov.
Pri vytvorení inštancie triedy SimilarityScore sa načíta predtrénovaný model podobnosti pomocou metódy keras.models.load_model zo súboru určeneného premennou model_path a inicializuje tridy ImageEncoder a TextEncoder.
Trieda tiež nastavuje hodnotu MAX na 5 (maximálne skóre), ktorá sa neskôr používa na výpočet podobnosti ako percentuálnej hodnoty.
Metóda predict prijíma ako argumenty cestu k súboru s obrázkom a textový vstup, zakóduje rysy obrázku a textu pomocou tried ImageEncoder a TextEncoder a predikuje podobnosť medzi nimi pomocou načítaného similarity_modelu.
Metóda vráti hodnotu podobnosti ako hodnotu typu float v rozsahu od 0 do self.MAX.
Metóda preprocess_text je pomocná metóda, ktorá predspracuje textový vstup tým, že nahrádza znaky nového riadku medzerami.
Metóda get_percentage je pomocná metóda, ktorá berie skóre ako argument a vypočíta percentuálnu hodnotu podobnosti pomocou hodnoty MAX.
Metóda compare je hlavnou metódou triedy, ktorá berie ako argumenty cestu k súboru s obrázkom a textový vstup. Predspracuje textový vstup pomocou preprocess_text, predikuje skóre podobnosti pomocou predict a potom vypočíta percentuálnu podobnosť pomocou get_percentage.
Metóda vráti percentuálnu hodnotu podobnosti ako hodnotu typu float.


