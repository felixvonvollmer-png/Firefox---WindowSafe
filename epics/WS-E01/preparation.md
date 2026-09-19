# WindowSafe – Epic Preparation WS-E01

```text
DOCUMENT_TYPE: EPIC_PREPARATION
EPIC_ID: WS-E01
EPIC_PREPARATION_ID: WS-E01-EP-20260919-01
STATUS: EPIC_PREPARATION_READY_FOR_REVIEW
DATE: 2026-09-19
CURRENT_CANONICAL_BASELINE_OR_MAIN_SHA: dc9c1c37a264cc80f79ec08bf166ec42cdd73b95
PROJECT: WindowSafe
EPIC_TITLE: Zuverlässige lokale Fenster-/Sitzungssicherung und manuelle Wiederherstellung (V1)
EPIC_RESEARCH_REUSE_OR_DELTA_STATUS: UPDATED
EPIC_PREPARATION_CRITICAL_SELF_REVIEW_STATUS: COMPLETE__NO_OPEN_CRITICAL_BLOCKING_MAJOR_SELF_FINDINGS
OPEN_MATERIAL_USER_DECISIONS_REQUIRED_BEFORE_START: NONE
```

## 1. Kanonische Ausgangslage

Diese Preparation ist ein kompakter Delta-Brief auf dem integrierten Project-Foundation-Stand
`dc9c1c37a264cc80f79ec08bf166ec42cdd73b95`. Sie ersetzt weder Product Truth noch Technical Foundation.

Kanonische Grundlagen:
- Product Definition: `foundation/inputs/inputs/WindowSafe_Product_Definition_WS-PD-20260917-01.md`
  plus separatem Approval Record.
- Technical Foundation: `foundation/inputs/inputs/WindowSafe_Technical_Foundation_WS-TFP-20260917-01_r6.md`
  plus Technical Decisions / T05-R2 / Preparation-PASS und READY-Binding.
- V6-Rollen: `foundation/sources/foundation-1.md` und `foundation/sources/foundation-2.md`.
- angenommener Project-Foundation-Review: `reviews/results/WS-PFR-20260918-02.json`.
- External Project Context Sync: `NOT_APPLICABLE`; kein separat installierter externer
  Projekttextkanal ist für WindowSafe gebunden.

Das Foundation-Gate ist integriert. Diese Preparation startet noch kein Feature und autorisiert
keine Browser-, Profil-, Release- oder Production-Arbeit.

## 2. Epic-Ziel und erwartetes Ergebnis

`WS-E01` liefert WindowSafe V1 als lokale Firefox-Desktop-Erweiterung, die normale
nicht-private Fenster und deren wiederherstellungsrelevante Tab-/Strukturmetadaten dauerhaft
sichert und bei teilweisem oder vollständigem Firefox-Restore-Ausfall **nur auf Nutzeraktion**
fehlende Inhalte wiederherstellen kann.

Am Epic-Ende soll der Nutzer:
- dauerhaft benannte Fenster speichern, wieder öffnen/fokussieren, umbenennen und entkoppeln können;
- automatische Recovery-Stände aller relevanten normalen Fenster haben;
- fehlende Fenster/Tabs nach fehlerhaftem Firefox-Start manuell ergänzen können, ohne bereits
  nativ wiederhergestellte Fenster automatisch zu duplizieren;
- die vereinbarten Container-/Gruppen-/Split-/Reader-/Pinned-/Muted-/Discarded-Grenzen
  datenerhaltend behandelt sehen;
- tägliche lokale Backups und nichtdestruktiven Import nutzen können;
- sichtbare Fehler-/Unklarheitszustände statt falscher Vollständigkeitsbehauptungen erhalten.

## 3. Scope

Im Epic enthalten sind die Produktankern `WS-CAP-01` bis `WS-CAP-04`, `WS-RESTORE`,
`WS-BACKUP`, `WS-QUALITY` und die für V1 relevanten `WS-AC-01` bis `WS-AC-11`.

Technische Scope-Grenzen:
- Firefox Desktop 156 als gebundene Mindest-/Referenzversion;
- Windows und Ubuntu Desktop als V1-Testmatrix;
- Firefox MV3 mit nichtpersistenter Event Page;
- IndexedDB als kanonische Recovery-Datenbank;
- kleine native HTML/CSS/TypeScript-Oberfläche;
- lokale Datenhaltung, lokale Downloads-Backups, kein eigener Server/Cloudpfad;
- produktive Implementierung erst hinter den vorgelagerten Plattform-/Messgates.

