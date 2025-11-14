# WTF: C++s Initialisierung macht mich fertig
## Was ist passiert?
Ich habe mir endlich die Zeit genommen, die öffentlichen Header der Open-Asset-Importer-Lib einmal aufzuräumen. 
Im Einzelnen habe ich jeden Header einmal geöffnet, dort aufgeräumt unud fehlende Dokumentationen nachgetragen 
und gegebenenfalls einige Konstruktoren "vereinfacht". In Summe habe ich gefühlt nichts an der grundlegenden 
Funktion verändert. Das dachte ich zumindest. Und dann habe ich den Unittest gestartet. Prompt waren 6 Tests rot. 
Aber warum?

## Deep Dive
Ich hatte einige Konstruktoren, die bereits als default deklariert warren, aus der Implementierung in den Header gepackt. 
Das sah so aus:

Aus

```cpp
.h:
class Foo {
public:
    Foo(); // trivial
};

.cpp:
Foo::Foo() = default;
```

wurde

```cpp
.h:
class Foo {
public:
    Foo() = default; // trivial
};
```
Das hatte aber keine fehlschlagenden Unittests zur Folge. Ein Glück. Also habe ich meinen Pull-Request weiter durchsucht.
Und ich wurde erneut fündig. In der Klass LineSplitter hatte ich ein kleines Detail im Konstruktor geändert. 

Und das sah folgendermaßen aus:

Aus

```cpp
AI_FORCE_INLINE LineSplitter::LineSplitter(StreamReaderLE& stream, bool skip_empty_lines, bool trim ) :
        mIdx(0),
        mCur(),
        mEnd(nullptr),
        mStream(stream),
        mSwallow(),
        mSkip_empty_lines(skip_empty_lines),
        mTrim(trim) {
    mCur.reserve(1024);
    mEnd = mCur.c_str() + 1024;
    operator++();
    mIdx = 0;
}
```

wurde 

```cpp
AI_FORCE_INLINE LineSplitter::LineSplitter(StreamReaderLE& stream, bool skip_empty_lines, bool trim ) :
        mIdx(0),
        mCur(),
        mEnd(nullptr),
        mStream(stream),
        mSkip_empty_lines(skip_empty_lines),
        mTrim(trim) {
    mCur.reserve(1024);
    mEnd = mCur.c_str() + 1024;
    operator++();
    mIdx = 0;
}
```

Das Attribut mSwallow, welche den Default-Wert annehmen sollte, wurde durch meine Änderung implizit initialisiert. 
Meiner Erwartung nach sollte sich daraus keine Änderung im Verhalten zeigen. Aber weit gefehlt! Statt wie erwartet war nun 
der Default ein anderer: true statt false.

Ein kurzer Hintergrund zu der oben genannten Klasse: Diese sorgt dafür, dass eine Text-Datei in ihre einzelnen Zeilen unterteil wird. 
Gibt es einen Fehler, wird eine Exception geworfen. Das Attribut mSwallow sogrt nun dafür , dass diese Exception nicht geworfen wird. 
Das da sich der Default nun von false auf true gesetzt wurde, schlugen all Parsing-Tests fehl, die gerade diese Exception erwarteten. 
Also initialisieren auf false, damit alle Tests wieder erfolgreich beendet wurden und fertig.

## Aber ...
Warum änderte sich der Initialwert, wenn man die Default-Initialisierung aus einem expliziten Konstruktor entfernt. Ich habe erwartet, 
dass sich gar nichts ändert und lag falsch. Ergo: mach implizite Annahmen immer explizit und gut nachvollziehbar. Sonst wird die Welt brennen. 
Das oben beschriebene Verhalten zeigte sich mit MSVC, g++ und clang++.

Es gibt bestimmt einen Grund in der C++-Spec. Aber ich habe es mir erspart, die zu suchen.
