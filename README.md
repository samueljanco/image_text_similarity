# Image-Text Similarity

## Inštalácia

### Windows

1. cx_Freeze
Najsôr je potrebné nainštalovať si nástroj cx_Freeze.
Do príkazovej riadky stačí zadať tento príkaz:
```
pip install cx_Freeze
```

2. requirements.txt
Pomocou nasledovného príkazu nainštalujte potrebné balíčky.
```
pip install -r requirements.txt
```

3. Vytvorenie distribučného balíka
Teraz môžete vytvoriť distribučný balík aplikácie.
Otvorte príkazový riadok a prejdite do adresára projektu, kde sa nachádza súbor windows_setup.py.
Zadajte nasledujúci príkaz:
```
python windows_setup.py build
```
Tento príkaz vytvorí distribučný balík aplikácie v priečinku "build".

4. Spustenie aplikácie
Po úspešnom vytvorení distribučného balíka môžete spustiť aplikáciu.
Prejdite do priečinka "build" a nájdite súbor s názvom "app".
Pre spustenie aplikácie stačí dvakrát kliknúť na tento súbor.

### MacOS

1. py2app
Najsôr je potrebné nainštalovať si nástroj py2app.
Do príkazovej riadky stačí zadať tento príkaz:
```
pip install py2app
```

2. requirements.txt
Pomocou nasledovného príkazu nainštalujte potrebné balíčky.
```
pip install -r requirements.txt
```

3. Vytvorenie distribučného balíka
Teraz môžete vytvoriť distribučný balík aplikácie.
Otvorte príkazový riadok a prejdite do adresára projektu, kde sa nachádza súbor macos_setup.py.
Zadajte nasledujúci príkaz:
```
python macos_setup.py py2app
```
Tento príkaz vytvorí distribučný balík aplikácie v priečinku "dist".

4. Spustenie aplikácie
Po úspešnom vytvorení distribučného balíka môžete spustiť aplikáciu.
Prejdite do priečinka "dist" a nájdite súbor s názvom "app".
Pre spustenie aplikácie stačí dvakrát kliknúť na tento súbor.


## Užívateľský manuál

Aplikácia má veľmi jednoduché užívateľské rozhranie a ľahko sa používa.
Po spustení sa užívateľovi zobrazí UI pozostávajúce z troch častí.
V ľavej časť okna sa nachádza textové pole, do ktorého užívateľ zadáva vstupný text.
Text je možné odsadzovať, členiť do odsekov a inak upravovať pomocou whitespacov.
Pravá strana je vyhradená pre vloženie vstupného obrázku.
Pokiaľ nie je zvolený žiaden obrázok, užívateľovi je zobrazované iba tlačidlo.
Po kliknutí na tlačidlo sa otvorí aplikácia na prezeranie súborov, pomocou ktorej užívateľ môže svoj obrázok vybrať.
Aktuálne zvolený obrázok sa zobrazuje na pravej strane okna nad tlačidlom pre výber obrázkov.
Jeho opätovným stlačením môže užívateľ zmeniť svoju voľbu vstupného obrázku.
V spondej časti okna sa nachádza tlačidlo s nápisom "Compare", ktoré spustí proces porovnávania zadaného textu a obrázku.
Po vyhodnotení podobnosti sa používateľovi zobrazí menšie okno s výsledkom uvedením v percentách.
Stlačením tlačidla OK môže užívateľ okno zavrieť a začať porovnávať novú dvojicu.

## Dataset

Model je trénovaný na datasete MS-COCO a jeho rozšírení o skóre sémantickej podobnosti Crisscrossed Captions (CxC).

MS COCO (Microsoft Common Objects in Context) obsahuje obrázky a príslušné anotácie.
Tento dataset je navrhnutý tak, aby slúžil na trénovanie a testovanie algoritmov strojového učenia na úlohy ako detekcia objektov, segmentácia obrázkov a generovanie popisov obrázkov.
MS COCO obsahuje viac ako 300 tisíc obrázkov s viac ako 2,5 miliónmi anotácií, ktoré zahrňujú popisy objektov, ich polohy a iné atribúty.
Obrázky v tomto datasete obsahujú rôzne typy scén, ako napríklad interiéry, exteriéry a mestské scenérie.

