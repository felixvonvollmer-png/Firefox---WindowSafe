# WindowSafe – Produktdefinition V1

```text
DOCUMENT_TYPE: PRODUCT_DEFINITION_SUBJECT
PRODUCT_DEFINITION_ID: WS-PD-20260917-01
REVISION: 1
DOCUMENT_STATE: PROPOSED_FOR_USER_REVIEW
DATE: 2026-09-17
LANGUAGE: de
PROJECT: WindowSafe
PLANNED_TARGET_REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
PROJECT_APPROACH: V6_GREENFIELD
SOURCE_ORIGIN: WindowSafe-Produktgespräch mit dem Nutzer bis einschließlich der Zustimmung zur Erstellung dieses Subjects
METHOD_REFERENCE: V6 Foundation 1, Abschnitte 3–8
METHOD_FOUNDATION_BLOB: 3b139a7dfd70da3ae6c83bbdfa703cb98ef94193
```

Diese Datei ist der Produktdefinitions-Subject, nicht der Approval Record. Eine spätere Nutzerfreigabe wird separat an die genaue Datei und ihre Prüfsumme gebunden. Änderungen erzeugen eine neue Revision. Der hier gewählte Dateiname bestimmt keine spätere Repositorystruktur.

## 1. Ziel, Nutzer und Abgrenzung [WS-GOAL]

WindowSafe ist eine schlichte, lokal arbeitende Firefox-Desktop-Erweiterung für einen Nutzer, der mehrere Fenster mit vielen Tabs verwendet. Sie hält eine eigene persistente Fenster-/Tab-Sicherung vor, unabhängig davon, ob Firefox seine vorherige Sitzung erfolgreich wiederherstellt.

**Kernworkflow:** Firefox startet ohne einige oder alle vorherigen Fenster. Der Nutzer öffnet WindowSafe und stellt die fehlenden Fenster mit den zuletzt erfolgreich gesicherten Tabs wieder her, ohne die Chronik durchsuchen zu müssen.

Zusätzlich verwaltet WindowSafe dauerhaft benannte Fenster, etwa „Arbeit“ und „Recherche“, deren Änderungen laufend gesichert werden. Das Produkt ist kein vollständiger Nachbau von Simple Tab Groups, kein Ersatz für Firefox Session Restore und kein vollständiges Firefox-Profilbackup. Es benötigt keinen eigenen Benutzeraccount, Server oder Cloud-Dienst.

## 2. Quellen und Entscheidungsstand [WS-SOURCE]

| Anker | Bereits im Gespräch festgelegter Inhalt |
|---|---|
| WS-UD-01 | Neues gespeichertes Fenster anlegen; aktuelles Fenster speichern; Eintrag öffnet das Fenster; Änderungen automatisch sichern. |
| WS-UD-02 | Firefox-Wiederherstellung nicht stören; bei deren Fehlschlag letzte Fenster unabhängig wieder öffnen können; tägliches lokales Backup. |
| WS-UD-03 | Sehr geringe zusätzliche Speicher- und CPU-Belastung; unnötigen Mehrverbrauch im MB-Bereich vermeiden, nicht Zuverlässigkeit für Kleinstoptimierungen opfern. |
| WS-UD-04 | Produktname WindowSafe; genanntes Zielrepository; Vorgehen nach V6. |
| WS-UD-05 | Private Fenster ausschließen; „Neues Fenster“ öffnet sofort ein verbundenes Fenster; Löschen des benannten Eintrags lässt das echte Fenster offen; Recovery nur auf Nutzeraktion. |
| WS-UD-06 | Wiederherstellung von URL, Reihenfolge, angeheftet/aktiv genügt ohne Seitensitzungsdaten; Container wurden ausdrücklich einschließlich der dafür besprochenen cookies-Berechtigung akzeptiert, ohne Cookie-Inhalte zu sichern. |
| WS-UD-07 | Nach Erklärung des Unterschieds zwischen benannten Fenstern und automatischer Recovery-Sicherung: alle normalen Fenster berücksichtigen; Tab-Gruppen, Split-Zuordnung und weitere besprochene Zustände berücksichtigen; Hintergrund-Tabs möglichst entladen wiederherstellen. |