## 4. Nichtziele

Nicht Teil dieses Epics:
- automatisches Öffnen von Recovery-Fenstern beim Browserstart;
- Cloud-/Account-/geräteübergreifende Synchronisierung;
- Cookie-, Passwort-, Formular-, Seiteninhalts-, Screenshot- oder vollständiges Profilbackup;
- eigener komplexer Tab-Manager oder Nachbau fremder Gruppenmodelle;
- Content-Scripts für Datenerfassung, Native Messaging oder eigener Systemhelfer;
- Umgehung privilegierter Firefox-URL-/API-Beschränkungen;
- AMO-Veröffentlichung, Signierung, Lizenzentscheidung, Production Readiness oder Distribution;
- Unterstützung weiterer Plattformen/Firefox-Versionen ohne eigenes späteres Binding;
- reale Nutzerprofile oder reale Sitzungs-/Chronikdaten in Tests.

## 5. Harte Invarianten und geschützte Grenzen

Die vollständigen I01–I10 aus der Technical Foundation bleiben bindend. Für diesen Epic sind
insbesondere folgende Grenzen nicht verhandelbar:

1. Fehlende Fenster/Tabs beim Startup sind **kein Löschsignal**.
2. Firefox Session Restore bleibt autoritativ für bereits nativ wiederhergestellte physische Fenster;
   WindowSafe öffnet beim Start nichts automatisch.
3. Geschützte Recovery-Roots bleiben bis zur Auflösung bzw. ausdrücklichen Nutzerdisposition erhalten.
4. Whole-window-close / Firefox-Quit darf keinen gespeicherten Fensterinhalt als leeren Stand ersetzen.
5. Erfolg wird erst nach relevanter dauerhafter Operation behauptet.
6. Private Fenster werden weder live noch historisch noch im Backup erfasst.
7. URL ist keine Identität; Container dürfen nicht still auf Default umgebogen werden.
8. Import ist nichtdestruktiv und öffnet/ersetzt nichts automatisch.
9. Normalbetrieb bleibt ereignisorientiert ohne Polling-/Vollscan-Leerlauf.
10. Einschränkungen und Fehler bleiben sichtbar; keine privilegierten Hacks oder falsche Vollständigkeit.

## 6. Vorgelagerte Dependencies und Startgates

### 6.1 Project Foundation
Erfüllt: integrierter unabhängiger Project-Foundation-PASS, exakter main-Stand `dc9c1c37a264cc80f79ec08bf166ec42cdd73b95`,
External Project Context Sync `NOT_APPLICABLE`.

### 6.2 Plattform-/Erkennungsqualifikation
**Noch offen und bewusst Bestandteil des ersten technischen Enabler-Features.**
Vor jeder davon betroffenen Produktimplementierung müssen gemäß Technical Foundation §7.1
exakt gebunden sein:
- tatsächlicher Firefox-156-Build und Ziel-OS;
- sichere Abgrenzung normaler Fenster gegenüber Popup/DevTools sowie Web-App/PiP-Sonderfällen;
- Grenzen von Hidden Tabs, Restore-Erkennung und Session-Markern;
- Container-/`cookieStoreId`-Existenz und instanzübergreifende Zuordnung;
- Tab-Groups und Split-View-Erkennung/Rekonstruktion;
- nicht öffnungsfähige/privilegierte URLs und sichere Fallbacks.

Unsicherheit sperrt die **betroffene Produktimplementierung**, nicht die Qualifikationsarbeit selbst.
Materielle Produktabstriche gehen zurück an den Nutzer.

### 6.3 Messmethodenbindung
Vor der betroffenen Implementierung muss für R500/R2000/H und T05-R2 eine reproduzierbare
A/B-Methode gebunden sein: Hardware, OS-/Firefox-Build, Profilzustand, Hintergrundlast,
Warm-up, Prozessbaum/Attribution, Messintervalle, CPU/RAM/I/O/DB-Größe, Sicherungslatenz,
mindestens fünf Paare je Profil/OS sowie bekannte Unsicherheit.

### 6.4 Browser-/Test-Envelope
Browserproben benötigen künstliche Wegwerfprofile und separaten zulässigen Installationsweg.
Temporär geladene Add-ons reichen nicht als Restart-Beweis. Kein reales Nutzerprofil.
Der aktuelle Preparation-/Materialisierungslauf führt **keine** Browserprobe aus.

## 7. Feature-Map – keine Task-Mikroplanung

### WS-E01-F01 — Plattform-, Toolchain- und Messqualifikation
**Typ:** technischer Enabler, zwingender Vorgänger für betroffene Produktfeatures.