CxC dataset obsahuje takmer 250-tisíc anotácii obsahujúce pozitívne a negatívne asociácie medzi pármi dvoch obrázkov, dvoch popisov alebo obrázku a popisu.
Práve tieto anotácie umožňujú modelu dosahovať lepšie výsledky.

Pri trénovaní modelu je použitá iba "SITS" (semantic image-text similarity) časť datasetu, ktorá obsahuje približne 88 tisíc (44000 v sits_val a 44000 v sits_test) párov obrázkov a textov s mierou podobnosti v rozsahu od 0 do 5.
Model je trénovaný na približne 80 tisíc z týchto párov.
Zvyšok dát je použitý na následné testovanie. 

Linky na sťiahnutie.

Crisscrossed Captions:

https://github.com/google-research-datasets/Crisscrossed-Captions

MS-COCO: 

https://archive.org/details/MSCoco2014


## Modely 

### Generovanie obrazových rysov

#### VGG16

Ide o konvolučnú neurónovú sieť, ktorá vznikla v roku 2014 pri súťaži ILSVR(ImageNet), no stále patrí medzi často používané modely.

Model sa učí hierarchické reprezentácie dát v obrázkoch prostredníctvom viacerých konvolučných vrstiev a pooling operácii. 
Model začína niekoľkými konvolučnými vrstvami, ktoré na vstupný obraz aplikujú viacero filtrov a efektívne zisťujú rôzne funkcie obrazu, ako napríklad hrany, textúry a časti objektov.
Každý filter v konvolučnej vrstve sa aplikuje na celý obraz a výstupom je nová obrazová mriežka, ktorá zachytáva konkrétne funkcie v obraze. 
Filtre sú parametre modelu a sú vopred naučené tak, aby detekovali špecifické funkcie v obraze.
Konvolučné vrstvy nasledujú pooling vrstvy, ktoré znižujú výstup z konvolučných vrstiev, znižujú priestorové rozmery a zachovávajú najdôležitejšie funkcie.
Pooling vrstvy fungujú tak, že pre každý blok výstupu z konvolučnej vrstvy zvolia najväčšiu hodnotu alebo priemernú hodnotu a výsledkom je zmenšený výstup, ktorý zachováva najdôležitejšie funkcie z konvolučných máp.
Tento proces konvolúcie a poolingu sa v modeli opakuje niekoľkokrát, čo umožňuje učiť sa stále komplexnejšie funkcie dát obrazu na vyšších úrovniach abstrakcie. 
Posledné vrstvy modelu sú vo všeobecnosti plne prepojené vrstvy, ktoré využívajú už naučené funkcie, aby vykonali konečnú klasifikáciu obrazu. 
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

#### ResNet

ResNet (Residual Network) je architektúra hlbokých neurónových sietí, ktorá bola predstavená v roku 2015 spoločnosťou Microsoft Research.
Je navrhnutá tak, aby riešila problém miznúceho gradientu, ktorý sa vyskytuje pri trénovaní veľmi hlbokých neurónových sietí.
ResNet toho dosahuje pomocou reziduálnych spojení, ktoré umožňujú informácií prechádzať medzi vrstvami bez toho, aby boli modifikované. To pomáha zabezpečiť, že informácie o gradientoch nezmiznú, keď sa šíria sieťou, čím umožňuje trénovať veľmi hlboké neurónové siete so stovkami alebo dokonca tisícami vrstiev.
Základným stavebným blokom architektúry ResNet je reziduálny blok, ktorý pozostáva z dvoch alebo viacerých konvolučných vrstiev s priamejším spojením.
Priame spojenie obchádza konvolučné vrstvy a vstup pridáva priamo k výstupu bloku, čím sa sieť učí reziduálne funkcie namiesto pôvodného mapovania.
To uľahčuje trénovanie veľmi hlbokých sietí a zlepšuje ich presnosť.
ResNet tiež používa vrstvy normalizácie dávok a aktivačné funkcie ReLU na stabilizáciu učenia a zavedenie nelinearity. Zvyčajne sa končí globálnou vrstvou priemerového zhlukovania, nasledovanou jednou alebo viacerými plne prepojenými vrstvami a softmax vrstvou pre klasifikáciu.
Tieto posledné vrstvy sú však v tomto prípade odstránené aby bol výstupom siete vektor rysov daného obrázku.


