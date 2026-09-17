# WindowSafe – Technical Foundation Preparation

```text
DOCUMENT_TYPE: TECHNICAL_FOUNDATION_PREPARATION_SUBJECT
PREPARATION_SUBJECT_ID: WS-TFP-20260917-01
REVISION: 6
AUTHORING_STATE: FORMAL_DECISION_REPRESENTATION_CORRECTION_CANDIDATE__T05_R2_UNCHANGED__INDEPENDENT_REREVIEW_REQUIRED
PREVIOUS_REVISION_SHA256: 74b324e63f5368b47b7b301ffd9761dd9060c70f8c6e1c8189d91792f8138bd6
PREVIOUS_REVIEW_ID: WS-TFPR-20260917-03
PREVIOUS_REVIEW_VERDICT: PASS
PREVIOUS_OPEN_FINDINGS: NONE
APPROVED_DECISION_SUBJECT_ID: WS-T05-R2-20260917-01
APPROVED_DECISION_SUBJECT_SHA256: 8d2b565beb28ca47e63df59b5d7d9236dd99c6f1967dba1190553c0a66b5800c
CURRENT_REREVIEW_ID: WS-TFPR-20260917-04
BASE_DECISION_RECORD_ID: WS-TD-20260917-01
BASE_DECISION_RECORD_SHA256: 4f10e70c558dc2ee6df59c47b48af037842800c5339a147b51f9e9f32f20aeaf
T05_R2_DECISION_RECORD_ID: WS-TD-20260917-03
DATE: 2026-09-17
PREPARER_ROLE: PROJECT_LLM_TECHNICAL_FOUNDATION_PREPARATION
PROJECT_TYPE: V6_GREENFIELD
PRODUCT_DEFINITION: WS-PD-20260917-01 / Revision 1
PRODUCT_SHA256: fff235b7591f483b9b31c945911a6b5950d29fac931b9136438ae5586c756900
PRODUCT_APPROVAL: WS-PD-APPROVAL-20260917-01
APPROVAL_SHA256: a655d1fb0a594997e1f6da00c7e8a36bb6c5807ac844ce9fbf04ccb7d1afd4a5
FOUNDATION_1_BLOB: 3b139a7dfd70da3ae6c83bbdfa703cb98ef94193
FOUNDATION_2_REFERENCE_BLOB: ff49e56aba09881e9e4a22dc8225949fbc4b54f6
TARGET_REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
TARGET_REPOSITORY_ID: 1374094477
INDEPENDENT_REVIEW_REQUIRED: YES
INDEPENDENT_REVIEW_EXECUTED_FOR_THIS_REVISION: NO
READY_FOR_AGENT: NO
IMPLEMENTATION_AUTHORIZED: NO
```

## 1. Herkunft, Verbindlichkeit und aktueller Stand [WS-TF-SOURCE]

Die freigegebene Produktdefinition und ihr separater Approval Record sind die Product Truth. Ihre Originalbytes wurden lokal geprüft; SHA-256 und Bytelänge des Subjects stimmen mit der Freigabe überein. Beide Dateien bleiben unverändert. Dieser Entwurf ist kein Product-Approval-Ersatz, kein unabhängiges Review und kein Programmierauftrag.

Die V6-Übersicht bestätigt dieselben eingefrorenen Foundation-Referenzen. Foundation 1 wurde zusätzlich in den Abschnitten zu Recherche, Preparation, Binding und Review gelesen; die GitHub-Antwort liefert den erwarteten Foundation-Blob. Die genannten historischen Candidate-Statusfelder ändern den Freeze nicht. Kein erneuter Foundation-Pair-Review wurde durchgeführt. [F1]

Historische read-only-Zielprüfung aus Revision 1 am 17.09.2026 (in Revision 2, 3, 4, 5 und 6 nicht erneut ausgeführt): GitHub meldet Repository-ID **1374094477**, Sichtbarkeit **public**, Default-Branch-Name **main**, aber eine leere Branchliste. Daher gibt es noch keinen hier bindbaren `main`-Commit. Dieser Stand muss vor einem späteren Schreibauftrag erneut geprüft werden. Tool-Schreibfähigkeit ist keine Autorisierung. Keine GitHub-Mutation, Installation, Firefox-Profiländerung oder Produktimplementierung ist in dieser Vorbereitung erfolgt. [G1]

Verbindlich sind die freigegebenen Produktgrenzen, **T01–T04** aus **WS-TD-20260917-01**, **T05-R2** aus dem formal korrigierten maschinenlesbaren Entscheidungsrecord **WS-TD-20260917-03** sowie **G01 = öffentlich beibehalten**. Alle übrigen Architekturvorschläge bleiben `DESIGN_DIRECTION_OR_PREFERRED_DEFAULT`; Revision 5 erhielt mit `WS-TFPR-20260917-03` unabhängig `PASS`; die nachträglich korrigierte immutable Decision-Record-Repräsentation und diese Revision 6 benötigen vor `READY_FOR_AGENT` einen engen erneuten Rereview. Reversible Details bleiben agent-owned; keine Datei-, Klassen-, Funktions-, Worker-, Task-, PR- oder Commit-Reihenfolge wird vorgegeben.

**Revision 6 ist ausschließlich der formale Propagationskandidat nach dem unabhängigen `PASS` von `WS-TFPR-20260917-03`.** Das PASS-Resultat bleibt unverändert historische Evidence für exakt Revision 5 plus `WS-TD-20260917-02`. Nach diesem PASS wurde separat festgestellt, dass der maschinenlesbare Decision Record die Einzellaufgrenzen mit `MAX_EXCLUSIVE` bezeichnet, obwohl die freigegebene T05-R2-Regel `kein gültiger Lauf > 15 % / > 30 %` exakt 15 % beziehungsweise 30 % zulässt. `WS-TD-20260917-03` korrigiert deshalb nur die Feldnamensemantik auf `MAX_INCLUSIVE`; T05-R2 selbst, alle Zahlen, T01–T04, G01, Plattformgate und Safety-Regeln bleiben unverändert. Weil die immutable Decision-Record-Referenz Teil der Pre-Agent-Bindung ist, wird diese neue Subject-Revision vor `READY_FOR_AGENT` erneut unabhängig als Delta rereviewt.

## 2. Entschiedene technische Grenzen [WS-TF-DECISIONS]

| ID | Freigegebene technische Entscheidung | Bedeutung / Trigger |
|---|---|---|
| **T01** | Firefox Desktop **156 als anfängliche Mindest-/Referenzversion**, V1-Testumfang Windows und Ubuntu Desktop; keine zugesagte Abdeckung älterer Firefox-Versionen, ESR, macOS oder Mobilbrowser. | Firefox 156 ist seit 15.09.2026 im Release-Kanal. Dies ist eine gewählte schlanke Testgrenze, nicht die Behauptung, alle APIs erforderten 156. Weitere Versionen erst nach Regressionsevidence. Exakte OS-Builds, Firefox-Build-ID und Testhardware werden im späteren Test-Envelope gebunden; keine Behauptung über das aktuell installierte Nutzersystem. [M01] |
| **T02** | Referenzlast **500 Tabs / 10 Fenster**, Stresstest **2.000 Tabs / 20 Fenster**; verbindliche Startziele nach Abschnitt 9, insbesondere bei der Referenzlast regulär spätestens **2 Sekunden** Sicherungsverzögerung. | Prüfgrößen, keine künstlichen Tab-Limits. Zahlen sind freigegebene Ziele, keine gemessenen Firefox-Ergebnisse. Überschreitung verlangt Optimierung oder eine sichtbare neue Entscheidung, nicht stilles Abschwächen. |
| **T03** | Reguläre interne Historie: bis zu **14 unterscheidbare abgeschlossene Sitzungscheckpoints** und **50 zuletzt geschlossene Fensterstände**, zusätzlich aktueller Stand und benannte Fenster. | Ungeklärte Recovery-Stände und ihre benötigten Inhalte sind von dieser Rotation ausgenommen. Bei Mehrverbrauch warnen statt geschützte Daten löschen. Die bereits freigegebenen 14 externen Tagesbackups sind eine andere Aufbewahrungsebene. |
| **T04** | Lokale **native IndexedDB** für zusammenhängende Recovery-Daten; zusätzlich `unlimitedStorage` für die Persistenz-/Quota-Richtung und `contextualIdentities` für vorhandene Container. | Neue Berechtigungspräzisierung: `unlimitedStorage` ist kein Freibrief für Speicherverbrauch. Mozilla dokumentiert damit u. a. persistente IndexedDB-Datenbanken ohne separaten Erstellungsdialog. Die Container-API benötigt `cookies` und `contextualIdentities`; ihre Verwendung kann die Firefox-Containerfunktion browserseitig aktivieren. Keine Container-Neuanlage durch WindowSafe, keine Cookie-Inhalte und keine Host-Berechtigungen. [M04, M08] |