Ergebnis:
- gebundener Firefox-156-/Windows-/Ubuntu-Fähigkeits- und Erkennungsmatrix;
- verifizierte minimale Berechtigungs-/Manifest-Richtung;
- gebundene Toolchain (TypeScript/Node/web-ext/Packaging) erst nach Kompatibilitätsprüfung;
- synthetischer Wegwerfprofil-/Restart-Testweg;
- gebundene R500/R2000/H-/T05-R2-Messmethodik;
- dokumentierte sichere Fallbacks und offene Plattformgrenzen.

Keine Erfassungs-/Recovery-Produktlogik in diesem Feature, bevor die jeweiligen Gates erfüllt sind.
Browserproben benötigen eine spätere ausdrückliche Execution Authorization.

### WS-E01-F02 — Dauerhafte Recovery-Datenhaltung und ereignisorientierte Erfassung
**Abhängigkeit:** F01 für alle betroffenen Plattform-/Messfragen.

Ergebnis:
- kanonischer IndexedDB-Zustand mit stabilen eigenen Identitäten/Revisionen/geschützten Roots;
- Ereigniserfassung normaler nicht-privater Fenster/Tabs;
- konsistente Tab-/Fenster-/Gruppen-/Split-Metadaten innerhalb der qualifizierten Grenzen;
- Startup-Reconciliation, Close-/Quit-Safety und fail-closed Konfliktbehandlung;
- Session-Werte nur als nichtkanonische Identitätshinweise;
- begrenzte Recovery-Historie gemäß T03/WS-P01.

Hauptanker: WS-AC-02, 03, 05, 06, 07, 09 sowie relevante Teile von 11.

### WS-E01-F03 — Benannte Fenster und manuelle kontexttreue Wiederherstellung
**Abhängigkeit:** F01 + F02.

Ergebnis:
- aktuelles Fenster speichern; neues benanntes Fenster; Umbenennen/Entkoppeln;
- Fokus statt Duplikat bei bereits verbundenem Fenster;
- manuelles Öffnen fehlender Fenster/Tabs und „Fehlende Fenster wiederherstellen“;
- datenerhaltender Umgang mit Container-/Group-/Split-/Reader-/Pinned-/Muted-/Discarded-Grenzen;
- sichtbare Status-/Konflikt-/Teilresultatdarstellung;
- keine automatische Startup-Recovery.

Hauptanker: WS-AC-01, 03, 04, 05, 07, 08, 11.

### WS-E01-F04 — Tagesbackup, Aufbewahrung und nichtdestruktiver Import
**Abhängigkeit:** F01 + F02; Reihenfolge relativ zu F03 nach erfüllten Abhängigkeiten agentenautonom.

Ergebnis:
- konsistenter täglicher Export bei geändertem Stand;
- Downloadabschluss als Erfolgsgate;
- regulär 14 erfolgreiche Tagesbackups/Instanz und konservative Bereinigung nur eigener Dateien;
- Restart-/Fehlerbehandlung für unvollständige Versuche;
- versionierter, validierter, nichtdestruktiver Import als zusätzliche Recovery-Quelle;
- keine automatische Öffnung/Ersetzung.

Hauptanker: WS-AC-09, 10 und relevante Ressourcen-/Fehlerteile aus 11.

### WS-E01-F05 — Integrierte V1-Nativevidence und Performance-/Failure-Closure
**Typ:** technischer Enabler für Epic-Convergence, keine neue Produktfunktion.

**Abhängigkeit:** F02, F03 und F04 akzeptiert oder exakt als notwendige Vorgänger disponiert.

Ergebnis:
- native Restart-/vollständige/teilweise/verzögerte Restore-Szenarien;
- Whole-window-close/Firefox-Quit/Event-Page-Restart/Abbruch-Failpoints;
- Gruppen/Container/Split/Reader/privilegierte URL-/Sonderfenster-Grenzen;
- private-Daten-Ausschluss;
- Backup-/Importfehlerpfade;
- R500/R2000/H, Idle, L10/B300, Latenz, RAM, I/O und Export-/Import-Spitzen auf Windows und Ubuntu;
- kumulative Interaktionsprüfung und nachvollziehbare Evidence für Epic-Convergence.

Dieses Feature darf keine neuen Produktfähigkeiten erfinden, um Mess-/Testprobleme zu kaschieren.

## 8. Dependency-/Autonomiegrenze

Zwingend:
`F01 -> F02 -> {F03, F04} -> F05`.

