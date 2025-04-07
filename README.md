# TheEconomistExporterTool
A tool for combining The Economist pages through access for SGH students

SGH daje swoim studentom możliwość czytania The Economist po zalogowaniu, jednakże tylko po stronie/rozdziale i w praktyce wymaga to połączenia internetowego i dużo klikania.

Ten skrypt pobiera pojedyncze rozdziały i klei je w całość w jeden PDF. Dzięki temu osoby które i tak mają dostęp do tych materiałów mają do nich dostęp, ale w trochę wygodniejszy sposób.

**Wymagania:**
- python
- biblioteki selenium, webdriver_manager i PyPDF2
(na dole instrukcje jak to zrobić)

Wygodne może się okazać:
- Jakieś IDE, np. PyCharm Community Edition (darmowe i europejskie!), gdyby trzeba było/ chcielibyście coś zmieniać w kodzie.

**Co zrobić?**
1. Uruchom plik main.py
2. Podaj ścieżkę dostępu do **pustego** folderu w którym chcesz aby pojawił się ostateczny plik
3. Zaloguj się na konto SGH (wymagana weryfikacja telefonem) gdy poprosi o to strona
4. I tyle :) Uzbrój się w cierpliwość, kod na razie działa wolno, ale spędziłem nad nim całe 30 min
5. Jak coś pójdzie nie tak – włącz go ponownie

**Inne uwagi/ tipy:**
1. Powinien działać na MacOS i Windows
2. Czasami strona wykryje, że jest to automatyzacja – odpowiednio szybkie kliknięcie Captchy powinno zachować progress i działanie programu
3. Czasami duplikują się strony – nie wiem, czy to wina PyPDF2 czy tego jak stronka wrzuca artykuły, ale nie przeszkadza to w czytaniu
4. 

**Jak zainsatlować wymagane pliki?**
Python najlepiej pobrać z oficjalnej strony, https://www.python.org/ .
W konsoli (wyszukaj _terminal_ na macu lub _cmd_ na Windows) uruchomisz go przy użyciu komendy _python_ lub _python3_. 

Zanim to zrobisz, zainstaluj biblioteki w konsoli wpisując odpowiednio:
_pip install nazwa$biblioteki_
np.
_pip install selenium_

Czasami zamiast _pip_ terminal domaga się wpisania _pip3_.

Aby odpalić od razu kod, wpisz 
_python main.py_ lub odpowiednio _python3 main.py_.


**Chętnie przyjmę uwagi :)**