**G01 / entschieden:** Das Repository **felixvonvollmer-png/Firefox---WindowSafe bleibt öffentlich**. Die frühere Empfehlung „zunächst privat“ ist durch die Nutzerentscheidung ersetzt. Diese Sichtbarkeitsentscheidung ist kein Schreib- oder Veröffentlichungsauftrag für dieses Paket. Echte URL-/Sitzungsdaten, Profile, Cookies und Secrets bleiben ausgeschlossen. Git-/Merge-/CI-/Provider-Berechtigungen gehören später in einen separaten Execution Envelope.

**T05-R2 / freigegeben:** Last-CPU-Vertrag gemäß `WindowSafe_Last_CPU_Decision_WS-T05-R2-20260917-01.md@sha256:8d2b565beb28ca47e63df59b5d7d9236dd99c6f1967dba1190553c0a66b5800c`. Harte Dauerlastgrenzen: R500 Median ≤ 10 % eines CPU-Kerns und kein gültiger Lauf > 15 %; R2000 Median ≤ 20 % und kein gültiger Lauf > 30 %. Soft-Ziele 5 % / 10 % sind ausdrücklich nicht acceptance-blockierend und erzwingen allein keinen Architekturumbau. Die frühere unfreigegebene 1-%/2-%-Fassung bleibt nur historische Evidence.

## 3. Systemrichtung und Verantwortungsgrenzen [WS-TF-ARCH]

**Empfehlung:** Firefox-only WebExtension mit Manifest V3, einer nicht persistenten Background/Event Page und einer nur bei Bedarf geöffneten schlanken HTML/CSS-Oberfläche. Firefox dokumentiert für MV3 Event Pages; ein Chrome-only-Service-Worker-Gerüst ist hier nicht die passende Basis. Listener müssen synchron bei Auswertung der Background-Skripte registriert werden. [M02, M03]

Die logischen Verantwortungen sind:

```text
Firefox-Ereignisse + gezielte Zustandsabfragen
                ↓
Erfassung und Identitätsabgleich
                ↓
Recovery-Regeln / konsistentes Zustandsmodell
                ↓
ein kontrollierter Schreibpfad → lokale Recovery-Datenbank
                ├→ kleine Listenansichten für die Oberfläche
                └→ unveränderlicher Exportstand → Downloads-Backup

Nutzeraktion → validierter Restore-/Importauftrag
                ↓
begrenzte Browseroperationen + beobachteter Ergebnisabgleich
```

Dies sind fachlich-technische Grenzen, keine vorgeschriebenen Dateien oder Klassen. Die Oberfläche sendet validierte Absichten und liest kompakte Ansichten; sie führt nicht einen zweiten unabhängigen Datenbank-Schreibpfad ein. Backup und Import benutzen denselben Konsistenzvertrag. Kein Server, Native-Messaging-Helper, Webseiten-Content-Script oder Fernzugriff auf Firefox-Sitzungsdateien.

Für die Umsetzung wird **TypeScript mit strenger Typprüfung, ausgegeben als lokales JavaScript, und eine native kleine Oberfläche ohne UI-Framework** empfohlen. Das ist eine reversible Entwicklungspräferenz. Node.js und Build-/Testtools sind Entwicklungswerkzeuge, keine Laufzeitvoraussetzung auf dem Nutzerrechner. Mozilla `web-ext` ist die bevorzugte Packaging-/Manifestprüfrichtung; genaue kompatible Versionen werden im Bootstrap festgeschrieben. Die aktuelle Dokumentation verlangt für web-ext 10 Node.js 22 oder neuer. [M22]

Native Plattformfunktionen sind hier der erste Wiederverwendungskandidat: Firefox-APIs, IndexedDB, Streams, JSON. Ein Session-Manager-Fork, ein Datenbankframework und eine eigene Kompressionsbibliothek werden ohne konkreten Nachweis nicht hinzugefügt. Es wurde kein fremder Code kopiert und keine Abhängigkeit installiert. Benötigte Entwicklungsabhängigkeiten werden später auf Wartung, Lizenz, Provenienz und transitive Kosten geprüft; dieser Entwurf behauptet keine bereits abgeschlossene Dependency-Auditierung.

## 4. Harte Invarianten aus Product Truth [WS-TF-INVARIANTS]

| ID | Bindende Grenze | Produktbezug |
|---|---|---|
| I01 | Nicht beobachtete Fenster/Tabs beim Start sind **kein Löschbefehl**. Fehlende Daten, Identitäten und verzögerte Ereignisse erzeugen Unsicherheit, nicht einen kleineren vermeintlich sicheren Stand. | WS-CAP-03/04, WS-P01 |
| I02 | Kein automatisches Recovery beim Browserstart; keine Änderung der Firefox-Restore-Einstellung. Ein benanntes oder erkanntes bereits offenes Fenster wird nicht routinemäßig dupliziert. | WS-CAP-01/03 |
| I03 | Geschützte Wurzeln bleiben über weitere Neustarts erhalten, bis Vollständigkeit ausreichend belegt oder eine ausdrückliche Nutzerdisposition gespeichert ist. Keine Verdrängung nur durch Zeit-, Größen- oder Historiengrenzen. | WS-DOMAIN, WS-P01 |
| I04 | Ganzen Fensterinhalt beim Schließen nicht durch leere Zwischenstände ersetzen. Einzelschließung und Transfer im bestätigten Normalbetrieb sind andere Übergänge. | WS-CAP-02 |
| I05 | Ein Erfolgshinweis setzt den erfolgreichen relevanten Speicherabschluss voraus. Gespeichert, Browserfenster angelegt, Webseiten geladen und Dateibackup abgeschlossen sind verschiedene Zustände. | WS-CAP-04, WS-BACKUP |
| I06 | Private Fenster/Tabs nicht speichern, auch nicht in Logs, Session-Tags, Exporten oder importierten Recovery-Beständen. Unklare Privatheit wird nicht optimistisch angenommen. | WS-RESTORE, WS-AC-09 |
| I07 | Container nicht still wechseln; gleiche URL oder gleichlautender Container-/Fenstername ist kein Identitätsbeweis. | WS-P02, WS-CAP-04 |
| I08 | Import verändert bestehende Fenster/benannte Einträge nicht automatisch. Ungültiger Import lässt den bisherigen Bestand unberührt. | WS-P04 |
| I09 | Keine unnötigen Seitenladungen, Datenkopien, Netzwerkabfragen, Dauer-Timer oder Vollscans im normalen Leerlauf. | WS-QUALITY |
| I10 | Fehler, Browserbeschränkungen oder nicht unterstützte Kombinationen sichtbar erhalten; kein unbemerktes Verwerfen, privilegierter Hack oder falscher Vollständigkeitsstatus. | WS-RESTORE, WS-CAP-04 |

## 5. Datenhaltung, Identität und Konsistenz [WS-TF-DATA]

### 5.1 Eine dauerhafte Recovery-Wahrheit

**Richtung T04:** IndexedDB trägt den konsistenten Recovery-Graphen einschließlich seiner Wurzeln, Revisionen, Import-/Restoreaufträge, Profilinstanzkennung und Backup-Register. Ein Transaktionsabschluss bündelt zusammengehörige Änderungen. Ein fehlgeschlagener Batch lässt die alte veröffentlichte Revision gültig; eine neue Revision wird nicht als teilweise aktualisierter alter Stand sichtbar. Für sicherheitsrelevante Commits wird die standardisierte `durability: "strict"`-Richtung vorgeschlagen, mit nachgewiesener Unterstützung und gemessenem Schreib-/Energieaufwand. Keine experimentellen Flush-Modi als versteckte Abhängigkeit. Ein solches API-Versprechen ist trotzdem keine Garantie gegen Hardware- oder Profilverlust. [M05]

`storage.local` darf kleine, nicht transaktionskritische Einstellungen halten. Es entsteht **keine zweite vollständige Sitzungskopie** dort. Die API dokumentiert keinen von uns hier belegten, mehrere Aufrufe umfassenden Transaktionsvertrag; eine eigene Transaktionsschicht darüber wäre zusätzlicher Prüfaufwand. `storage.session` ist optional für kleine flüchtige Laufzeitkennungen/Indizes, nicht für die einzige Kopie einer Sicherung. Es liegt im RAM und wird nicht auf Festplatte persistiert. [M06, M07]

Die native Speicherengine wird nicht durch eine neue komplexe Datenbankbibliothek ersetzt, nur um wenige API-Aufrufe zu sparen. Persistenz, Quota-Fehler, Löschen von Browserdaten und Erweiterungsupdate müssen an der gebundenen Zielversion geprüft werden; `unlimitedStorage` beseitigt insbesondere nicht jeden Fehler bei vollem Datenträger. [M06]

### 5.2 Unveränderliche Inhalte teilen, keine Tab-Identitäten zusammenlegen

Ein gespeicherter Stand referenziert unveränderliche Tab-/Gruppen-/Fensterrevisionen. Benanntes Fenster, aktuelle Sitzung und geschützter Checkpoint dürfen dieselbe unveränderte Revision referenzieren. Nur betroffene Informationen erhalten eine neue Revision; ein einzelner Tabwechsel kopiert nicht die gesamte Historie. Die genaue Record-Granularität bleibt agent-owned und muss die Schreibbudgets erfüllen.

