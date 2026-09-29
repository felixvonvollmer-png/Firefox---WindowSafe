# WindowSafe — WS-E01 Epic Preparation Delta

```text
DOCUMENT_TYPE: EPIC_PREPARATION_DELTA
EPIC_ID: WS-E01
EPIC_PREPARATION_DELTA_ID: WS-E01-EP-DELTA-20260929-02
PREVIOUS_PREPARATION_DELTA_ID: WS-E01-EP-DELTA-20260929-01
PREVIOUS_PREPARATION_DELTA_SHA256: e848043bd6cdf8c28e3b9eff72e97ec5c738567a26e5705dfb9851cb65cc074f
DATE: 2026-09-29
STATUS: CRITICAL_SELF_REVIEW_COMPLETE__READY_FOR_MATERIALIZATION
MODE: BROWNFIELD__APPEND_ONLY_DELTA

CURRENT_CANONICAL_BASELINE_OR_MAIN_SHA: 1cb82c926903b2fd6b497d008db61c71c5d92aca

BASE_EPIC_PREPARATION_ID: WS-E01-EP-20260919-01
BASE_EPIC_PREPARATION_GIT_BLOB: a92fbe87a9640b67367db96631e082864b89e9b3
BASE_EPIC_SUBJECT_GIT_BLOB: f12b4756046febfec07b0426a0129bce482ce2d2
BASE_EPIC_BINDING_GIT_BLOB: 930b4c3176a9601e44f7a4b04ff1d4530488b6e1
BASE_REVIEWED_EPIC_SUBJECT_END_SHA: 644b81f63dcc1990bc894a9c2c9bd8dc24a98c04

PROJECT_FOUNDATION_ACCEPTED_BINDING_BLOB: 8a85ff8481a6bd831b3e2ace3382404762476834
PROJECT_FOUNDATION_REVIEW_RESULT_BLOB: ff96f8b1cac7d9a664339c7df55ddbf77947e3a8
PROJECT_FOUNDATION_REVIEW_ID: WS-PFR-DELTA-20260928-01
PROJECT_FOUNDATION_REVIEW_VERDICT: PASS

APPROVED_PRODUCT_DELTA_ID: WS-PD-DELTA-20260924-01
APPROVED_PRODUCT_DELTA_GIT_BLOB: c8d52f1720aa24544b0d24f652e6b9c8d14254ec
TECHNICAL_FOUNDATION_DELTA_ID: WS-TFP-DELTA-20260928-02
TECHNICAL_FOUNDATION_DELTA_GIT_BLOB: 539dd9d35d40b832c07a779e351e7964af9f8705

EXTERNAL_PROJECT_CONTEXT_SYNC_ID: WS-EXTCTX-SYNC-20260929-01
EXTERNAL_PROJECT_CONTEXT_SYNC_SHA256: d4bdc815e281f083acd6222d1ff19dc4255e05d2a52038d42bb360b5c61f2062
EXTERNAL_PROJECT_CONTEXT_DESCRIPTION_SHA256: 647d8fcffff3c55b8e32f33f0cb80e22591bea77835817db87a96659f52f4ba5
EXTERNAL_PROJECT_CONTEXT_SYNC_STATUS: CONFIRMED_BY_USER

F01_PR: 3
F01_HEAD: 7d66ca5b025c8f748d7f97b961c496ee450daaa7
F01_STATE_BLOB: 7515185da745289574f6aeaa556732c93625e128
F01_UBUNTU_CLOSURE_BLOB: 9f22df503da45409a1b57e6512f0067faf9f5e4f

EPIC_RESEARCH_REUSE_OR_DELTA_STATUS: REUSED_NO_MATERIAL_DELTA
EPIC_PREPARATION_PROPORTIONALITY_PASS: COMPLETE
EPIC_PREPARATION_CRITICAL_SELF_REVIEW_STATUS: COMPLETE__NO_OPEN_CRITICAL_BLOCKING_MAJOR_SELF_FINDINGS
OPEN_MATERIAL_USER_DECISIONS_REQUIRED_BEFORE_START: NONE

INDEPENDENT_EPIC_PREPARATION_REVIEW: REQUIRED__PENDING
EXACT_EPIC_REBINDING: NOT_CREATED
READY_FOR_AGENT: NO
F01_CONTINUATION_AUTHORIZED: NO
PRODUCT_FEATURE_IMPLEMENTATION_AUTHORIZED: NO
```

## 1. Zweck

Dieses Dokument ist **nur das Delta** zur historischen, unabhängig angenommenen
`WS-E01-EP-20260919-01`. Die historische Preparation, ihr Subject, ihr Review und ihr Binding
werden weder überschrieben noch rückwirkend umgedeutet.

