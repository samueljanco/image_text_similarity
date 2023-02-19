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


## Implementácia