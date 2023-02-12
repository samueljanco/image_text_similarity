# image_text_similarity

## Inštalácia

## Uživateľský manuál

## Model 

### Generovanie obrazových rysov

Obrazové rysy sa zo vstupných trénovacich obrázkov generujú pomocou modelu VGG16. Ide o konvolučnú neurónovú sieť, ktorá vznikla v roku 2014 pri súťaži ILSVR(ImageNet), no stále patrí medzi často používané modely.

Model sa učí hierarchické reprezentácie dat v obrázkoch prostredníctvom viecerých konvolučných vrstiev a pooling operácii. 
Model začína niekoľkými konvolučnými vrstvami, ktoré na vstupný obraz aplikujú viacero filtrov, efektívne zisťujú rôzne funkcie obrazu, ako napríklad hrany, textúry a časti objektov.
Každý filter v konvolučnej vrstve sa aplikuje na celý obraz a výstupom je nová obrazová mriežka, ktorá zachytáva konkrétne funkcie v obraze. 
Filtre sú parametre modelu a sú vopred naučené tak, aby detekovali špecifické funkcie v obraze.
Konvolučné vrstvy nasledujú pooling vrstvy, ktoré znižujú výstup z konvolučných vrstiev, znižujú priestorové rozmery a zachovávajú najdôležitejšie funkcie.
Pooling vrstvy fungujú tak, že pre každý blok výstupu z konvolučnej vrstvy zvolia najväčšiu hodnotu alebo priemernú hodnotu a výsledkom je zmenšený výstup, ktorý zachováva najdôležitejšie funkcie z konvolučných map.
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





## Implementácia