Nach erfüllten Abhängigkeiten bleiben konkrete Reihenfolge von F03/F04, Task-Schnitt,
Worker/PR-Aufteilung und reversible Implementierungsdetails beim Coding-Agenten.
Default externe Feature-Concurrency bleibt ONE. Keine LLM-Mikroplanung pro Task/PR.

## 9. Architektur-, Daten-, Trust- und Provider-Delta

Kein materieller Architekturwechsel gegenüber Technical Foundation r6.

Bestätigt:
- Firefox-only MV3 Event Page bleibt passend;
- IndexedDB bleibt kanonisch, Session-Values nur Hint;
- keine neuen Provider/Server/Content-Scripts/Native-Messaging-Pfade;
- Downloads-API bleibt Dateibackuppfad;
- eigenes stabiles Gruppen-/Window-/Tab-Identitätsmodell bleibt erforderlich;
- Split-View-Fallback bleibt datenerhaltend;
- private Daten bleiben vollständig außerhalb der Produktdaten.

Der Epic führt keine neue Datenklasse und keinen neuen Trust-Provider ein.

## 10. Risiko und Review-Erwartung

**Kumulativer Risikofloor: ELEVATED.**

Begründung: Recovery-/Concurrency-Korrektheit, sensible Browsermetadaten, geschützte Roots,
destruktive Backupbereinigung, Import und Browseroperationen mit nichtatomaren Bestätigungen.

Für jedes Inkrement gilt die Foundation-2-Risikoklassifikation separat. PR-Splitting darf den
kumulativen Risikofloor nicht umgehen. Recovery-Core, Restore und Backupbereinigung benötigen
mindestens unabhängigen technischen Review vor Integration; High-Risk wird verwendet, wenn
der tatsächliche Changeset einen entsprechenden Trust-/Destruktivitäts-/Irreversibilitätsumfang
erreicht. Feature Acceptance bleibt zusätzlich separat.

## 11. Verification-/Acceptance-/Evidence-Richtung

Vor Featurestart:
- exakte Feature-Baseline/Subject/Evidence;
- Product-/Foundation-/Epic-Kompatibilität;
- erforderliche vorgelagerte Gates erfüllt;
- risikoadäquate Execution Authorization.

Während Implementierung:
- deterministische Modell-/Unit-/Contract-/Failpoint-Tests;
- keine behauptete native Evidence ohne echten Browserlauf;
- keine realen Nutzerdaten.

Vor Feature Acceptance:
- kumulative Feature-Evidence gemäß Foundation 2;
- exakter CI-/Changeset-Stand;
- native Runtime-Evidence soweit für das Feature erforderlich;
- offene Critical/Blocking/Major = NONE;
- relevante Ressourcen-/Performance-Nachweise;
- sichtbare Einschränkungen statt stiller Fallbacks.

Epic-Convergence:
- alle notwendigen Features akzeptiert/disponiert;
- vollständige V1-Interaktions- und Nativevidence aus F05;
- keine offenen Epic-Critical/Blocking/Major;
- Product/Foundation/Living Docs synchron.

## 12. Research-Reuse/Delta

Status: `UPDATED`.

Die Foundation-Recherche bleibt grundsätzlich gültig. Am 2026-09-19 wurden aktuelle
Mozilla-/MDN-Primärquellen und ein eng begrenzter Open-Source-Delta-Check erneut geprüft.
Es ergab sich **kein materieller Produkt- oder Architekturwechsel**, aber mehrere
Preparation-relevante Bestätigungen:
- Firefox 156 ist seit 2026-09-15 veröffentlicht; die Add-on-Developer-Änderungen in 156
  betreffen die hier verwendeten Window/Tab/Session/Download-APIs nicht.
- Firefox MV3 nutzt weiterhin nichtpersistente Background Scripts/Event Pages;
  `background.service_worker` ist in Firefox weiterhin nicht unterstützt.
- `tabGroups` kann Gruppenmetadaten verwalten; Group-IDs sind über Restore nicht stabil.
- Split-View-Mitgliedschaft ist über `splitViewId` beobachtbar, aber APIs zum expliziten
  Erzeugen/Entfernen von Split Views sind weiterhin nicht verfügbar.
- `tabs.create()` dokumentiert `cookieStoreId`, `discarded`, `muted`, `openInReaderMode`,
  `pinned` und Fehler bei nicht öffnungsfähigen privilegierten URLs.
- `windows.WindowType` dokumentiert nur `normal`, `popup`, `panel`, `devtools`; dies genügt
  nicht als alleiniger Beweis für Web-App-/PiP-Abgrenzung.