Architektúra:

- Vstupná vrstva
- Konvolučná vrstva - Táto vrstva aplikuje konvolúciu na vstupný obraz a extrahuje z neho vlastnosti.
- Vrstva normalizácie dávok - Táto vrstva normalizuje výstup z predchádzajúcej vrstvy, aby stabilizovala proces učenia.
- Aktivačná vrstva - Táto vrstva aplikuje aktivačnú funkciu (ako napr. ReLU) na výstup z predchádzajúcej vrstvy a zavádza nelinearitu.
- Reziduálny blok - Tento blok je kľúčovou súčasťou architektúry ResNet a pozostáva z dvoch alebo viacerých konvolučných vrstiev s priamejším spojením. Priame spojenie obchádza konvolučné vrstvy a vstup pridáva priamo k výstupu bloku. To pomáha prekonať problém miznúceho gradientu a umožňuje trénovať veľmi hlboké neurónové siete.
- Vrstva globálneho priemerového zhlukovania - Táto vrstva vykonáva priemerové zhlukovanie cez vlastnosti a vracia jeden vlastnostný vektor pre každý kanál.
- (X) Plne prepojená vrstva - Táto vrstva vykonáva finálnu klasifikáciu pomocou extrahovaných vlastností z predchádzajúcich vrstiev.
- (X) Softmax vrstva - Táto vrstva prevedie výstup z finálnej plne prepojenej vrstvy na pravdepodobnostné rozdelenie pre rôzne triedy.

Počet konvolučných vrstiev a reziduálnych blokov sa môže líšiť v závislosti od konkrétnej architektúry ResNet (ResNet50, ResNet101...).


### Vnorenie slov (word embedding)

#### Universal Sentence Encoder

Model USE je postavený na architektúre Transformer a používa multi-head self-attention ako hlavný mechanizmus na získavanie informácií z danej vety.
Multi-head self-attention umožňuje modelu vyhľadávať informácie z celej vety v rovnakom čase a zohľadniť tieto informácie pri určovaní vektoru reprezentujúceho danú vetu.
USE tiež využíva techniku pred-trénovania na veľkých korpusoch textov, čo mu umožňuje získať širšie pochopenie jazyka a jeho kontextu.
Výsledkom je vektorová reprezentácia, ktorá zachováva významové vlastnosti daného textu.

#### Bert

Bert (Bidirectional Encoder Representations from Transformers) je architektúra modelu neurónovej siete pre prirodzené jazykové spracovanie (NLP), ktorú vytvorila spoločnosť Google v roku 2018.
Model je založený na architektúre transformátorov a používa bi-direkcionálne kódovanie, čo znamená, že model dokáže spracovať celú sekvenciu slov a učiť sa vzťahy medzi slovami v oboch smeroch.
To umožňuje modelu porozumieť kontextu a zlepšiť presnosť jazykových modelov.
Bert používa viacvrstvovú neurónovú sieť, ktorá obsahuje 12 alebo 24 transformátorových blokov v závislosti od veľkosti modelu.
Každý transformátorový blok pozostáva z viacerých vrstiev neurónov, ktoré sa postupne spracúvajú.
Každá vrstva obsahuje multi-head self-attention mechanizmus a viacvrstvové perceptróny (feedforward) siete.
Bert má dva hlavné trénovacie ciele: masked language modeling (MLM) a predikciu ďalšieho slova (next sentence prediction).
Pri MLM sa náhodne zakryjú niektoré slová vstupnej sekvencie a model sa učí predikovať tieto slová na základe kontextu.
Pri predikcii ďalšieho slova sa model učí rozpoznávať, či sú dve vstupné vety navzájom súvisiace alebo nie.
Bert sa používa na rôzne NLP úlohy, vrátane klasifikácie textu, poimenovania entít, parafraza textov a prekladu jazykov.
Tento model dosiahol výrazné zlepšenie výkonu pre mnohé z týchto úloh a stále sa používa v najnovších výskumných prácach a aplikáciách v oblasti NLP.