Die folgenden **Präzisierungen sind Vorschläge zur jetzigen Freigabe**, keine behaupteten früheren Einzelentscheidungen:

- **WS-P01 – Schließen und Recovery-Historie:** Auch zuletzt geschlossene unbenannte Fenster bleiben innerhalb einer begrenzten Recovery-Historie manuell erreichbar. Eine ungeklärte unvollständige Wiederherstellung darf den geschützten vorherigen Stand auch über mehrere Neustarts hinweg nicht verdrängen.
- **WS-P02 – Fehlender Container:** Betroffene Tabs bleiben erhalten und werden nicht stillschweigend in einer anderen Umgebung geöffnet. Der Nutzer kann einen vorhandenen Container zuordnen oder diese Tabs zunächst auslassen; keine automatische Container-Neuanlage.
- **WS-P03 – Lokale Backups:** Automatischer Backup-Unterordner im Firefox-Downloadverzeichnis, getrennte Zuordnung je WindowSafe-Profilinstanz; regulär die letzten 14 erfolgreich abgeschlossenen Tagesbackups. V1-Backups sind nicht eigens verschlüsselt. Sichere Bereinigung und Schutz ungeklärter Recovery-Stände gehen vor starrer Dateizahl.
- **WS-P04 – Import:** Ein importiertes Backup wird zunächst als zusätzliche Wiederherstellungsquelle aufgenommen. Es ersetzt weder laufende Fenster noch bestehende benannte Einträge automatisch und öffnet noch keine Webseiten.

Eine ausdrückliche Freigabe dieses gesamten Subjects umfasst diese vier Vorschläge. Bis dahin ist diese Revision nicht APPROVED.

## 3. Produktbegriffe [WS-DOMAIN]

**Benanntes Fenster:** Dauerhafter WindowSafe-Eintrag mit Namen und zuletzt erfolgreich gesichertem Tab-Zustand. Er bleibt auch nach dem Schließen des Browserfensters erhalten.

**Automatische Sitzungssicherung:** Erfassung aller relevanten normalen Fenster, auch ohne manuelles Benennen. Sie ist von der Liste dauerhaft benannter Fenster zu unterscheiden.

**Geschützter Wiederherstellungsstand:** Vorhandene Sicherung, die durch einen leeren, teilweisen oder mehrdeutigen Browserstart nicht verkleinert oder durch Historienrotation verdrängt werden darf, solange ihre Wiederherstellung ungeklärt ist.

**Live-Zustand:** Aktuell beobachtete Fenster und Tabs. Beobachtung allein beweist weder Vollständigkeit einer Wiederherstellung noch eine beabsichtigte Löschung.

**Tagesbackup:** Separate lokale Sicherungsdatei der wiederherstellungsrelevanten WindowSafe-Daten; keine Kopie sämtlicher Firefox-Profildaten.

„Sicherer Stand“ bedeutet hier erfolgreich gespeicherter und intern konsistenter Stand, nicht einen absoluten Beweis, dass zuvor nie ein Browser- oder Add-on-Fehler aufgetreten ist.

## 4. Fähigkeiten und Bedienung [WS-CAP]

### Benannte Fenster [WS-CAP-01]

„Aktuelles Fenster speichern“ benennt und verknüpft ein relevantes Firefox-Fenster. „Neues Fenster“ legt einen benannten Eintrag an und öffnet unmittelbar ein verbundenes normales Fenster mit neuem Tab. Namen lassen sich ändern.

Ein Klick öffnet einen geschlossenen Eintrag in einem neuen Fenster. Ist bereits genau ein zugehöriges Fenster geöffnet, wird dieses fokussiert statt dupliziert. Wiederholtes Klicken darf keine konkurrierenden WindowSafe-Öffnungen erzeugen. Beim erneuten Speichern eines bereits verbundenen Fensters wird die bestehende Verbindung verwendet, nicht unbemerkt ein zweiter Schreibgegenstand angelegt.