- Temporär installierte Erweiterungen verschwinden beim Firefox-Neustart; Restart-Evidence
  braucht daher einen geeigneten dauerhaft installierten Teststand in einem Wegwerfprofil.
- Mozilla-Beispiele sind als API-Referenzen nützlich, ersetzen aber kein Recovery-Protokoll.
  Simple Tab Groups zeigt ähnliche Berechtigungs-/Backupfelder, nutzt jedoch deutlich breitere
  Funktionen/Permissions (u.a. Tab-Verstecken, Hostzugriff und optional Native Messaging);
  daraus wird **keine** Komponente übernommen.

Details und Quellen: `epics/WS-E01/evidence/research.md`.

## 13. Modell-/Qualitätsgrenzen

- unabhängiger Epic Preparation Review: frischer/ausreichend isolierter
  `INDEPENDENT_EPIC_PREPARATION_REVIEWER`;
- Implementierer darf dieses Verdict nicht selbst erzeugen;
- stärkere Modelle ersetzen keine erforderliche Unabhängigkeit;
- innerhalb des Epics JIT-Modell-/Reasoning-Zuordnung nach Risiko/Komplexität;
- unbekannte oder risikoreiche Recovery-/Concurrency-Probleme nicht blind auf niedrige
  Reasoning-Stufe routen.

## 14. Offene agent-owned technische Fragen

Diese Punkte sind **keine offenen materiellen Nutzerentscheidungen** und werden innerhalb F01
bzw. der jeweiligen Feature-Grenze evidenzbasiert entschieden:
- exakte Sonderfenster-/Web-App-/PiP-Erkennung auf Firefox 156;
- konkrete Toolchain-/Compiler-/web-ext-Versionen;
- genaue synthetische Testprofil-Installation für Restarttests;
- konkrete A/B-Messwerkzeuge und Prozessattribution auf Windows/Ubuntu;
- interne IndexedDB-Schema-/Revision-/GC-Repräsentation;
- Debounce/Max-Latency-Mechanik;
- Restore-Matching-Heuristik innerhalb I01–I10;
- Geometriesanitierung und native API-Fallbackdetails;
- Gzip-/unkomprimierter Exportpfad innerhalb der Foundation-Grenzen.

## 15. OPEN_LATER mit Triggern

- **Materialer Plattformabstrich:** Wenn F01 zeigt, dass eine freigegebene Produktfähigkeit
  auf der Zielmatrix nicht sicher umsetzbar ist -> STOP betroffene Arbeit -> Nutzerentscheidung
  -> ggf. Product/Foundation/Epic-Delta + neues Review.
- **Browser-Testinstallation:** vor tatsächlicher Browserprobe separat autorisieren; keine
  Signaturabschaltung im realen Nutzerprofil.
- **Distribution/Signierung/Lizenz:** vor Auslieferung separat entscheiden.
- **Neue Provider/Kosten/Secrets:** nur nach ausdrücklicher Nutzerfreigabe.
- **Production Readiness:** erst vor realen Nutzern/Produktionsdaten.

## 16. Proportionality Pass

Diese Preparation referenziert Product/Foundation statt sie zu duplizieren, enthält keine
Datei-/Klassen-/Task-/PR-Mikroplanung und hält nur Epic-relevante Deltas, Abhängigkeiten,
Risiken, Feature-Richtungen und Evidence-Gates. `WS-E01` bleibt bewusst ein zusammenhängender
V1-Epic und wird nicht in künstliche Mikro-Epics zerlegt.

## 17. Gate-Status

```text
PROJECT_FOUNDATION_REVIEW_PASS: SATISFIED
EXTERNAL_PROJECT_CONTEXT_SYNC: NOT_APPLICABLE
EPIC_PREPARATION_PROPORTIONALITY_PASS: COMPLETE
EPIC_PREPARATION_CRITICAL_SELF_REVIEW: COMPLETE__NO_OPEN_CRITICAL_BLOCKING_MAJOR_SELF_FINDINGS
OPEN_MATERIAL_USER_DECISIONS_REQUIRED_BEFORE_START: NONE
EPIC_PREPARATION_INDEPENDENT_REVIEW: PENDING
EPIC_BINDING_STATUS: REVIEW_REQUIRED
READY_FOR_AGENT: NO
PRODUCT_FEATURE_IMPLEMENTATION_AUTHORIZED: NO
BROWSER_PROFILE_TEST_EXECUTION_AUTHORIZED: NO
```