Logisch verschieden bleiben: Profilinstanz, Browserlauf, logisches Fenster, logischer Tab, gespeicherte Gruppe/Splitbeziehung, Revision und Restoreversuch. Eine URL ist Nutzinhalt, kein Primärschlüssel. Zwei gleiche URLs bleiben zwei Tabs. Mehrere Roots mit identischem Inhalt sind keine Begründung, zwei unterschiedliche Fenster zusammenzuführen.

Bereinigung darf ausschließlich unerreichbare Revisionen beziehungsweise ausdrücklich regulär ausrotierbare Historie entfernen. Aktuelle, benannte, geschützte, importierte oder für einen laufenden Export benötigte Roots zählen zur Erreichbarkeit. Quota-Druck erzeugt eine sichtbare Warnung/Sicherungspause, nicht heimliche Löschung. Bei Warnung bleibt unterscheidbar, bis zu welcher Revision tatsächlich gespeichert wurde.

### 5.3 Firefox-Session-Metadaten als Hinweise, nicht als Sicherung

Eigene kleine Window-/Tab-Identitäten werden über `sessions.setWindowValue` und `sessions.setTabValue` mit Browserobjekten verbunden. Firefox kann solche Werte beim Wiederherstellen wieder zugänglich machen; normale numerische Browser-IDs ersetzen diese persistente logische Identität nicht. Keine vollständigen URL-Listen zusätzlich in Session-Tags schreiben. Die Werte sind nicht die unabhängige Recovery-Datenbank. [M09, M10]

Schreiben in IndexedDB und Setzen eines Firefox-Sessionwerts bilden **keine gemeinsame atomare Transaktion**. Der Abgleich muss unterbrochene Markierung/Bestätigung erkennen. Unvollständige oder duplizierte Tags dürfen nicht als zuverlässiger Nachweis gelten. Ein neu geöffnetes oder dupliziertes Browserobjekt kann alte Tags übernehmen: Eindeutigkeit prüfen, nicht blind vertrauen. Eigene Gruppenkennungen werden über das gespeicherte Modell und Tab-Zuordnungen geführt; es wird keine nicht dokumentierte `setGroupValue`-API vorausgesetzt.

## 6. Start, Normalbetrieb und Recovery [WS-TF-RECOVERY]

### 6.1 Zustandsübergänge statt eines festen Startup-Timers

Mindestens die fachlichen Zustände **ABGLEICH_LÄUFT**, **VERBUNDEN**, **RECOVERY_UNGEKLÄRT**, **ÖFFNUNG_LÄUFT** und **SPEICHERFEHLER** müssen unterscheidbar sein. Konkrete interne State-Namen sind nicht vorgeschrieben.

Eine erneute Initialisierung der Event Page ist nicht automatisch ein neuer Firefox-Lauf. Browserstart, Add-on-Update, Extension-Prozessfehler und normales Aufwachen verlangen unterschiedliche Behandlung. Geht ein flüchtiger Marker verloren, beginnt ein konservativer Wiederabgleich; er rotiert nicht allein deshalb den letzten geschützten Stand weg. Listener starten vor asynchroner Datenladung; währenddessen eintreffende relevante Änderungen werden geordnet berücksichtigt. Kein unbegrenzt wachsender RAM-Eventlog. [M02, M07]

In den geprüften `runtime`-/`sessions`-Dokumentationen ist kein allgemein belastbares Signal belegt, das für unseren gesamten Anwendungsfall „die letzte Sitzung wurde vollständig und korrekt wiederhergestellt“ garantiert. `runtime.onStartup`, eine erfüllte Promise, `status: complete`, gleiche Tab-Anzahlen oder einige Sekunden Ruhe werden deshalb **nicht** so interpretiert. Das ist eine konservative Designableitung, keine Behauptung, der gesamte Firefox-Quellcode sei untersucht worden. [M11, M12]

Abgleich liest beim Start den notwendigen Gesamtkontext; spätere Abfragen betreffen grundsätzlich nur betroffene Fenster/Tabs. Nur eindeutig wiedergefundene erwartete logische Elemente mit plausibler Zuordnung und verarbeiteter Ereignisfolge dürfen als vorhanden gelten. Zusätzliche Live-Tabs werden separat gesichert. Fehlende, doppelte oder zeitweilig nicht lesbare Elemente halten den zugehörigen Schutz aufrecht.

Bereits bekannte URLs/Strukturinformationen werden nicht durch eine kurz sichtbare leere, fehlende oder verdächtige Restore-Beobachtung vernichtet. Fehlende Eigenschaften sind nicht dasselbe wie `false` oder „keine Gruppe“. Auch nach scheinbar vollständigem Abgleich bleibt ein vorheriger Checkpoint im regulären Rettungspfad erhalten. Die präzise Protokollimplementierung und Race-Tests sind Pflicht des Agenten, kein Anlass für zeitbasierte Löschheuristiken.

### 6.2 Normalbetrieb und Schließen

Tab-Neuanlage, Navigation, relevante Zustände, Einzelschließung, Gruppierung und Transfer werden ereignisorientiert erfasst. `tabs.onRemoved` liefert `isWindowClosing`; das ist eine Schließursachenhilfe, aber kein Beweis dafür, dass ein Mensch auf das X geklickt hat. Fenster-/letzten-Tab-Schließungen werden gegen den zuletzt gespeicherten nichtleeren Fensterstand abgeglichen. [M13]

Bei einem Tabtransfer bleibt dessen Inhalt während der abgelösten Zwischenphase erhalten. Quelle und Ziel werden gemeinsam konsistent fortgeschrieben, sobald eine belastbare Zuordnung vorliegt. Nicht passende/fehlende Gegenereignisse gehen in einen ungeklärten Übergang, nicht in einen Löschpfad. Native Gruppen-/Splitbewegungen dürfen nicht zu doppelt ausgeführten eigenen Verschiebungen führen.

**Letzte Sitzung gegenüber geschlossenen Fenstern:** Der Browser liefert nicht aus jedem Fensterschließen eine eindeutige Absicht „Browser wird gleich ganz beendet“. Darum müssen laufender Fenstersatz, der Stand vor zusammenhängendem Schließen und zusätzlich kürzlich geschlossene Fenster getrennt rekonstruierbar bleiben. Bei mehreren nacheinander geschlossenen Fenstern darf die verfügbare Recovery-Quelle nicht mit jedem `onRemoved` zusammenschrumpfen. Eine rein aus Schließzeiten abgeleitete Vermutung darf frühere enthaltene Fenster nicht vernichten. Mehrdeutige Kandidaten erscheinen als solche; „alle fehlenden“ bezieht sich auf einen erkennbaren ausgewählten Recovery-Stand, nicht blind auf die gesamte 50-Fenster-Historie. Die Auswahl-/Retentionslogik ist ein expliziter Review- und Testschwerpunkt.

### 6.3 Manuelles Öffnen ist ein nachvollziehbarer Auftrag

Ein Nutzerklick bezieht sich auf eine bestimmte gespeicherte Revision. Vor externen Browserwirkungen wird ein begrenzter Restoreauftrag identifizierbar gemacht. Wiederholte Klicks auf denselben logischen Gegenstand werden serialisiert. Vor jedem Öffnungsschritt wird auf bereits vorhandene eindeutige Bindungen und zwischenzeitliche native Wiederherstellung geprüft.

Ein Absturz zwischen Browser-Neuanlage und deren lokaler Bestätigung lässt sich nicht durch eine browser-/datenbankübergreifende Transaktion ausschließen. Deshalb **kein blindes automatisches Wiederholen** eines ungewissen Öffnungsschritts nach Neustart. Vorhandene Objekte abgleichen; verbleibende Mehrdeutigkeit anzeigen und Nutzerfortsetzung verlangen. Auch wenn Firefox sehr spät nach einer manuellen Öffnung denselben Stand zurückbringt, gilt Konfliktbehandlung statt automatischem Schließen vermeintlicher Duplikate. Ein absolutes „Firefox kann nie selbst ein Duplikat erzeugen“ wäre ein unzulässiges Versprechen.

Neue Recovery-Fenster werden kontrolliert erzeugt. Hintergrund-Tabs werden nach Möglichkeit gleich `discarded` angelegt; `windows.create({url: alleURLs})` ist nicht die ungeprüfte Massenlade-Strategie. Die aktive Seite je neuem Fenster darf normal laden. Parallelität und UI-Arbeitsportionen bleiben begrenzt und messbar. Bereits von Firefox wiederhergestellte Fenster werden nicht prophylaktisch neu navigiert, sortiert, entladen oder umgruppiert. [M14, M15]

Teilresultate bleiben mit betroffenen Einträgen und ursprünglichem Quellstand nachvollziehbar. Ein zurückgewiesener URL-Aufruf oder fehlender Container darf die restlichen erfolgreich erfassten Daten nicht beschädigen.

## 7. Firefox-Fähigkeiten und Berechtigungen [WS-TF-PLATFORM]