Das Löschen eines benannten Eintrags lässt das Browserfenster offen und hebt die benannte Verbindung auf. Solange dieses normale Fenster geöffnet ist, bleibt es Teil der automatischen Sitzungssicherung. Alte Backups werden durch das Löschen des Namenseintrags nicht rückwirkend bereinigt; die Oberfläche darf daher keine vollständige Datenlöschung behaupten.

### Laufende Sicherung [WS-CAP-02]

Neue und geschlossene einzelne Tabs, Navigation, Reihenfolge, Verschiebungen zwischen Fenstern und unterstützte Struktur-/Zustandsänderungen werden während des Betriebs mit kurzer, später messbar festzulegender Verzögerung gesichert. Die Sicherung darf nicht ausschließlich beim Beenden stattfinden.

Das Schließen eines ganzen Fensters oder Firefox darf dessen gesicherten Inhalt nicht durch eine Folge leerer Zustände ersetzen. Bewusste einzelne Tab-Schließungen im eindeutig zugeordneten Normalbetrieb aktualisieren dagegen den aktuellen Stand. Historische Stände bleiben nach den Aufbewahrungsregeln verfügbar.

### Firefox-Start und Wiederherstellung [WS-CAP-03]

WindowSafe öffnet beim Browserstart keine Fenster oder Tabs automatisch und verändert Firefox' eigene Wiederherstellungseinstellung nicht. Von Firefox wiederhergestellte Fenster werden bei eindeutiger Zuordnung weiter synchronisiert; auch Änderungen unmittelbar während der Startphase müssen berücksichtigt werden, ohne die alte Sicherung blind zu überschreiben.

Nach einem fehlerhaften Start stehen einzelne Fenster und eine Aktion „Fehlende Fenster wiederherstellen“ bereit. Bereits eindeutig vorhandene Fenster werden nicht zusätzlich geöffnet. Noch laufende, mehrdeutige oder kollidierende Wiederherstellungen werden sichtbar gemacht; ein bloßer Zeitablauf gilt nicht als Nachweis erfolgreicher Vollständigkeit.

Sind nur einige Tabs eines Fensters vorhanden, bleiben die fehlenden Tabs gesichert. Neue Live-Änderungen werden getrennt vom geschützten Ausgangsstand erhalten. Der Nutzer kann fehlende Tabs ergänzen oder den aktuellen Zustand ausdrücklich als gewünschten neuen Stand übernehmen. Vor einer solchen Übernahme bleibt ein vorheriger Wiederherstellungspunkt erhalten.

### Konflikte und Status [WS-CAP-04]

Bei fehlender oder doppelter Identität, unklarer Zuordnung, Lese-/Schreibfehlern oder unvollständigem Recovery wird keine destruktive Zusammenführung geraten. Gleiche URLs allein beweisen keine Tab-Identität; zwei absichtlich gleiche Tabs bleiben zwei Tabs.

Die Oberfläche unterscheidet mindestens geöffnet, geschlossen, Wiederherstellung ungeklärt und Sicherung fehlgeschlagen. Angezeigt werden Name beziehungsweise verständliche Fensterbezeichnung, Tab-Anzahl sowie Zeitpunkt des letzten erfolgreichen Sicherungs-/Backupstands. Einzelne nicht wiederherstellbare Einträge bleiben mit Hinweis erhalten; ein Teilergebnis darf nicht als vollständig erscheinen.

Die Oberfläche bleibt auf Fensterliste, notwendige Aktionen und wenige Einstellungen beschränkt. Es entsteht kein eigener komplexer Tab-Manager.

## 5. Wiederherstellungsumfang und Firefox-Grenzen [WS-RESTORE]

