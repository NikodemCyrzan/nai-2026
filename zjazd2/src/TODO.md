# Lista rzeczy do zrobienia

## Komponent silnika

Komponent silnika rakietowego, który będzie przyjmował swój offset, komponent Physics oraz kierunek jako `Vector2` i 
będzie miał metodę pozwalającą sterować ciągiem. Niech ta metoda przyjmuje ciąg w Newtonach, żeby AI mogło 
policzyć ile dokładnie teraz go potrzeba. Niech te silniki też mają max ciąg, żeby nie było, że silnik magicznie generuje
nieskończony ciąg.

## Komponent czujnika

Komponent, który będzie miał metodę pozwalającą sprawdzać jak daleko czujnik znajduje się od 
terenu w kierunku `velocity`. Niech też przyjmuje offset w konstruktorze.

## Komponent AI

Komponent AI, który będzie przyjmował czujniki i za pomocą logiki rozmytej decydował jak mocno silniki powinny pracować.

## `RenderContext`

Przygotować `RenderContext` żeby dało się w nim dodawać rzeczy do wyrenderowania.

## Komponent kamery

Komponent, który będzie miał wpływ na to, jak rzeczy renderują się na ekranie, oraz będzie pozwalał śledzić `GameObject`.
Będzie trzeba przygotować prostą macierz, która będzie przenosić rzeczy z przestrzeni świata na przestrzeń 
kamery, oraz w `RenderContext` zbierać jakoś wszystko, co ma zostać wyrenderowane w danej klatce.

## Silnik graficzny

Wszystko, co zostanie dodane w `RenderContext` do wyrenderowania w danej klatce musi zostać wyrenderowane używając `PyQt6` 
lub innej może lepszej do tego zadania biblioteki.

## Komponent Input Controller

Komponent, który będzie znał stan gry (czy teraz wystrzeliwujemy auto, czy patrzymy jak leci) i będzie sterował innymi
komponentami - wyłączał fizykę, włączał ją z powrotem i dodawał impuls, wyłączał/włączał AI, przełączał tryb kamery.