Das Delta ist erforderlich, weil F01 nach der historischen Epic-Bindung eine materielle
Sonderfenstergrenze aufgedeckt hat und der Nutzer daraufhin Product Truth sowie Project Technical
Foundation geändert hat. Zusätzlich wurde die aktuelle Project Foundation neu gebunden/reviewt und
der tatsächlich verwendete externe ChatGPT-Projektkontext nach Project-Foundation-PASS synchronisiert.

## 2. Aktuelle kanonische Ausgangslage

Wirksam für dieses Delta sind:

- Base Product Definition `WS-PD-20260917-01` plus freigegebenes
  `WS-PD-DELTA-20260924-01` (WS-P05);
- Technical Foundation r6 plus unabhängig reviewtes/bound
  `WS-TFP-DELTA-20260928-02`;
- angenommene Project Foundation auf aktuellem `main`
  `1cb82c926903b2fd6b497d008db61c71c5d92aca`;
- unabhängiger Project-Foundation-PASS `WS-PFR-DELTA-20260928-01`;
- externer WindowSafe-ChatGPT-Projektkontext: `CONFIRMED_BY_USER` durch
  `WS-EXTCTX-SYNC-20260929-01@sha256:d4bdc815e281f083acd6222d1ff19dc4255e05d2a52038d42bb360b5c61f2062`.

Der historische WS-E01-Bindingstatus `READY_FOR_AGENT` ist **keine** Autorisierung für die
post-WS-P05-F01-Fortsetzung. Vor Wiederaufnahme sind dieses Delta, unabhängiger Epic Review,
Exact Rebinding und eine neue F01-Ausführungsautorisierung erforderlich.

## 2.1 Nutzerbestätigte Epic-/Autonomierichtung

Der Nutzer hat im Project-LLM-Chat ausdrücklich bestätigt, dass **WS-E01 der eine
zusammenhängende WindowSafe-V1-Epic bleibt**. Für V1 werden keine zusätzlichen Mikro-Epics
eingeführt.

Kanonische Feature-Grenzen innerhalb dieses Epics bleiben:

`F01 -> F02 -> {F03, F04} -> F05`.

Nach erfolgreichem unabhängigen Review dieses Epic-Deltas und Exact Rebinding soll eine
**separate breite WS-E01-Ausführungsautorisierung** vorbereitet werden. Sie darf den
Lead-/Coding-Agenten autorisieren, den verbleibenden WS-E01-Lauf von F01 bis
`EPIC_CONVERGED` innerhalb der gebundenen Product-/Foundation-/Epic-Grenzen autonom
durchzuführen, statt für jedes Feature zum Project-LLM zurückzukehren.

Diese breite Autorisierung darf insbesondere **nicht** bedeuten:

- Implementierer erzeugt eigene unabhängige Verdicts;
- Feature-Acceptance-, technische Review-, Risk-, Evidence- oder CI-Gates entfallen;
- ein fehlgeschlagenes Gate wird aus Bequemlichkeit abgeschwächt;
- neue materielle Product-/Scope-/Architektur-/Security-/Daten-/Provider-/Kosten- oder
  Betriebsentscheidungen werden vom Agenten selbst getroffen;
- ein Folge-Epic wird automatisch ausgewählt oder gestartet.

Der Lead/Coding-Agent darf innerhalb des gebundenen Epics Tasks, technische Details,
PR-Schnitt, Fixes, Reihenfolge von F03/F04 und zulässige Review-/Worker-Orchestrierung
autonom steuern. Er darf erforderliche unabhängige Reviews nur durch tatsächlich getrennte
Reviewer-/Kontexte konsumieren; stärkere Modelle oder Self-Review ersetzen Unabhängigkeit nicht.

`STOP_AND_REPORT` an den Nutzer/Project-LLM ist erst erforderlich, wenn:
- eine neue materielle Nutzerentscheidung benötigt wird;
- ein gebundener Review-/Security-/Risk-/Lifecycle-Gate nicht sicher erfüllbar ist;
- notwendige Unabhängigkeit in der verfügbaren Umgebung tatsächlich nicht hergestellt werden kann;
- Product/Foundation/Epic-Rebinding materiell erneut nötig wird.

Normale Feature-/Task-/PR-Zwischenschritte erzeugen **kein zusätzliches Project-LLM-Gate**.

Nach `EPIC_CONVERGED` greift weiterhin der V6-Post-Epic-Stop:
Project-LLM + Nutzer prüfen Produktstand und entscheiden erst dann über
nächsten Epic, Stop oder Production Readiness. Aktuell ist **kein WS-E02 ausgewählt**.

## 3. Product-/Restore-Delta — WS-P05

