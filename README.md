# trading-bot-observer-pattern
## Exemplarische Implementierung des Observer Patterns am Beispiel eines Trading Bots 

### Installationsanleitung

Die für die Installation und Ausführung relevanten Dateien sind im GitHub Repository https://github.com/jhehemann/trading-bot-observer-pattern zu finden. Diese Dateien müssen zunächst heruntergeladen und in einem Zielordner gespeichert werden. Zusätzlich muss zur Ausführung des Python-Scripts ein Kraken-Account angelegt und ein API-Keypair (private und public) generiert werden. Im Zielordner muss nun eine neue Datei mit dem Namen „kra-ken.key“ erstellt werden, in die das generierte Keypair eingefügt wird. Damit die API ange-sprochen werden kann und Daten geladen werden können, greift die observer_pattern.py Datei bei der Ausführung auf die Keys in der kraken.key Datei zu.

Um die observer_pattern.py Datei ausführen zu können, müssen vorab einige Programme und Bibliotheken installiert werden. Dazu empfiehlt es sich eine virtuelle Programmierumge-bung zu schaffen, um die entsprechenden Versionen innerhalb dieser Umgebung zu installie-ren. Das Projektteam hat für die Umsetzung eine solche virtuelle Umgebung mit der Umge-bungsverwaltung Conda erzeugt und alle relevanten Programme und Bibliotheken in die en-vironment.yml Datei exportiert. Aus dieser Datei kann eine virtuelle Umgebung mit exakt den in der Datei beschriebenen Programmversionen erzeugt werden. Dazu muss zunächst Con-da installiert werden (Anleitung: https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Anschließend muss über den Terminal in den entsprechenden Ord-ner mit den drei Dateien navigiert werden. Wenn nun der Befehl „conda env create -f en-vironment.yml“ ausgeführt wird, wird die neue virtuelle Umgebung mit dem Namen „tra-ding_bot“ erzeugt. Nachdem die Umgebung erzeugt wurde, muss diese lediglich noch mit dem Befehl „conda activate trading_bot“ aktiviert werden. Wenn nun über den Terminal der Befehl „python observer_pattern.py“ ausgeführt wird, startet das Programm, wobei im Termi-nal Fenster die Dokumentation der Programmschritte parallel ausgegeben wird.

### Co-Autoren
- Jannik Hehemann
- Dominik Bepple
- Marvin Blaich
- Marlene Marz