Die folgende Matrix ist eine Vorbereitungsrichtung, **keine bereits erfolgreich geprüfte Firefox-Kompatibilitätsmatrix**. Ein fehlender API-Nachweis wird nicht durch eine ähnliche Firefox-Oberflächenfunktion ersetzt.

| Bereich | Technische Richtung | Erforderlicher Nachweis / sicherer Grenzfall |
|---|---|---|
| URLs, Reihenfolge, aktiv, angeheftet, stumm | Dokumentierte Tab-APIs und relevante Änderungsereignisse. | Mehrfach gleiche URLs, sehr lange URLs, leere Übergangswerte, letzte-Tab-Schließung und gleichzeitig eintreffende Navigation prüfen. Titel nie als HTML ausführen. |
| Container | Vorhandene `cookieStoreId` zusammen mit Instanzzuordnung; Namen/Farben nur als Orientierung. | ID aus anderem Profil, gelöschter/neuer Container und deaktivierte Containerfunktion dürfen keine stille Zuordnung zur Standardumgebung auslösen. [M08, M14] |
| Native Gruppen | Eigene logische Identität; Firefox-Gruppe mit Mitgliedschaft und Metadaten rekonstruieren. | `tabs.group()` kann angeheftete Tabs entpinnen. Unvereinbare importierte Zustände nicht durch beliebige Aufrufreihenfolge „reparieren“. Gruppenkontiguität, Collapse/aktiver Tab und Gruppenbewegung testen. [M16] |
| Split View | Auslesbare Beziehung als Metadatum; normale Zwei-Tab-Wiederherstellung mit Hinweis als erlaubter Fallback. | Die gelesene Mozilla-Dokumentation belegt Zuordnungsbeobachtung, aber noch keinen hier verifizierten stabilen Vertrag zur nativen Neuerzeugung. API-Existenz und reale Kombinationen vor Nutzung prüfen. [M17] |
| Lesemodus / entladen | Reader-Absicht speichern; Hintergrundtab möglichst direkt entladen erzeugen. | Kombinationen mit aktiv, pinned, muted, Container und Gruppe tatsächlich prüfen. Kein pauschaler Fallback auf Laden aller Seiten, kein erzwungenes Abspielen von Audio. [M14] |
| Fensteranordnung | Dokumentierte Geometrie- und Zustandswerte, Änderungsereignisse soweit verfügbar. | Bounds-Event nur nach Capability-Prüfung. Bei fehlendem Ereignis gezielte ohnehin nötige Abfragen statt Geometrie-Polling. Ohne zuverlässig geprüfte Bildschirmgrenzen Firefox/OS eine sichere Standardposition wählen lassen. [M15, M18] |
| Verborgene Tabs / andere Add-ons | Unsichtbarkeit nicht mit Abwesenheit oder Privatheit verwechseln. | Vorhandene reguläre Tabs sichern; fremde Gruppen-/Hide-Logik nicht rekonstruieren oder ferngesteuert ändern. Verlust fremder Darstellungseigenschaften ehrlich abgrenzen. |
| Sonderfenster | Normale nichtprivate Browserfenster sind Ziel. | Die gelesene Window-Dokumentation belegt keinen für alle Fälle geeigneten `isWebApp`-Schalter. Web-App-/Popup-/DevTools-/PiP-Verhalten auf der Zielversion prüfen; ungeklärte Sonderfälle nicht als native Vollwiederherstellung ausgeben. [M18] |
| Interne / lokale Adressen | Erfasste Originaladresse als Daten erhalten; nur nach Nutzeraktion und validiertem Öffnungspfad verwenden. | Zunächst HTTP/HTTPS und ausdrücklich unterstützte neue/leere Tabs. Andere Protokolle nicht blind öffnen; keine `javascript:`-, `data:`-, externen Protokollhandler- oder privilegierten Ausführungswege. Nicht automatisch öffnungsfähige Einträge bleiben sichtbar erhalten. [M14] |

**Berechtigungsrichtung:** `tabs`, `storage`, `sessions`, `alarms`, `downloads`, `tabGroups` und das bereits akzeptierte `cookies`; zusätzlich nach T04 `contextualIdentities` und `unlimitedStorage`. Es wird keine zusätzliche nicht existierende `windows`-Berechtigung vorausgesetzt. Keine allgemeinen Host-Berechtigungen, kein `scripting`, keine `webRequest`-/`history`-/`browsingData`-/`nativeMessaging`-Berechtigung für diese Architektur. Nicht benötigte Berechtigungen werden vor Packaging entfernt, nicht vorsorglich verlangt. [M04]

`contextualIdentities` erschließt mehr Funktionen als WindowSafe benutzen soll. Die implementierte Nutzung bleibt auf Lesen vorhandener Container und deren Zuordnung beschränkt. Insbesondere keine Container-Erstellung/-Umbenennung/-Löschung und keine Cookie-Inhalts-API-Aufrufe. Die von Mozilla beschriebene mögliche Aktivierung der Containerfunktion durch eine Erweiterung ist in T04 sichtbar als Nebenwirkung zur Zustimmung gestellt. [M08]

Privatmodus wird zusätzlich mit der Manifestgrenze `incognito: not_allowed` ausgeschlossen; die Erfassung prüft trotzdem den konkreten Kontext vor jeder Übernahme. Importierte Privatmarker werden nicht entfernt, um die Daten anschließend doch als normale Tabs einzuspielen. Fehlende/inkompatible Herkunftsangaben werden konservativ behandelt. Beliebigen fremden URLs lässt sich allerdings nicht ansehen, ob sie irgendwann in einem privaten Fenster verwendet wurden; zugesagt ist keine erfundene historische Privatheitserkennung. [M25]

Eine zufällige lokale WindowSafe-Instanzkennung trennt Daten und Downloadnamen. Sie ist weder ein Firefox-Profilpfad noch ein globales Benutzerkonto. Ein Backup aus einem anderen Profil wird nicht allein wegen gleicher numerischer Container- oder Tab-IDs an Live-Objekte gebunden. Auch kopierte Profile/Installationskennungen verlangen bei erkannten Kollisionen einen neuen, expliziten Abgleich. Kein Zugang zu anderen Firefox-Profilen wird vorausgesetzt.

### 7.1 Vorgelagerte Plattform-/Erkennungsqualifikation [WS-TF-PREIMPLEMENTATION-PLATFORM]

**Harter Halt vor Beginn oder Freigabe der betroffenen Produktimplementierung.** Die Klärungstrigger aus Product WS-RESTORE und WS-OL-01/03 werden nicht auf Feature-Acceptance verschoben. Insbesondere darf die produktive Erfassungslogik nicht implementiert werden, solange die sichere Erkennung und Behandlung normaler versus Web-App-/Popup-/DevTools-/Picture-in-Picture-Fenster für die unterstützte Umgebung ungeklärt ist.

Vor dem jeweiligen Implementierungsstart muss ein exakt referenzierter Qualifikationsstand für die betroffenen Plattformfragen vorliegen: Zielversion/-umgebung, benötigte API beziehungsweise Erkennungsmöglichkeit, tragfähige Evidenz, dokumentierte unterstützte Grenze und sichere Behandlung nicht unterstützter Fälle. Dies umfasst entsprechend WS-OL-01/03 die API-Kombinationen, Restore-Erkennungsgrenzen, Sonderfenster, fremd verborgene Tabs und instanzübergreifende Containerzuordnung. Fehlende sichere Nachweise bleiben offen und sperren die betroffene Arbeit; ein Zeitpunkt, eine bloße UI-Funktion oder die Aussicht auf spätere Tests sind kein Ersatz.

Eindeutige Primärdokumentation darf belastbare Teilfragen klären; unsichere Plattformkombinationen benötigen vor ihrer darauf aufbauenden Produktimplementierung eine gesondert autorisierte isolierte Qualifikation. Kleine Qualifikationsproben gegen künstliche Profile sind von der normalen WindowSafe-Produktimplementierung zu trennen und benötigen ihren eigenen zulässigen Test-Envelope. Dieses Dokument startet keine solche Probe. Materielle Funktions-/Plattformabstriche verlangen Nutzerentscheidung und erforderliches Product-/Preparation-Rebinding; der Agent darf sie nicht selbst als technischen Fallback genehmigen, soweit Product Truth diesen nicht schon erlaubt.

Ein separat freigegebener **Foundation-Bootstrap ohne Produktfeatures** darf Entwicklungsrahmen, Nachweiskontexte und diese Stop-Gates materialisieren; er ist keine Ausnahme, um bereits die Erfassung oder andere Produktfunktionen unter einem anderen Namen zu bauen. Sobald die nötige Vorabklärung dokumentiert und gebunden ist und die weiteren Ausführungsgates erfüllt sind, kann die betreffende Produktimplementierung starten.

**Nachgelagert und zusätzlich:** Vollständige native Integrations-, Fehlerfall- und Regressionstests der tatsächlich implementierten Funktionen sind spätestens vor Feature-Acceptance zu erbringen. Vorabklärung und nachgelagerte Abnahme sind zwei verschiedene Pflichtnachweise. Beide werden im Binding und späteren Handoff getrennt ausgewiesen.