| Gegenstand | V1-Verhalten |
|---|---|
| Tabs | URL, Titel zur Orientierung, Reihenfolge, aktiver Tab und angehefteter Zustand. |
| Stummschaltung | Benutzerseitigen Stummzustand wiederherstellen; kein automatisches Fortsetzen von Medien. |
| Container | Vorhandene richtige Umgebung verwenden; fehlende oder mehrdeutige Umgebung nach WS-P02 behandeln. Keine Cookie-, Login- oder Passwortsicherung. |
| Native offene Tab-Gruppen | Mitgliedschaft, Gruppenname, Farbe und eingeklappten Zustand sichern und mit unterstützten APIs rekonstruieren. |
| Split View | Auslesbare Zusammengehörigkeit sichern. Vollständige native Neuerzeugung nur bei nachgewiesener unterstützter API. Sonst beide Tabs als gewöhnliche Tabs erhalten und die Einschränkung anzeigen. Kein Nachbau durch eingebettete Webseiten oder privilegierte Hacks. |
| Lesemodus | Absicht erhalten; tatsächliche Anzeige best-effort, andernfalls normale Originalseite mit erkennbarem Fallback. |
| Entladene Tabs | Bei WindowSafe-Recovery Hintergrund-Tabs standardmäßig möglichst ohne Laden der Webseiten anlegen. Der aktive Tab je Fenster wird normal geladen. Einschränkungen von Eigenschaftskombinationen müssen geprüft werden; kein stiller Fallback auf massenhaftes gleichzeitiges Laden. |
| Fensteranordnung | Größe, Position und Zustand best-effort. Bei ungeeigneter/unklarer Bildschirmkonfiguration sichere sichtbare Standardanordnung statt ungeprüfter alter Koordinaten. |

Die Zusagen gelten für die in der Technical Foundation festzulegende unterstützte Firefox-Umgebung. API-Fähigkeiten werden nicht nur aus Firefox-Oberflächenfunktionen abgeleitet. Die Dokumentation bestätigt unter anderem Container-/Discarded-/Reader-Optionen sowie Gruppen- und Split-Metadaten; eine Versions- und Laufzeitprüfung ersetzt dies nicht. [M1–M4]

Private Browserfenster werden weder live noch in Historie oder Backups erfasst. Ein normaler Container mit dem Namen „Privat“ ist davon zu unterscheiden.

Firefox-eigene gespeicherte und geschlossene Gruppen, Tab Notes, vertikale Tab-Darstellung, Profildaten sowie Sidebar-/Gruppenmodelle anderer Erweiterungen werden nicht als eigene WindowSafe-Datensysteme nachgebaut. Bewusst geschlossene Gruppen sind keine automatisch zu reparierenden Verluste. In normalen Fenstern vorhandene, durch andere Add-ons verborgene Tabs gelten nicht allein wegen ihrer Unsichtbarkeit als gelöscht; das Fremd-Add-on wird nicht ferngesteuert.

Sonderfenster, insbesondere Web-App-, Popup-, DevTools- und Picture-in-Picture-Fenster, erhalten kein ungeprüftes Versprechen nativer Wiederherstellung. Ihre sichere Erkennung und Behandlung ist vor Umsetzung der Erfassung zu klären; nicht zuverlässig abgrenzbare Fälle dürfen nicht stillschweigend als vollständig unterstützt gelten.

Nicht automatisch öffnungsfähige Adressen bleiben als erkennbare Einträge erhalten, soweit sie überhaupt erfasst werden können. Firefox beschränkt unter anderem privilegierte interne und lokale Datei-URLs beim Anlegen von Tabs. WindowSafe umgeht solche Beschränkungen nicht. [M1]

## 6. Backups, Import und Datenschutz [WS-BACKUP]

Bei laufendem Firefox wird nach einem lokalen Kalendertagswechsel beziehungsweise beim ersten geeigneten Start geprüft, ob seit dem letzten erfolgreichen Backup relevante Änderungen vorliegen. Dann wird ein Tagesbackup erstellt; bei unverändertem Zustand ist keine identische neue Datei nötig. Ein gespeicherter Erfolgszeitpunkt gilt erst nach abgeschlossenem Dateischreiben. Fehler bleiben sichtbar und müssen später erneut versucht werden, ohne schnelle Dauerschleifen.