Word embeddings majú viacero výhod oproti iným technikám na reprezentáciu slov, ako napríklad one-hot encoding alebo bag-of-words modely.
Word embeddings používajú tzv. husté (dense) vektory, čo znamená, že zachytávajú viac informácií v menšom počte dimenzií.
Taktiež, môžu zachytiť sémantické vzťahy medzi slovami, čo je užitočné pre porovnávanie s obrázkami.


### Predikcia podobnosti

Modely na predikciu podobnosti zakódovaných obrázkov a textov sú neurónové siete navrhnuté pomocou knižnice TensorFlow/Keras.
Tieto modely majú dva vstupy, jeden vstup pre vektor obrazových rysov a druhý pre vektorovú reprezentáciu textu.
Pre oba vstupy nasledujú Dense vrstvy s ReLU aktiváciou.
Modely sú odlišné v spôsobe spájania výstupov z obrazových a textových vrstiev.

**a) Multiply** 
Po Dense vrstvách sú výstupy spojené pomocou operácie násobenia (element-wise multiplication) vo vrstve multipy.
Tieto výstupy sú ďalej spracované pomocou ďalšej vrstvy Dense a výstup z tejto vrstvy je následne odoslaný do poslednej vrstvy s jedným výstupom a lineárnou aktiváciou.

**b) Add**
Po Dense vrstvách sú výstupy spojené pomocou operácie sčítania (element-wise addition) vo vrstve add.
Tieto výstupy sú ďalej spracované pomocou ďalšej vrstvy Dense a výstup z tejto vrstvy je následne odoslaný do poslednej vrstvy s jedným výstupom a lineárnou aktiváciou.

**a) Concatenate**  
Po Dense vrstvách sa používajú Dense vrstvy s aktiváciou ReLu a počtom neurónov 256 pre každý z týchto vstupných kanálov.
Tieto dve vrstvy sú následne spojené do jednej vrstvy pomocou funkcie concatenate a výsledný vektor je vstupom do ďalšej Dense vrstvy s aktiváciou ReLu a počtom neurónov 128.
Výstupom z tejto vrstvy je posledná Dense vrstva s aktiváciou Linear a počtom neurónov 1, ktorá určuje výstup modelu.


Celý model je nakoniec zostrojený pomocou triedy Model z Kerasu, ktorá využíva funkcionálne API a je skompilovaný s Adam optimizérom a stratovou funkciou Mean Squared Error.

## Experimenty

Pri určovaní najlepšieho modelu pre predikciu podobnosti obrázkov a textov bolo natrénovaných 12 modelov.
Tieto modely kombinujú rôzne spôsoby extrahovania rysov z obrázkov a textov a taktiež rôzne spôsoby ich následnej kombinácie.
Pre generovanie obrazových rysov boli použité modely VGG16 a ResNet a vektorová reprezentácia textu bola vytvorená pomocou modelov Bert a Universal Sentence Encoder.
Spájanie týchto dvoch vstupov následne prebiehalo troma spôsobmi a to sčítaním, násobením alebo konkatenáciou.
Architektúry všetkých spomenutých komponentov sú popísané v predchádzajúcej časti.
Každý z modelov bol trénovaný v 50-tich epochách na viac ako 80-tisíc pároch z dátasetu Crisscrossed Captions.
Následne boli modely testované na 8000 nových pároch z rovnakého dátasetu, pričom ako stratová funkcia bola použitá 'mean_squared_error'.
Výsledky testov sú uvedené v nasledujúcej tabuľke.