## 8. Backup, Import und Fehlergrenzen [WS-TF-BACKUP]

### 8.1 Tagesbackup und Lebenszyklus

Das Fälligkeitskriterium ist **lokaler Kalendertag plus geänderte wiederherstellungsrelevante Revision**, nicht nur „24 Stunden vergangen“. Ein bereits erfolgreich gesicherter identischer Stand braucht keine weitere Datei. Nach Browserstart sowie bei relevanter Aktivität wird Fälligkeit geprüft; ein Alarm kann den nächsten Tageswechsel abdecken. Firefox-Alarme müssen nach Browserneustart erneut eingerichtet werden. Es gibt keine minütliche Sitzungsvollabfrage. Uhr-/Zeitzonenwechsel, Schlafmodus und längere Nichtbenutzung sind Testfälle. [M20]

Export bezieht sich auf einen konsistenten, unveränderlichen Datenstand. Seine benötigten Revisionen bleiben bis zum Ende des Versuchs geschützt, während neue Live-Änderungen weiter gespeichert werden. Eine Datenbanktransaktion wird nicht während asynchroner Downloads offen gehalten. Die genaue Streaming-/Chunking-Implementierung bleibt agent-owned.

**Richtung:** versioniertes JSON, für tägliche Dateien bevorzugt native Gzip-Kompression über `CompressionStream`, ohne zusätzliche Kompressionsbibliothek. Unkomprimiertes JSON bleibt ein transparenter technischer Fallback. Der gesamte Export darf nicht mehrfach als große Zeichenkette und Bytekopie im RAM liegen. Wird die Event Page mitten im Export beendet, bleibt der Versuch rekonstruierbar; nicht bestätigte Dateien gelten nicht als erfolgreich. Kompression ist weder Verschlüsselung noch ein Beweis niedrigen RAM-Verbrauchs. [M21]

### 8.2 Erfolg und sichere Aufbewahrung

Ein erfolgreich zurückgegebener Download-Identifier ist noch kein abgeschlossener Dateibackup. Die Abschlussmeldung beziehungsweise ein verifizierter vollständiger Downloadzustand muss vor dem Erfolgseintrag vorliegen. Dateinamen verwenden einen relativen WindowSafe-Unterordner, Instanzkennung, Datum und kollisionssichere Versuchskomponente. Kein unkontrolliertes Überschreiben gleichnamiger Dateien. [M19]

Nach Neustart werden bekannte unvollständige Versuche über ihre verwaltbaren Downloadinformationen abgeglichen. Abgeschlossen, unterbrochen, noch laufend und nicht mehr verifizierbar bleiben verschieden. Eine verlorene Abschlussmeldung erzeugt nicht automatisch eine Serie weiterer Dateien. Erneute Versuche sind begrenzt, mit Abstand und sichtbarem Fehlerstatus.

Aufbewahrung richtet sich nach den **14 erfolgreichen Tagesbackups** aus Product Truth. Bereinigung erfolgt erst nach einem neuen bestätigten Erfolg und nur bei eindeutig eigener Datei: verwalteter Versuch, bekannte Download-ID und passende Zuordnung. Bei verlorener Downloadhistorie, veränderter Zuordnung oder extern verschobenen Dateien nicht erraten, was gelöscht werden darf. Keine freie Dateisystemsuche, keine fremden Downloads löschen. Das bloße Entfernen aus der Downloadhistorie ist keine Dateilöschung. [M19]

Downloadpfad-Einstellungen und etwaige Browserdialoge werden vor automatischer Nutzung im Testprofil geprüft. WindowSafe verstellt nicht global den Firefox-Downloadordner. Externe Cloud-Synchronisierung eines vom Nutzer gewählten Downloadverzeichnisses lässt sich nicht pauschal verhindern; das Add-on selbst überträgt keine Backupdaten an einen Dienst.

### 8.3 Import als eigener, nicht destruktiver Datenbestand

Formatversion, Struktur, Typen, eindeutige Identitäten, Referenzen und erlaubte Werte werden vor verbindlicher Übernahme geprüft. Komprimierte Dateien verlangen zusätzlich Grenzen gegen unkontrolliertes Entpacken. Größen-/Anzahl-/Tiefe-Limits müssen zum gebundenen Belastungsumfang passen und sichtbar dokumentiert werden; kein stilles Abschneiden langer URLs, Titel oder großer gültiger Sicherungen, nur um Messziele einzuhalten.

Unvertrauenswürdige Daten werden nicht als HTML, Code, Dateipfad oder privilegierter Aufruf interpretiert. Keine automatische Freigabe eines fremden Protokolls, keine Prototyp-Manipulation über ungeprüfte Schlüssel, keine Namensgleichheit als Merge-Befehl. Bei Fehlern bleiben vorhandene Roots unverändert; unvollständige Importstaging-Daten sind kein angebotener vollständiger Recovery-Stand.

Ein gültiger Import wird zunächst eine zusätzliche Recovery-Quelle mit eigener Herkunft. Öffnen, Zuordnen eines Containers oder Ersetzen eines benannten Eintrags sind getrennte Nutzeraktionen. Wiederholte Importe dürfen nicht versehentlich laufende Live-Bindungen übernehmen. Auch der Export aus dieser Quelle muss ihre unterstützten Informationen ohne stillen Verlust erhalten.

## 9. Freigegebene Ressourcen- und Last-CPU-Ziele T02 + T05-R2 [WS-TF-PERF]

**Die Zielwerte aus §9.1 sind unverändert mit T02 freigegeben; das Last-CPU-Kriterium in §9.3 ist mit T05-R2 freigegeben. §9.2 bleibt eine separat gekennzeichnete synthetische Größenprobe und ist kein Nachweis einer bereits existierenden Erweiterung.** 1 KiB = 1.024 Byte, 1 MiB = 1.048.576 Byte. Zusätzlicher Browserprozess-Speicher, JS-/DOM-Speicher, logische Datensatzgröße und Dateien auf Festplatte dürfen nicht miteinander verwechselt werden.

### 9.1 Gebundene Lastprofile

- **R500:** 500 Tabs in 10 Fenstern, mittlere URL-Länge 160 UTF-8-Byte und Titel-Länge 80 ASCII-Zeichen; realistische Mischung aus aktiven/angehefteten/stummen Tabs, mehreren Containern und zusammenhängenden Gruppen.
- **R2000:** 2.000 Tabs in 20 Fenstern, gleiche Metadatenverteilung. Stressnachweis, kein Produktlimit.
- **H:** zusätzlich 14 verschiedene abgeschlossene Sitzungscheckpoints mit jeweils Änderungen an 5 % der Tab-Datensätze und 50 geschlossene Fensterstände mit je 50 Tabs bei R500 bzw. 100 bei R2000. Gemeinsame unveränderte Inhalte dürfen geteilt werden. Keine künstliche Beschränkung auf gleichlautende URLs zur Verbesserung der Kompression.

Separate adversarielle Fälle enthalten lange/unicodehaltige URLs, viele identische URLs mit verschiedenen Identitäten, weit mehr ungeklärte Stände und große Importe. Sie müssen datenerhaltend behandelt werden, fallen aber nicht unter dieselbe feste Dateigrößenprognose.

| Messgröße | R500 – freigegebenes Startziel | R2000 – freigegebenes Stressziel |
|---|---|---|
| Attributierbarer lebender Add-on-JS-/DOM-/Cache-Speicher, Oberfläche geschlossen, nach Beruhigung | höchstens **8 MiB** | höchstens **24 MiB** |
| Aktuell notwendige logische Nutzdaten als kompaktes UTF-8-JSON, ohne Historie | höchstens **1 MiB** | höchstens **4 MiB** |
| Gesamte wiederherstellungsrelevante logische Daten einschließlich H | höchstens **8 MiB** | höchstens **32 MiB** |
| Vollständiger unkomprimierter Referenzexport einschließlich H | höchstens **8 MiB** | höchstens **32 MiB** |
| Zusätzlicher Export-/Import-Spitzenspeicher oberhalb des ruhenden Add-on-Werts | höchstens **8 MiB** | höchstens **16 MiB** |
| Normale Sicherungsverzögerung: Eingang eines relevanten Ereignisses bis erfolgreicher Persistenz | p95 höchstens **1 s**, Maximum **2 s** | p95 höchstens **2 s**, Maximum **3 s** |
| Metadaten-Burst: 300 relevante Ereignisse über 3 Sekunden | spätestens **2 s** nach letztem Ereignis gesichert; keine Änderung länger als **5 s** nur ungesichert halten | spätestens **3 s** nach letztem Ereignis; höchstens **6 s** älteste ungesicherte Änderung |
| Durch WindowSafe verursachte CPU im ruhigen 10-Minuten-Intervall | durchschnittlich höchstens **0,1 % eines CPU-Kerns** | gleiches Ziel |
| Fensterliste bis sichtbar/bedienbar, ohne sämtliche alten Tab-Details zu laden | p95 höchstens **250 ms** | p95 höchstens **500 ms** |