Während Firefox nicht läuft, erzeugt das Add-on keine Backups. Ein Start nach einer Pause sichert den noch vorhandenen Stand, rekonstruiert aber keine unbeobachteten Zwischenstände.

Automatische Backups liegen nach WS-P03 in einem WindowSafe-Unterordner des Firefox-Downloadverzeichnisses. Die normale Downloads-API erlaubt relative Unterordner, aber keine beliebigen absoluten Zielpfade. V1 benötigt dafür keinen separat installierten Systemhelfer. [M5]

Das Backup enthält die benannten Fenster, automatische Recovery-Stände, erhaltene Strukturmetadaten und erforderliche Einstellungen mit Formatversion und Zeitangabe. Ungeklärte ältere Recovery-Inhalte müssen ebenfalls enthalten bleiben und dürfen nicht durch einen fehlerhaften aktuellen Start ersetzt werden.

Regulär bleiben die letzten 14 erfolgreichen Tagesbackups pro Instanz erhalten. Bereinigung erfolgt nur für eindeutig eigene, verwaltbare Backup-Dateien und erst nach erfolgreicher neuer Sicherung. Fremde Downloads werden nicht gelöscht. Ist sichere Bereinigung nicht möglich, bleibt die Datei erhalten und die Abweichung wird angezeigt; die Zahl 14 ist keine Garantie für beliebig extern verschobene Dateien. Die Downloads-API entfernt Dateien über bekannte Download-IDs, nicht über einen freien allgemeinen Dateisystemzugriff. [M6]

Ein Import wird vor Übernahme auf Format und Konsistenz geprüft, führt keinen Code aus und behandelt URLs als Daten. Beschädigte oder inkompatible Daten verändern den vorhandenen Bestand nicht. Gemäß WS-P04 ist der Standard eine zusätzliche Recovery-Quelle; Öffnen oder Ersetzen erfolgt erst durch die jeweilige Nutzeraktion. Aus einem anderen Profil importierte Containerreferenzen dürfen nicht ungeprüft lokalen Containern gleichgesetzt werden.

URLs, Suchparameter, Titel und Fensternamen können vertrauliche Informationen enthalten. WindowSafe überträgt Sicherungsdaten nicht an eigene Server, Telemetrie-, Analyse- oder externe Favicon-Dienste. Der normale Seitenaufruf nach einer Wiederherstellungsaktion bleibt ein normaler Browserzugriff. V1-Backup-Dateien sind nicht eigens verschlüsselt; etwaige Kompression ist kein Zugriffsschutz. Ein vom Nutzer anderweitig synchronisierter Downloadordner liegt außerhalb der Kontrolle des Add-ons.

Erforderliche Berechtigungen werden auf die vereinbarten Funktionen begrenzt. Die akzeptierte cookies-Berechtigung dient dem Containerkontext, nicht dem Lesen, Exportieren oder Verändern von Cookie-Inhalten. Keine Inhalts-Skripte zum Auslesen von Webseiten, keine Passwort-/Formulardatensammlung und keine direkte Manipulation interner Firefox-Sitzungsdateien.

## 7. Ressourcenschonung und Zuverlässigkeit [WS-QUALITY]

WindowSafe arbeitet ereignisorientiert. Keine regelmäßigen Vollscans aller Tabs im normalen Leerlauf; zeitlich begrenzte Start-/Abgleicharbeit und seltene Backup-Terminprüfungen sind davon zu unterscheiden. Relevante Änderungen werden gebündelt, unveränderte Daten nicht grundlos erneut gespeichert. Einzelne Tab-Änderungen dürfen nicht routinemäßig sämtliche Sitzungen und Historien neu schreiben.

