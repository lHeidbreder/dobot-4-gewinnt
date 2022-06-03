Eine Implementation des Spiels "4 gewinnt" auf Python Basis mit Verbindung zum Dobot Magician.

## Voraussetzungen:

Das Programm benötigt eine zusätzliche Bibliothek, PySimpleGUI. Diese kann wenn nötig via pip installiert werden:

* linux: `pip install pysimplegui`
* windows: `py -m pip install pysimplegui`

Darüber hinaus müssen die logischen Ports ermittelt werden, unter denen die Dobots angeschlossen sind. Unter Windows geschieht dieses über den Aufruf des `show-dobot-ports.ps1` PowerShell Skripts.<br>
Sofern diese nicht "COM6" und "COM8" sind, müssen die Zeilen 18 und 19 der `src/Game.py` angepasst werden.

Zu guter Letzt muss sichergestellt werden, dass die Dobots die korrekte Distanz voneinander entfernt sind.

## Verwendung:
Um das Programm zu verwenden, wird die Datei `main.py` mit 2 Kommandozeilenparametern aufgerufen. Diese stellen die Namen der Spieler dar.

Beispiel: `py -3 main.py Alice Bob`

Es öffnet sich daraufhin ein Fenster, über das Auswahlen von menschlichen Spielern getätigt werden, wenn sie am Zug sind.