Diese Größen sind keine Garantie, dass der **gesamte Firefox-Prozess** um höchstens 8 MiB wächst. Zum Nachweis gehören zusätzlich gepaarte Messungen mit/ohne Add-on für Prozess-RAM, CPU und tatsächliches Datenbank-Dateiwachstum. Nicht sauber attributierbarer nativer Speicher wird separat ausgewiesen und darf nicht als null ausgegeben werden. Hoher ungeklärter Mehrverbrauch verhindert einen pauschalen Ressourcenschonungs-PASS trotz kleiner JSON-Datei. Die exakte reproduzierbare Messmethode und das Testsystem sind vor Freigabe der betroffenen Produktimplementierung zu binden; die tatsächlichen Implementierungsmessungen erfolgen später, spätestens vor Feature-Acceptance. Diese Vorabbindung darf nicht auf das erst nach Implementierung ausgeführte Performance-Gate verschoben werden.

**Zusätzliche mechanische Grenzen:** Im gewöhnlichen Leerlauf keine periodischen Vollscans, keine sinnlosen Speicherwrites und keine wiederkehrende Add-on-Arbeit außer fälliger Sicherungs-/Fehlerbehandlung. Relevante Ereignisse sollen vor kostspieliger Bearbeitung gefiltert werden. Debouncing braucht eine maximale Wartezeit; endloser Eventfluss darf Persistenz nicht endlos hinausschieben. Eine normale Änderung schreibt nicht ganze unbetroffene Sitzungen und Historien neu. Gemessen werden logische geschriebene Bytes, betroffene Records und reale I/O-Wirkung getrennt; keine erfundene Gleichsetzung logischer Payload mit SSD-Schreibvolumen.

Die Verzögerungsziele gelten bei laufendem, reagierendem Browser und verfügbarem Datenträger in der gebundenen Testumgebung. OS-Pausen, Suspend und echte I/O-Fehler sind gesondert auszuweisen; sie sind keine Grundlage, innerhalb des Normaltests schlechte Messwerte nachträglich auszuschließen. Ein Fehlerstatus ersetzt keinen gespeicherten Stand. Bei vielen Tabs dürfen Ressourcenlimits nicht durch stilles Weglassen von Tabs eingehalten werden.

### 9.2 Tatsächlich durchgeführte Größenprobe – eng begrenzte Aussage

Ein eigenständiges Python-Analyseskript erzeugt ausschließlich synthetische Metadaten. Es ist **kein WindowSafe-Code**, kein genehmigtes Datenmodell und kein Firefox-Test. Für einen aktuellen Stand ohne Historie wurden gemessen:

| Synthetischer Umfang | Kompaktes JSON | Python-Gzip, Stufe 6 |
|---|---:|---:|
| 500 Tabs / 10 Fenster | 238.646 Byte, ca. **233,1 KiB** | 55.286 Byte, ca. 54,0 KiB |
| 2.000 Tabs / 20 Fenster | 949.180 Byte, ca. **926,9 KiB** | 223.646 Byte, ca. 218,4 KiB |

Der Befund stützt nur, dass Metadaten dieses angenommenen Umfangs nicht von sich aus mehrere Megabyte pro aktuellem Stand erfordern. Er misst **nicht** RAM, IndexedDB-Overhead, gesamte Historie, reale Firefox-CPU oder die Kompression des späteren Add-ons. Skript und Ergebnis sind separat beigefügt; Wiederholung muss dieselben synthetischen JSON-Prüfsummen liefern.

### 9.3 Last-CPU-Kriterium T05-R2 – freigegeben [WS-TF-LOAD-CPU]

F01 beanstandet, dass Idle-CPU und Persistenzlatenz kein Last-CPU-Bestehenskriterium ersetzen. Der Nutzer hat nach Vorlage einer zunächst strengeren, nicht freigegebenen 1-%/2-%-Fassung ausdrücklich darauf hingewiesen, dass unrealistische Vorabziele unnötige Architekturumbauten provozieren könnten. Die daraufhin vorgeschlagene **T05-R2**-Fassung wurde im unmittelbaren Entscheidungskontext mit „ok“ freigegeben. Der exakte Entscheidungsgegenstand ist `WindowSafe_Last_CPU_Decision_WS-T05-R2-20260917-01.md@sha256:8d2b565beb28ca47e63df59b5d7d9236dd99c6f1967dba1190553c0a66b5800c`.

**Harte Dauerlastgrenzen:**

| Kriterium | R500 | R2000 |
|---|---:|---:|
| L10: 600 s, 10 tatsächlich verarbeitete relevante Zustandsänderungen/s | Median der gültigen A/B-Paare **≤ 10 % eines CPU-Kerns** | Median **≤ 20 %** |
| Zusätzliche Einzellaufgrenze | kein gültiger Lauf **> 15 %** | kein gültiger Lauf **> 30 %** |
| B300: 300 relevante Ereignisse/3 s, festes 10-s-Fenster inkl. Nachlauf | **≤ 20 %** im Mittel | **≤ 40 %** im Mittel |

**Soft-Optimierungsziele:** R500 möglichst ≤ 5 %, R2000 möglichst ≤ 10 %. Das Nichterreichen eines Soft-Ziels allein ist **kein Acceptance-Fehler, kein blockierendes Finding und kein Auftrag zum Architektur-Redesign**. Kleine reversible Optimierungen bleiben zulässig, wenn sie Recovery, Latenz, Safety und Wartbarkeit nicht verschlechtern.

Mindestens fünf gültige gepaarte Messläufe je Lastprofil und Betriebssystem vergleichen eine identische synthetische Testlast ohne und mit WindowSafe über den relevanten Firefox-Prozessbaum. Messwerkzeug, Browser-/OS-Build, Hardware, Profilzustand, Hintergrundlast, Warm-up, Messintervall und bekannte Messunsicherheit werden **vor Beginn der betroffenen Produktimplementierung** gebunden. Die tatsächlichen Last-CPU-Ergebnisse entstehen später und sind spätestens vor Feature-Acceptance nachzuweisen.

Alle T02-Grenzen gelten gleichzeitig. Ein CPU-PASS durch verlorene, nicht ausgelieferte oder absichtlich über die zulässige Sicherungsverzögerung hinaus verschobene Änderungen ist ungültig. Harte T05-R2-Überschreitung verlangt Optimierung oder eine sichtbare neue materielle Entscheidung; Soft-Zielverfehlung allein nicht.

## 10. Risiko, Verifikation und Evidence [WS-TF-VERIFY]

### 10.1 Reviewpflicht und Prüftiefe

**Elevated Risk** ist mindestens anzusetzen: private Browsermetadaten, konkurrierende Ereignisse, Zustandskonsistenz, destruktive Bereinigung und Recovery unter Abbruch. Die geringe Größe eines Add-ons macht diese Pfade nicht zu einem unbesehenen LOW_RISK-Projekt. Nach Foundation 1 ist ein **unabhängiger Technical Foundation Preparation Review erforderlich**. Eigenprüfung durch den vorbereitenden LLM ersetzt ihn nicht. [F1]

Besonders zu prüfen sind Start-/Schließübergänge, Veröffentlichung neuer Datenwurzeln, Garbage Collection, Backupbereinigung, Import, Containerzuordnung und Browseroperationen mit nicht atomarer Bestätigung. Kritische Safety-Gates dürfen später nicht nur abgeschwächt werden, um CI grün zu bekommen.

### 10.2 Nachweisfamilien mit Produktankern

**Reihenfolge der Nachweise:** Die in §7.1 genannten Plattform-/Erkennungsfragen und die konkrete Ressourcen-Messmethode gemäß §§9.1/9.3 sind vor Beginn der betroffenen Produktimplementierung zu klären und zu binden. Die folgende Tabelle benennt zusätzliche Integrations-/Regressions-/Acceptance-Evidence der späteren Implementierung. Sie verschiebt keine dieser vorgelagerten Pflichten auf die Abnahme.