Keine persistierten Favicon-Bilddaten, Screenshots, Seiteninhalte, Medien oder vollständigen Navigationshistorien. Historien und Zwischenspeicher sind begrenzt; kein unnötiges dauerhaftes Vorhalten aller alten Stände im RAM. Ressourcengrenzen dürfen nicht durch stilles Wegwerfen benötigter Recovery-Daten eingehalten werden.

Vor Implementierungsfreigabe werden in der Technical Foundation getrennte, reproduzierbar messbare Ziele für zusätzlichen RAM, persistente Daten, Backupgröße, Leerlauf-/Last-CPU, Schreibaufwand und maximale reguläre Sicherungsverzögerung festgelegt. Referenzumfang und Testumgebung gehören dazu. Es ist noch keine unbelegte pauschale MB-Grenze oder absolute Null-CPU-Garantie vereinbart.

Priorität: **kein stiller Verlust und kein falscher Sicherheitsstatus; danach geringer Ressourcenverbrauch ohne unnötige Komplexität.** Nach hartem Prozess-/Systemabbruch können jüngste noch nicht erfolgreich persistierte Änderungen fehlen. WindowSafe verspricht Wiederherstellung des letzten erfolgreichen Standes, nicht verlustfreie Rettung noch ungespeicherter Daten, zerstörter Profile oder ausgefallener Datenträger. Der ergänzende Dateibackup-Pfad bleibt deshalb wichtig; Extension-Speicher wird bei Deinstallation normalerweise entfernt. [M7]

## 8. Prüfbarkeit der V1 [WS-ACCEPTANCE]

Diese Szenarien sind Produkt-Akzeptanzziele, keine bereits ausgeführten Tests und keine vorgeplante Feature-/Task-Reihenfolge:

| Anker | Erwarteter Nachweis |
|---|---|
| WS-AC-01 | Benennen, Öffnen, Fokussieren, Umbenennen und Entfernen eines Eintrags funktionieren ohne ungewollte Fensterschließung oder Doppelbindung. |
| WS-AC-02 | Neue, navigierte, verschobene und einzeln geschlossene Tabs sowie unterstützte Zustände erscheinen nach erfolgreicher Sicherung im richtigen Fensterstand. |
| WS-AC-03 | Korrekte native Wiederherstellung mehrerer benannter und unbenannter Fenster führt zu keiner zusätzlichen WindowSafe-Öffnung; Live-Sicherung läuft weiter. |
| WS-AC-04 | Vollständiger Restore-Ausfall: alle Fenster des geschützten vorherigen Standes sind einzeln beziehungsweise gemeinsam manuell wieder öffnungsfähig. |
| WS-AC-05 | Teilweiser, verzögerter oder mehrfach fehlgeschlagener Restore verdrängt fehlende Fenster/Tabs nicht; neue Live-Änderungen bleiben zusätzlich erhalten. |
| WS-AC-06 | Ganzes Fenster schließen, mehrere Fenster nacheinander schließen, Firefox beenden und abrupten Abbruch testen: vorhandene erfolgreich gespeicherte Recovery-Stände werden nicht durch Schließereignisse geleert. |
| WS-AC-07 | Identitätskonflikte und mehrere Tabs mit identischer URL verursachen weder erratene Zusammenführungen noch stillen Verlust. |
| WS-AC-08 | Gruppen, Container und sonstige vereinbarte Zustände werden innerhalb nachgewiesener Fähigkeiten erhalten; fehlender Container/Split-API/URL-Zugriff erzeugt erkennbare, datenerhaltende Einschränkungen. |
| WS-AC-09 | Private Fenster sind in keiner Sicherung enthalten; Daten bleiben zwischen Profilinstanzen getrennt; Add-on sammelt keine Cookie-/Seiteninhalte. |
| WS-AC-10 | Tageswechsel, Neustart, ausgeschalteter Browser, Backupfehler, Aufbewahrung und Import sind geprüft; beschädigter Import verändert keinen bestehenden Stand. |
| WS-AC-11 | Vereinbarte Lastprofile erfüllen die gebundenen Ressourcen- und Sicherungsverzögerungsziele; große Wiederherstellungen laden Hintergrundseiten nicht unkontrolliert gleichzeitig. |