| Model                   | MSE      |
| ---                     | ---      |
| ResNet-Bert-Add         | 2.0136   |
| ResNet-Bert-Concatenate | 1.9626   |
| ResNet-Bert-Multiply    | 1.9676   |
| ResNet-USE-Add          | 2.1296   |
| ResNet-USE-Concatenate  | 2.2795   |
| **ResNet-USE-Multiply**     | **1.5904**   |
| VGG16-Bert-Add          | 1.9674   |
| VGG16-Bert-Concatenate  | 2.0012   |
| VGG16-Bert-Multiply     | 1.9758   |
| VGG16-USE-Add           | 2.2469   |
| VGG16-USE-Concatenate   | 2.2195   |
| VGG16-USE-Multiply      | 1.7551   |

Najlepší výsledok dosiahol pri testovaní model **ResNet-USE-Multiply**.
Môžeme pozorovať ako značne vplýva spôsob kombinácie rysov obrázku a textu na výslednú silu modelu.
Zatiaľ čo pri kombinácií pomocou sčítania alebo konkatenácie mali modely ResNet-USE a VGG16-USE najhoršie výsledky zo všetkých testovaných modelov, pri kombinácii pomocou násobenia dosahovali tie najlepšie.
Textový model USE sa v kombinácií s oboma obrazovými modelmi osvedčil ako lepšia možnosť (pri zvolení správnej kombinácie rysov), keď v spojení s ResNetom dosiahol úplne najlepší výsledok 1.5904 a skombinovaný s VGG16 mu patrí druhé miesto výsledkom 1.7551.
Čo sa týka modelov generujúcich obrazové rysy sa celkovo ako silnejší ukázal model ResNet, keďže vo väčšine kombinácií dosiahol lepšie výsledky ako jeho konkurencia VGG16.

Následne bol ešte najlepší z modelov **ResNet-USE-Multiply** trénovaný na rôznych počtoch epoch. Tu mal najlepší výsledok model trénovnay na 50-tich epochách. 

| Počet epoch | MSE |
| --- | --- |
| 40 | 1.6039 |
| 50 | 1.5904 | 
| 70 | 1.6740 |
| 100 | 1.7163 | 


## Implementácia

### ImageEncoder

Trieda ImageEncoder používa pred-trénovaný model ResNet na extrakciu rysov z vstupných obrázkov.
Pri inicializácií trieda načíta model ResNet pred-trénovaný na datasete ImageNet , ktorý sa skladá zo všetkých vrstiev s výnimkou poslednej klasifikačnej vrstvy.
Tento nový model sa potom uloží ako atribút triedy z názvom "model".

Metóda "encode" prijíma zoznam vstupných obrázkov, načíta každý obrázok pomocou metódy load_img z Keras, zmenší ho na (224, 224) a prevedie na numpy pole.
Predspracované obrázky sa uložia do zoznamu a nasledne sa z nich pomocou modelu vygeneruju obrazové rysy.
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
Pri vytvorení inštancie triedy SimilarityScore sa načíta pred-trénovaný model podobnosti pomocou metódy keras.models.load_model zo súboru určeného premennou model_path a inicializuje triedy ImageEncoder a TextEncoder.
Trieda tiež nastavuje hodnotu MAX na 5 (maximálne skóre), ktorá sa neskôr používa na výpočet podobnosti ako percentuálnej hodnoty.
Metóda predict prijíma ako argumenty cestu k súboru s obrázkom a textový vstup, zakóduje rysy obrázku a textu pomocou tried ImageEncoder a TextEncoder a predikuje podobnosť medzi nimi pomocou načítaného similarity_modelu.
Metóda vráti hodnotu podobnosti ako hodnotu typu float v rozsahu od 0 do self.MAX.
Metóda preprocess_text je pomocná metóda, ktorá predspracuje textový vstup tým, že nahrádza znaky nového riadku medzerami.
Metóda get_percentage je pomocná metóda, ktorá berie skóre ako argument a vypočíta percentuálnu hodnotu podobnosti pomocou hodnoty MAX.
Metóda compare je hlavnou metódou triedy, ktorá berie ako argumenty cestu k súboru s obrázkom a textový vstup. Predspracuje textový vstup pomocou preprocess_text, predikuje skóre podobnosti pomocou predict a potom vypočíta percentuálnu podobnosť pomocou get_percentage.
Metóda vráti percentuálnu hodnotu podobnosti ako hodnotu typu float.