| Produktakzeptanz | Erforderliche Evidenzrichtung |
|---|---|
| WS-AC-01 | Speichern/Benennen/Umbenennen/Löschen, schneller Mehrfachklick, bereits verbundenes Fenster, keine unerwünschte Browserfensterschließung. |
| WS-AC-02 | Ereignisfolgen für Navigation, neue Tabs, Einzelschließung, Transfer, Gruppen-/Splitänderungen; Quelle/Ziel nach Unterbrechung konsistent. |
| WS-AC-03–05 | Echter nativer Restore vollständig/teilweise/verzögert; unmittelbare Benutzeränderungen; fehlende Tags, wiederverwendete Browser-IDs; mehrere aufeinanderfolgende fehlerhafte Neustarts; alte geschützte Inhalte bleiben erhalten. |
| WS-AC-06 | Ein Fenster/letzter Tab, mehrere nacheinander, Gesamtquit, Abbruch vor/nach DB-Commit und Session-Tag; Event-Page-Suspend/Restart und Erweiterungsupdate. |
| WS-AC-07 | Gleiche URLs mit unterschiedlichen Identitäten, doppelte Sessionmarker, Duplikate nach spätem Firefox-Restore, verlorene Bestätigung nach Browser-Neuanlage. |
| WS-AC-08 | Native Kombinationen aus Gruppen, Pin, Container, Reader, discarded, mute und Split; Sonderfenster-/Geometriegrenzen, nicht öffnungsfähige URL und sichtbare Teilresultate. |
| WS-AC-09 | Private-Fenster-Ausschluss in Datenbank/Tags/Logs/Export; kein Cookie-Inhaltszugriff; Profile und fremde Import-IDs getrennt; Manifest- und Berechtigungsprüfung. |
| WS-AC-10 | Tageswechsel, Neustart, Schlafmodus, kein Firefoxbetrieb, Download-ID ohne Abschluss, Abbruch, verlorene Downloadhistorie, nur eigene Bereinigung; beschädigter/zu großer/inkompatibler Import. |
| WS-AC-11 | Reproduzierbare R500/R2000/H-Messungen, UI-Latenz, Dauerlast, Exportspitzen, I/O, langsamer Datenträger; zusätzlich die T05-R2-L10-/B300-CPU-Bestehensnachweise. Messmethode/Testsystem vor betroffener Implementierung binden. Kein unkontrolliertes gleichzeitiges Laden von Hintergrundseiten. |

Deterministische Unit-/Modelltests untersuchen Zustandsübergänge, Ereignispermutationen und Failpoints. Sie ersetzen keine Integration mit den echten Firefox-APIs. Belegbar unterschiedliche Evidenzklassen bleiben getrennt: Modelltest, gemessener lokaler Test, CI-Verifikation und nativer Laufzeittest. Ein Dokument oder ein erfolgreicher Typecheck beweist keinen gelungenen Browser-Restore.

**Wichtige Installationsgrenze:** Temporär geladene Erweiterungen werden bei Browserbeendigung entfernt. Ein reiner `web-ext run`-/`about:debugging`-Temporärtest genügt daher nicht als Beweis der Neustartfunktionen. Der Restart-Test benötigt eine stabile Add-on-ID und einen geeigneten dauerhaft installierten Teststand in einem eigens erzeugten Wegwerfprofil. Zulässige Testbuilds und Installationsweg werden vor Ausführung autorisiert. Keine Signaturabschaltung im tatsächlich genutzten Profil; eine eventuelle Signierung/Übertragung an Mozilla ist ein gesonderter Auslieferungs-/Datenweg, nicht durch dieses Dokument genehmigt. [M23, M24]

Laufzeittests benutzen synthetische lokale Testseiten und künstliche Profile, nicht echte Chronik, offene Arbeitsfenster, Konten oder Sitzungsexporte des Nutzers. Die Performance-Evidence dokumentiert Hardware, OS-/Firefox-Build, Profilzustand, Hintergrundlast, Messwerkzeug, mindestens fünf vergleichbare Durchläufe sowie Median/p95/Maximum und Messgrenzen. GC-/Leerlaufannahmen sind offen zu nennen; eine für Messzwecke erzwungene Bereinigung darf nicht als automatisch erreichtes Alltagsverhalten ausgegeben werden.

CI soll reproduzierbare Build-/Lint-/Typ-/Modelltests, Format-/Referenzkonsistenz und relevante mechanische Safety-Gates tragen. Native GUI-/Restart-/Performance-Nachweise sind nur dann CI-verifiziert, wenn sie dort tatsächlich ausgeführt wurden. Ansonsten bleibt der genaue lokale Nachweis sichtbar; kein erfundenes `CI_PASS` für manuelle Beobachtung.

## 11. Epic-Richtung und Agentengrenze [WS-TF-EPICS]

Die Produktgröße rechtfertigt vorläufig **einen zusammenhängenden V1-Epic „zuverlässige lokale Fenster-/Sitzungssicherung und manuelle Wiederherstellung“**. Das ist eine High-Level-Richtung, noch kein gebundener Epic Subject und keine Erlaubnis zu seiner Ausführung. Ein großer Block wird nicht künstlich in Mikro-Epics zerlegt, nur um mehr externe LLM-Schritte zu erzeugen.

Als unabhängig prüfbare Feature-Richtungen kommen konsistente Erfassung/Recovery-Datenhaltung, benannte Fenster und manuelles kontexttreues Wiederherstellen sowie Dateibackup/Import infrage. Schutz- und Ressourcenregeln durchziehen diese Fähigkeiten. Feature-Schnitt und Reihenfolge werden nach angenommener Project Foundation in der eigentlichen Epic Preparation präzisiert; Implementierungsdetails und Tasks bleiben beim Agenten.

Der erste Coding-Agent-Lauf erzeugt nach gesonderter Freigabe zunächst nur die **Project Foundation**: nötige Produkt-/Architektur-/Review-/Evidence-Kontexte, reproduzierbare Entwicklungsbasis und angemessene Guards. Kein normales Produktfeature vor dem Foundation-Gate. Anschließend gelten unabhängiger Project Foundation Review, erforderliche externe Kontext-Synchronisierung oder begründetes NOT_APPLICABLE, unabhängige Epic Preparation und spätere Feature-Acceptance-Gates. `MERGED_TO_MAIN`, `FEATURE_ACCEPTED` und `PRODUCTION_RELEASED` bleiben unterschiedliche Zustände. [F1]

## 12. Korrekturrücklauf, Eigenprüfung und nächste Gates [WS-TF-STATUS]

Das unabhängige Resultat **WS-TFPR-20260917-03** lautet **PASS** und schließt `WS-TFPR-20260917-02-F01`; die beiden historischen Findings aus Resultat 01 waren bereits geschlossen. Dieses PASS bleibt unverändert und wird nicht umgedeutet. Der danach separat festgestellte Residualbefund betrifft ausschließlich die maschinenlesbare Bezeichnung zweier T05-R2-Einzellaufgrenzen im Decision Record; er verändert weder das PASS für den exakt reviewten alten Tuple noch die freigegebene T05-R2-Entscheidung. Für den korrigierten immutable Tuple ist vor `READY_FOR_AGENT` dennoch ein neuer Delta-Rereview erforderlich.

| Status / Punkt | Disposition und spätester Trigger |
|---|---|
| T01–T04 / USER_DECISIONS_PRESERVED | Unverändert nach WS-TD-20260917-01. |
| G01 / REMAIN_PUBLIC | Unverändert öffentlich beibehalten. Kein Git-/Upload-/Merge-/Agentenauftrag. |
| T05-R2 / USER_DECISION_RECORDED | Exakter Last-CPU-Vertrag freigegeben; harte 10-%/20-%-Dauerlastgrenzen mit Einzellaufcaps 15 %/30 %, getrennte Soft-Ziele 5 %/10 %. Soft-Zielverfehlung allein erzwingt keinen Architekturumbau. |
| Historische WS-TFPR-20260917-01-F01/F02 / CLOSED_BY_INDEPENDENT_REREVIEW_02 | Der unabhängige Rereview WS-TFPR-20260917-02 schließt beide ursprünglichen MAJOR-Findings. Diese Schließung wird nicht vom Preparer neu bewertet oder verändert. |
| WS-TFPR-20260917-02-F01 / CLOSED_BY_INDEPENDENT_REREVIEW_03 | Revision 5 wurde unabhängig mit PASS rereviewt; die Schließung bleibt unverändert historische Evidence. |
| Unabhängiger Preparation Review / PASS_03_PRESERVED__FORMAL_DELTA_REREVIEW_REQUIRED | `WS-TFPR-20260917-03` bleibt PASS für r5 + WS-TD-02. Wegen der nachträglichen immutable Decision-Record-Korrektur wird r6 + WS-TD-03 mit neuer Review-ID `WS-TFPR-20260917-04` separat rereviewt. Kein Agentenstart vor diesem neuen PASS und finalem READY-Binding. |
| Plattform-/Erkennung / REQUIRED_BEFORE_AFFECTED_PRODUCT_IMPLEMENTATION | Product WS-RESTORE und WS-OL-01/03: dokumentierte Vorabqualifikation und unterstützte Grenze vor Implementierungsfreigabe. Ungeklärte Fälle sperren betroffene Umsetzung; materielle Einschränkungen brauchen Nutzerentscheidung. Siehe §7.1. |
| Native Integration / REQUIRED_BEFORE_FEATURE_ACCEPTANCE | Vollständige native Tests der implementierten Funktionen ergänzen die Vorabqualifikation. Sie ersetzen diese nicht. Hier keine Browser-/Profiltests durchgeführt. |
| Ressourcen / T02_AND_T05_R2_BOUND__PREIMPLEMENTATION_METHOD_BINDING_REQUIRED | T02 und T05-R2 gelten gemeinsam. Konkrete Messmethode, Trace, Tools und Testumgebung vor betroffener Produktimplementierung binden; eigentliche Resultate spätestens vor Acceptance. |
| Recovery-Protokoll / AGENT_OWNED_WITH_HARD_LIMITS | Details innerhalb unveränderter Invarianten und qualifizierter Plattformgrenzen entwickeln und mit Failpoints verifizieren. Kein zeitbasierter Löschfreibrief. |
| Foundation-Bootstrap / SEPARATE_AUTHORIZATION_REQUIRED | Ein ausdrücklich autorisierter Bootstrap ohne Produktfeatures darf Entwicklungs- und Gate-Rahmen vorbereiten; er umgeht weder offene Entscheidungen noch unabhängige Review-/Ausführungsgates. |
| Toolchain-/Testbuild-/OS-Envelope / OPEN_BEFORE_EXECUTION | Tools, genaue Versionen, zulässige Wegwerfprofil-Installation, aktuelle Repoidentität/-baseline, Schreib-/Merge-/CI-Rechte und Kostenrahmen vor jeweiligem Lauf binden. Historische leere Branchliste ist keine aktuelle Baseline. |
| Signierung, Lizenz, Veröffentlichung / OPEN_LATER | Vor Auslieferung separat entscheiden. Keine Uploads an Mozilla, keine neuen Anbieter, Kosten, Credentials oder produktiven Daten durch diese Korrektur freigegeben. |