Für öffentlich nicht zuverlässig unterscheidbare Sonderfenster, insbesondere native
WebApp-/Taskbar-Tab-Fenster, die über die öffentliche Firefox-WebExtension-API als `normal`
erscheinen, gilt:

- öffentlich sichtbare, nichtprivate Tab-/Sitzungsdaten dürfen über den gewöhnlichen
  WindowSafe-Datenpfad gesichert werden;
- WindowSafe behauptet keine zuverlässige WebApp-/Taskbar-Identität;
- Wiederherstellung erfolgt ausschließlich als gewöhnliche Firefox-Fenster/Tabs;
- native App-Shell, Pinning/Taskbar-Semantik, OS-Integration und sonstige native
  Sonderfenster-Eigenschaften werden nicht als erhalten oder rekonstruiert zugesagt;
- keine privaten Firefox-/Chrome-Attribute und keine URL-/Titel-/Geometrieheuristik werden
  als Ersatzidentität verwendet;
- die tatsächlich geltende Einschränkung muss für Nutzer sichtbar sein.

Andere bereits qualifizierte oder weiterhin unterscheidbare Sonderfenstergrenzen werden dadurch
nicht pauschal erweitert.

## 4. F01 — geänderte Qualifikationsgrenze

F01 bleibt ein technischer Enabler. Es implementiert weiterhin **keine produktive
Capture-/Recovery-Logik**.

Nach dem vollständigen Epic-Rebinding darf F01 nur noch den verbleibenden
Qualification-Scope schließen:

1. WS-P05-Fallback technisch qualifizieren:
   - öffentlich sichtbare Tab-/Sitzungsdaten sind über akzeptierte öffentliche APIs verfügbar;
   - gewöhnliche Fenster/Tabs sind ein tragfähiger öffentlicher Restore-Zielpfad;
   - kein interner WebApp-Discriminator ist für diesen Fallback erforderlich;
   - spätere Produkt-/Acceptance-Evidence kann die allgemeine sichtbare Limitierung prüfen.
2. verbleibende Ubuntu Display-/Geometry-/State-Evidence abschließen;
3. Cross-OS Measurement-/Memory-/Peak-Methodik und Attribution fertig qualifizieren.

`TARGET_EQUIVALENT_RESTART` bleibt aufgrund der vorhandenen gebundenen Windows-/Ubuntu-Evidence
geschlossen, sofern keine neue gegenteilige Evidence entsteht.

Die historischen F01-Dateien am PR-#3-Head bleiben absichtlich unverändert und zeigen weiterhin
`WS-E01-F01_BLOCKED__MATERIAL_USER_DECISION_REQUIRED`. Dieser historische Status wird **nicht**
als aktuelle Nutzerentscheidung interpretiert; seine materielle Ursache wurde durch WS-P05
beantwortet. Er wird erst innerhalb eines neu autorisierten, exakt rebound F01-Laufs durch neue
append-only Evidence fortgeschrieben.

Die bisherigen offenen Gates `WINDOWS_DESKTOP`, `SPECIAL_NATIVE_GUI_CASES` und
`MEASUREMENT_FINAL_ATTRIBUTION` werden durch die Nutzerentscheidung **nicht automatisch geschlossen**.

## 5. Folgewirkung auf spätere WS-E01-Features

### F02 — Recovery-Datenhaltung und Capture

Keine neue Feature-Richtung. F02 darf öffentlich nicht unterscheidbare `normal`-Fälle nicht
aufgrund einer erfundenen WebApp-Erkennung verwerfen. Es implementiert nur die nach F01
qualifizierten öffentlichen Datenpfade.

### F03 — manuelle Wiederherstellung

Zusätzlich zur historischen Preparation:

- öffentlich nicht unterscheidbare Sonderfensterdaten werden bei Restore nur als gewöhnliche
  Fenster/Tabs wiederhergestellt;
- die Nutzeroberfläche darf keine native WebApp-/Taskbar-Wiederherstellung behaupten;
- die allgemeine Einschränkung muss sichtbar und testbar sein.

### F04 — Backup / Import

Kein materielles Delta. Gesicherte WS-P05-Daten bleiben innerhalb der allgemeinen
nichtprivaten, nichtdestruktiven Backup-/Importregeln.

### F05 — integrierte Closure

F05 muss später zusätzlich nachweisen, dass:
- der WS-P05-Daten-/Tab-Fallback keine öffentlich sichtbaren, freigegebenen Daten verliert;
- keine native WebApp-Identität als wiederhergestellt behauptet wird;
- die sichtbare Einschränkung mit dem tatsächlich gelieferten Restore-Verhalten übereinstimmt.

## 6. Abhängigkeiten und Autonomie

Die bestehende Dependency-Richtung bleibt:

`F01 -> F02 -> {F03, F04} -> F05`.