### train_model a test_model

Tieto skripty slúžia na tréning a testovanie modelu, ktorý predikuje podobnosť medzi obrazovými a textovými rysmi.

**transform_to_dictionary(arr)**

Funkcia berie ako vstup 2D numpy pole, v ktorom prvý stĺpec obsahuje kľúče a zvyšné obsahujú hodnoty.
Následne toto pole transformuje na slovník, kde sa každý riadok stane jednou jeho položkou.

**prepare_data(image_file, text_file, cxc_file)**

Funkcia na vstupe dostane cesty k súborom image_file, text_file a cxc_file.
Premenná image_file a text_file sú súbory typu numpy obsahujúce rysy obrazu a textu.
cxc_file je súbor typu CSV obsahujúci riadky identifikátorov obrazov a textu, ako aj skóre podobnosti.
Funkcia najprv načíta rysy obrázkov a textov z ich súborov, a potom ich pomocou funkcie transform_to_dictionary transformuje na slovníky.
Potom načíta CSV súbor a pridáva rysy obrázkov, rysy textov a ich cieľové skóre zodpovedajúce identifikátorom v cxc súbore do zoznamov.
Nakoniec funkcia vráti zoznamy ako polia numpy.


**[train] build_model(combine_via)**

Funkcia zostrojí a skompiluje model, ktorý sa bude trénovať.
Parameter combine_via určí spôsob spájania obrazových a textových rysov.


**[train] main(args)**

Funkcia najskôr zavolá prepare_data() na dve množiny dát (sits_val.csv a sits_test.csv).
Následne oba páry trojíc (obrázky, texty, targety) vygeneruje náhodnú permutáciu a dáta permutuje.
Z druhej trojice vynechá posledných arg.test_size príkladov, ktoré budú použité pri testovaní.
Tréningové dáta spojí pomocou funkcie np.concatenate() a natrénuje na nich model postavený pomocou funkcie build_model().
Nakoniec model uloží pod názvom arg.output.

**[test] main(args)**
Funkcia najskôr zavolá prepare_data() na dáta zo sits_test.csv.
Následne vygeneruje rovnaké permutácie ako pri trénovaní a pomocou nich poprehadzuje poradie príkladov.
Nakoniec vyberie posledných args.test_size príkladov (obrázky, texty, targety) a otestuje na nich model zadaný v args.model.


### GUI

Trieda App definuje grafické užívateľské rozhranie (GUI) pomocou knižnice PyQt5.
Rozhranie umožňuje používateľom porovnať podobnosť medzi obrázkom a textom zobrazením percentuálneho ohodnotenia podobnosti.

Trieda App dedí od triedy QWidget, ktorá je základnou triedou pre všetky prvky užívateľského rozhrania v PyQt5. 
Pri inicializácií trieda vytvorí premennú udržiavajúcu cestu k obrázku a inštanciu triedy SimilarityScore.

Trieda tiež vytvára textové pole, tlačidlo "Select Image", pole pre obrázok a tlačidlo na spustenie porovnania("Compare"). Tlačidlo "Select Image" otvára dialógové okno zobrazujúce súbory, ktoré umožňuje používateľom vybrať obrázok.
Tlačidlo "Compere" spúšťa metódu compare, ktorá získava text z textového poľa a porovnáva ho so zvoleným obrázkom pomocou objektu SimilarityScore. Ak sú zadané text aj obrázok, zobrazí sa ako vyskakovacie okno s výslednou podobnosťou.

Metóda "popUpEvent" používa triedu "QMessageBox" na vytvorenie vyskakovacieho okna, ktoré zobrazuje výsledok ako informačnú správu.

## Záver

Výsledkom projektu je desktopová aplikácia napísaná v jazyku Python, pomocou ktorej môže používateľ určiť mieru podobnosti medzi obrázkami a textom. Aplikácia na tento účel využíva model umelej inteligencie, konkrétnejšie neurónovú sieť natrénovanú na rozšírení dátasetu MS-COCO s názvom Crisscrossed Captions. Model bol vybraný s 12 testovaných variant, medzi ktorými sa ukázal ako najsilnejší.