**Vorbereitende Eigenprüfung:** Der neue Residualbefund wurde gegen den unveränderten T05-R2-Decision-Subject, `WS-TD-20260917-02`, Revision 5 und das unabhängige PASS 03 abgeglichen. Die einzige Decision-Record-Korrektur ist `MAX_EXCLUSIVE` → `MAX_INCLUSIVE` für die beiden Einzellaufgrenzen; Werte 15/30 und Regeltext bleiben unverändert. Revision 6 aktualisiert ausschließlich diese immutable Referenz und den Lifecycle-/Reviewstatus. Diese Eigenprüfung ist kein neues unabhängiges PASS.

**Gesamtstatus:** `WS-TFPR-20260917-03` bleibt unverändert PASS für den reviewten r5/WS-TD-02-Tuple. `WS-TD-20260917-03` und Revision 6 bilden den formal korrigierten Pre-Agent-Tuple und benötigen noch `WS-TFPR-20260917-04`. `READY_FOR_AGENT = NO`; keine Implementierung, Git-Mutation, Firefox-Ausführung oder CPU-Messung in dieser Runde.

Subject, T05-R2-Entscheidung, Decision-Record-Repräsentation, Rückläufe und Binding sind getrennte, hashgebundene Artefakte. Die formale Korrektur des Decision Records erzeugt deshalb diese neue Subject-Revision und ein neues Binding; historische Product-/Approval-/Entscheidungs-/Reviewdateien werden nicht in-place geändert.

## 13. Quellenregister [WS-TF-REFERENCES]

Recherchegrundlage aus Revision 1, dort gelesen am **17.09.2026**; Revision 2 lud Foundation 1 für den Pre-Agent-Reviewvertrag erneut per exaktem Blob. **In Revision 6 keine neue API-/Release-Recherche, GitHub-Abfrage oder Foundation-Byteverifikation.** Korrekturbasis sind das unveränderte unabhängige PASS 03, der separat gemeldete formale Residualbefund, Product Truth, T05-R2 und die bisherigen gebundenen Entscheidungen sowie der bereits im Gespräch vollständig verfügbare V6-Foundation-1-Vertrag. Die originale Quellenliste bleibt historische Recherchebasis, kein in dieser Runde erneuerter Kompatibilitätsnachweis. T05-R2-Zahlen/Messgestaltung sind eine freigegebene materielle Entscheidung auf Basis einer eigenen Empfehlung; ihre technische Machbarkeit ist noch nicht gemessen. Keine Browserfunktion oder Ressourcenmachbarkeit wird ohne Laufzeitevidence als verifiziert implementiert behauptet.

Formaler Residualrecord: `WindowSafe_Formal_Residual_Correction_WS-FR-20260917-01.json@sha256:14e184e49a3ef79743adb9b9c668c458d7a4ba625e06e876d9b6e2fc5f36f0cf`.

Zusätzliche lokale Referenzen: `results/WS-TFPR-20260917-01.json@sha256:d530dbe024dc662ee7e79a3531df067cc792652f36ce6098bb7821775fb717e7`, `results/WS-TFPR-20260917-02.json@sha256:c9c7ac5443392ed5b618ef0b9f1f292a076a97b83b8095638378ae98b2dca0d5`, `WindowSafe_Last_CPU_Decision_WS-T05-R2-20260917-01.md@sha256:8d2b565beb28ca47e63df59b5d7d9236dd99c6f1967dba1190553c0a66b5800c` sowie der formal korrigierte Decision Record `WindowSafe_Technical_Decisions_WS-TD-20260917-03.json@sha256:36bc4954a4aa9046be381a3095bc3f3574cb6ef2527e7bd060be15eda925f2e3`; der supersedierte Record `WS-TD-20260917-02@sha256:b56978b1458e1e91e225be97bffb687f9d29aa38e1fd31b981d759af5ccef7de` bleibt unverändert historische Evidence.

- **F1:** `felixvonvollmer-png/projektbeschreibung-und-geruest`, `foundations/v6/README.md`; F1-Subject `foundations/v6/candidates/01_grundlage_llm_produktdefinition_technical_foundation_epic_reviews_v6_candidate3_20260906.md`, Blob `3b139a7dfd70da3ae6c83bbdfa703cb98ef94193`, insbesondere §§7–10; F2 nur als eingefrorene Referenz aus dem README, Blob `ff49e56aba09881e9e4a22dc8225949fbc4b54f6`. Kein neuer Pair-Review.
- **G1:** https://api.github.com/repos/felixvonvollmer-png/Firefox---WindowSafe und https://api.github.com/repos/felixvonvollmer-png/Firefox---WindowSafe/branches?per_page=100 — öffentliche Repoidentität und leere Branchliste, keine Schreiboperation.
- **M01:** https://www.firefox.com/en-US/firefox/156.0/releasenotes/ — Release 15.09.2026; gewählte Zielversion ist keine automatische Featurekompatibilitätsgarantie.
- **M02:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Background_scripts — nicht persistente Backgrounds, frühe Listener und Lebenszyklusgrenzen.
- **M03:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/background — Firefox-Background-Konfiguration versus Service Worker.
- **M04:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/permissions — Berechtigungsbedeutung, insbesondere `unlimitedStorage` und Hostrechte.
- **M05:** https://developer.mozilla.org/en-US/docs/Web/API/IDBDatabase/transaction — Transaktionen und Durability-Optionen.
- **M06:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/local — Firefox-Quota-/Deinstallationsgrenzen.
- **M07:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/session — flüchtiger Speicher, keine Festplattensicherung.
- **M08:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/contextualIdentities — Container-API, Berechtigungen und Aktivierungsnebenwirkung.
- **M09:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sessions/setWindowValue und https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sessions/getWindowValue — Fenster-Metadaten über Wiederherstellung.
- **M10:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sessions/setTabValue — Tab-Metadaten.
- **M11:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/runtime/onStartup — Startsignal, keine hier belegte globale Restore-Vollständigkeitsgarantie.
- **M12:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sessions — Umfang der dokumentierten Sitzungsschnittstelle.
- **M13:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/onRemoved — `isWindowClosing`.
- **M14:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/create — erlaubte URLs, Container, muted, discarded und Reader-Optionen.
- **M15:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/create — Fenstererzeugung und Geometrie-/Zustandsoptionen.
- **M16:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabGroups und https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/tabs/group — native Gruppen, instabile numerische IDs und Entpinnen beim Gruppieren.
- **M17:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Working_with_the_Tabs_API — Abschnitt über Split Views; ergänzend https://blog.mozilla.org/addons/2026/04/23/webextensions-api-changes-firefox-149-152/ — dokumentierter Entwicklungsstand der Schnittstellen, keine eigenen Laufzeittests.
- **M18:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/Window ; https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/WindowType ; https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/windows/onBoundsChanged — Fensterarten und Bounds, tatsächliche Plattformfähigkeit noch zu qualifizieren.
- **M19:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/download ; https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/DownloadItem ; https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/onChanged ; https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/downloads/removeFile — Downloadauftrag, Abschluss und ID-gebundene Dateibereinigung.
- **M20:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/alarms — Lebensdauer von Alarmen.
- **M21:** https://developer.mozilla.org/en-US/docs/Web/API/CompressionStream — native Stream-Kompression.
- **M22:** https://extensionworkshop.com/documentation/develop/web-ext-command-reference/ — web-ext-Tooling und Node-Voraussetzung.
- **M23:** https://extensionworkshop.com/documentation/develop/testing-persistent-and-restart-features/ — temporäre Installation reicht nicht für echte Neustarttests.
- **M24:** https://extensionworkshop.com/documentation/publish/signing-and-distribution-overview/ — spätere Signierungs-/Verteilungsgrenze.
- **M25:** https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/incognito — Ausschluss des Privatmodus.