## 9. Nichtziele und offene Folgeentscheidungen [WS-NONGOALS / WS-OPEN]

Nicht Teil von V1: Cloud-Sync, geräte-/profilübergreifende Live-Synchronisation, vollständiges Profil-/Cookie-/Login-Backup, Speicherung von Formularen/Scrollposition/Back-Forward-Verlauf, eigene komplexe Tab-Gruppenlogik, Lesezeichen als Hauptdatenbank, native Systemhilfssoftware oder automatisches Recovery beim Browserstart.

| Anker / Status | Punkt und spätester Klärungstrigger |
|---|---|
| WS-OL-01 / OPEN_LATER | Unterstützte Firefox-Mindestversion, Betriebssystem-Testmatrix und API-Kombinationen: in Technical Foundation, vor Agenten-Implementierungsfreigabe. Materielle Abstriche erfordern Nutzerentscheidung. |
| WS-OL-02 / OPEN_LATER | Referenzlast, Ressourcenbudgets, maximale Sicherungsverzögerung und interne begrenzte Historie: in Technical Foundation, vor Agenten-Implementierungsfreigabe; WS-P01 und WS-QUALITY dürfen nicht abgeschwächt werden. |
| WS-OL-03 / OPEN_LATER | Technische Erkennung von Restore-Vollständigkeit, Sonderfenstern, versteckten Tabs und instanzübergreifenden Containerkonflikten: vor Freigabe der betroffenen Implementierung. Unklarheit ist kein Auftrag zum Raten. |
| WS-OL-04 / OPEN_LATER | Installations-/Signierungs-/Verteilungsweg, Lizenz und etwaige Veröffentlichung: vor Auslieferung; kein öffentlicher Release, neuer Anbieter, Vertrag oder kostenpflichtiger Dienst dadurch autorisiert. |

Interne Speicherengine, Manifestgeneration, Programmiersprache, Dateistruktur, Kompressionsverfahren und genaue Ereignisverarbeitung sind noch keine bindende Implementierungsplanung. Sie werden nach Produktfreigabe technisch vorbereitet beziehungsweise innerhalb der gebundenen Grenzen vom Agenten entschieden.

Diese Produktfreigabe autorisiert keine Implementierung, Repositorymutation, Veröffentlichung oder Tests gegen das tatsächlich verwendete Firefox-Profil. Die weitere Arbeit folgt den getrennten V6-Vorbereitungs-, Review- und Ausführungsgates.

## 10. Quellen zur technischen Einordnung [WS-REFERENCES]

Produktregeln stammen aus dem Gespräch beziehungsweise den sichtbar vorgeschlagenen Präzisierungen. Die folgenden offiziellen Quellen wurden am 17.09.2026 gelesen; sie stützen API-Grenzen, sind aber weder Laufzeittests noch technische Freigaben:

- **F1:** V6 Foundation 1 im Repository `felixvonvollmer-png/projektbeschreibung-und-geruest`; Git-Blob `3b139a7dfd70da3ae6c83bbdfa703cb98ef94193`. Product-Definition-Approval insbesondere Abschnitt 8. Eingefrorene Zuordnung laut `foundations/v6/freezes/V6-F1-FREEZE-20260906-01/freeze_manifest.md`.
- **M1:** MDN, tabs.create(): https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/create
- **M2:** MDN, tabGroups und TabGroup: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabGroups und https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabGroups/TabGroup
- **M3:** MDN, tabs.Tab: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/Tab
- **M4:** MDN, Working with the Tabs API, „Working with tab split views“: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Working_with_the_Tabs_API
- **M5:** MDN, downloads.download(): https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/download
- **M6:** MDN, downloads.removeFile(): https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/removeFile
- **M7:** MDN, storage.local: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/local
- **M8:** MDN, windows.create(): https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/create
- **M9:** MDN, sessions.setWindowValue() und tabs.onRemoved: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sessions/setWindowValue und https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/onRemoved