Keine neue Feature-Aufspaltung und keine Task-/Datei-/PR-Mikroplanung wird durch dieses Delta
vorgegeben. Nach erfüllten Gates bleiben reversible technische Details agent-owned.

## 7. Project-/Context-Gates

```text
PROJECT_FOUNDATION_ACCEPTED: YES
PROJECT_FOUNDATION_REVIEW: PASS
EXTERNAL_PROJECT_CONTEXT_SYNC: CONFIRMED_BY_USER
EPIC_PREPARATION_DELTA: THIS_SUBJECT
CRITICAL_SELF_REVIEW: COMPLETE
INDEPENDENT_EPIC_PREPARATION_REVIEW: PENDING
EXACT_EPIC_REBINDING: PENDING
NEW_F01_EXECUTION_AUTHORIZATION: PENDING
```

Der externe Context-Sync ist durch die Nutzerbestätigung an die exakte Beschreibung
`sha256:647d8fcffff3c55b8e32f33f0cb80e22591bea77835817db87a96659f52f4ba5` gebunden. Der Project-LLM kann die UI nicht selbst inspizieren; die
tatsächliche Installation beruht deshalb auf der expliziten Nutzerbestätigung.

## 8. Research-Reuse-/Guidance-Delta

`EPIC_RESEARCH_REUSE_OR_DELTA_STATUS = REUSED_NO_MATERIAL_DELTA`.

Begründung:

- Die materielle Plattformfrage ist durch bereits gebundene F01-Windows-/Ubuntu-Evidence und
  exakte Firefox-156-Quellen entstanden und wurde danach in Product/TF reviewt;
- dieses Epic-Delta erzeugt keine neue Firefox-API-, Provider-, Dependency- oder
  Architekturbehauptung, die zusätzliche externe Recherche benötigt;
- die weiterhin offenen Display-/Measurement-Fragen gehören in F01-Evidence und werden dort
  nicht durch neue Preparation-Annahmen ersetzt.

Für diesen neuen materiellen Epic-Preparation-Auftrag wurde der aktuelle Global-Guidance-Router
am Meta-main `47816eecb9df524aa1d91d564496dea5bc4b94b7` gelesen:
- Router blob `6533828691dd918dc9303b216d78bed616364fd2`;
- relevante AI-Agent-Guidance blob `58d80fe4e45bd64667df92769cbd23654e2a55e2`.

Diese Guidance beeinflusst nur spätere Agent-/Effort-/Kontextwahl innerhalb gebundener Grenzen und
besitzt keine Governance- oder Scope-Autorität.

## 9. Risiko / Reviews

Der kumulative WS-E01-Risikofloor bleibt mindestens `ELEVATED`.

Das Delta verändert keinen Provider, keine neue Berechtigung und keinen produktiven Datenpfad
außerhalb der bereits freigegebenen WS-P05-Grenze. Wegen Recovery-/Plattform-/Lifecycle-Relevanz
bleibt ein unabhängiger `EPIC_PREPARATION_REVIEW` erforderlich.

PASS des Epic Reviews allein startet F01 nicht. Danach folgen:
- Exact Epic Rebinding;
- separate neue F01 Execution Authorization;
- erst dann F01-Restqualifikation.

## 10. Offene Entscheidungen

```text
OPEN_MATERIAL_USER_DECISIONS_REQUIRED_BEFORE_START: NONE
```

Neue materielle Nutzerentscheidungen sind nur erforderlich, wenn neue F01-Evidence eine weitere
Product-/Scope-/Security-/Architekturabweichung zeigt.

## 11. Proportionality Pass

Dieses Delta ändert nur:
- Product-/TF-Anker auf WS-P05;
- F01-Qualification-Grenze;
- F03/F05-Fallback-/Evidence-Richtung;
- Project-Foundation-/External-Context-Sync-Basis;
- Rebinding-Gates.

Unveränderte Teile der historischen WS-E01 Preparation werden referenziert und nicht dupliziert.
Es gibt keine Datei-/Klassen-/Task-/PR-Mikroplanung.

## 12. Stop

Bis zu unabhängigem Epic-PASS und Exact Rebinding:

- keine F01-Fortsetzung;
- kein F02/Product-Code;
- keine Browserprobe;
- keine Feature Acceptance;
- kein Merge von PR #3;
- keine Release-/Production-Arbeit.

Nach Exact Rebinding entsteht **nicht automatisch** Ausführungsautorität. Erst eine separate
breite WS-E01 Execution Authorization darf anschließend den autonomen Restlauf F01–F05 bis
`EPIC_CONVERGED` freigeben. Sie muss die bestehenden unabhängigen Review-/Acceptance-Gates
und materielle Stop-Bedingungen ausdrücklich erhalten.
