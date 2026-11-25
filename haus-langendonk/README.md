# Haus Langendonk – Animation (4K, 2 Minuten)

Quellcode der Animation zur Geschichte der Wasserburg Haus Langendonk bei Aengenesch (Geldern).
Das fertige Video (ca. 350 MB) ist zu groß für GitHub und liegt deshalb nicht im Repository.

Neu erzeugen:

    npm i three@0.160 playwright
    python3 -m http.server 8765 &          # in diesem Ordner
    python3 music.py                        # erzeugt music.wav
    for k in 0 1 2 3; do node render.js 3840 frames 25 $k 4 & done; wait
    ffmpeg -framerate 25 -i frames/f%05d.jpg -i music.wav -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -shortest Haus_Langendonk_4K.mp4

Quellen: Wikipedia „Haus Langendonk (Geldern)“, KuLaDig.
Bilder (Wikimedia Commons): Frank Vincentz (CC BY-SA 3.0), Stefan K. (CC BY 2.0),
Kupferstich um 1720 und Aufnahme Hermann Gross um 1920 (gemeinfrei).
Die 3D-Szenen sind eine freie Rekonstruktion nach der Beschreibung der Karte von 1790.
