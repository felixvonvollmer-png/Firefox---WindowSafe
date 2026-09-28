# WindowSafe – Technical Foundation Delta Preparation

```text
DOCUMENT_TYPE: TECHNICAL_FOUNDATION_DELTA_PREPARATION_SUBJECT
PREPARATION_ID: WS-TFP-DELTA-20260928-01
PROJECT: WindowSafe
DATE: 2026-09-28
STATUS: CRITICAL_REVIEW_COMPLETE__INDEPENDENT_REVIEW_REQUIRED
MODE: BROWNFIELD__APPEND_ONLY_DELTA

BASE_TECHNICAL_FOUNDATION_ID: WS-TFP-20260917-01
BASE_TECHNICAL_FOUNDATION_REVISION: 6
BASE_TECHNICAL_FOUNDATION_SHA256: c461c45c5bd20f12dcffb400acd6f7d5c0f0de0a75616eef3eb1d78dd175dcb6
BASE_TECHNICAL_FOUNDATION_GIT_BLOB_AT_CURRENT_F01_HEAD: 446e1e0553aa64997345b16c2c0c8e97cb6709b6

APPROVED_BASE_PRODUCT_DEFINITION_ID: WS-PD-20260917-01
APPROVED_BASE_PRODUCT_DEFINITION_SHA256: fff235b7591f483b9b31c945911a6b5950d29fac931b9136438ae5586c756900
APPROVED_PRODUCT_DELTA_ID: WS-PD-DELTA-20260924-01
APPROVED_PRODUCT_DELTA_SHA256: 0caca99a713a0e026af5b63beee5f8abc310ef3d38f20c9653cd3042322aec16
PRODUCT_DELTA_APPROVAL_ID: WS-PD-DELTA-APPROVAL-20260928-01
PRODUCT_DELTA_APPROVAL_SHA256: 9e15db18b095655dfc503d67cad4486998e68493c323f8b2217e9d71e5987ab5

V6_ACTIVE_FOUNDATION_1_BLOB: 0c10e10eebcb2b23336cc9cdf4a88305a209fd22
V6_ACTIVE_FOUNDATION_2_BLOB: 3034da0fbee6ab79318da25ed65ccdc0933074e5

TARGET_REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
TARGET_REPOSITORY_ID: 1374094477
CURRENT_MAIN_SHA: 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
CURRENT_F01_BRANCH: feature/ws-e01-f01-qualification
CURRENT_F01_HEAD: 7d66ca5b025c8f748d7f97b961c496ee450daaa7
CURRENT_F01_PR: 3__DRAFT__UNMERGED
CURRENT_F01_STATE: WS-E01-F01_BLOCKED__MATERIAL_USER_DECISION_REQUIRED

RISK_CLASS: ELEVATED
CRITICAL_REVIEW_STATUS: COMPLETE__CORRECTIONS_APPLIED__NO_OPEN_CRITICAL_BLOCKING_MAJOR_FINDINGS
INDEPENDENT_TECHNICAL_FOUNDATION_PREPARATION_REVIEW: REQUIRED__PENDING
EXACT_BINDING_STATUS: NOT_CREATED
CODING_AGENT_MATERIALIZATION_AUTHORIZED: NO
F01_CONTINUATION_AUTHORIZED: NO
```

## 1. Zweck und Delta-Grenze

Dieser Subject beschreibt ausschließlich das Project-Technical-Foundation-Delta aus der
freigegebenen Produktregel **WS-P05**: öffentlich nicht zuverlässig unterscheidbare
Sonderfenster wie native WebApp-/Taskbar-Tab-Fenster dürfen ihre öffentlich sichtbaren,
nichtprivaten Tab-/Sitzungsdaten in den normalen WindowSafe-Datenpfad einbringen; eine
WindowSafe-Wiederherstellung verspricht jedoch nur gewöhnliche Firefox-Fenster/Tabs und
keine native WebApp-/Taskbar-Rekonstruktion.

`WS-TFP-20260917-01 r6` bleibt unverändert historische und weiterhin wirksame Foundationbasis.
Dieses Delta wirkt nach erfolgreichem Review und Exact Binding additiv. Es ist kein
Greenfield-Neuentwurf.

## 2. Evidenzbasis

F01 hat auf Firefox 156 sowohl unter Windows als auch Ubuntu beobachtet:

- native WebApp-/Taskbar-Tab-Fenster können im Test erzeugt und nativ identifiziert werden;
- über die öffentliche WebExtension-Schnittstelle werden diese Fälle als `normal` exponiert;
- ein belastbarer öffentlicher WebApp-/Taskbar-Discriminator wurde in der gebundenen
  API-/Quellenprüfung nicht gefunden;
- URL, Titel, Geometrie und privilegierte native/Chrome-Attribute sind kein zulässiger
  Ersatz für Produktidentität.

Diese Evidence begründet das Delta; sie wird nicht als native Produktfähigkeit umgedeutet.

## 3. Delta zu Foundation §7 – Sonderfenster

Die Grundrichtung bleibt: normale nichtprivate Browserfenster sind das primäre Ziel.

Für Sonderfenster werden zwei technische Klassen unterschieden:

### A. Öffentlich zuverlässig unterscheidbare Klassen

Wenn die akzeptierte öffentliche Firefox-WebExtension-API eine belastbare Unterscheidung
liefert, wird die dafür gebundene sichere Behandlung verwendet. Bereits qualifizierte
Private-/DevTools-/PiP- und weitere Grenzen bleiben dadurch unverändert.

### B. Öffentlich nicht zuverlässig unterscheidbare `normal`-Fälle

Für Fälle innerhalb WS-P05 gilt:

- öffentlich sichtbare, nichtprivate Tabs und sonstige bereits freigegebene
  wiederherstellungsrelevante Daten dürfen über denselben öffentlichen Datenpfad wie normale
  Fenster erfasst werden;
- WindowSafe speichert oder behauptet **keine** native WebApp-/Taskbar-Identität;
- Wiederherstellung benutzt ausschließlich öffentliche APIs für gewöhnliche Fenster/Tabs;
- App-Shell, Taskbar-/Pinning-Semantik, OS-Integration und andere nicht öffentlich
  rekonstruierbare Sonderfenster-Eigenschaften sind außerhalb der V1-Restore-Zusage;
- keine internen Firefox-/Chrome-Attribute, keine URL-/Titel-/Geometrieheuristik und keine
  zusätzliche privilegierte Berechtigung wird zum scheinbar verlässlichen Discriminator.

Da der Sonderfensterstatus gerade **nicht zuverlässig erkennbar** ist, verlangt die Foundation
keinen per-Fenster-Fallbackmarker. Stattdessen muss die Produktoberfläche beziehungsweise die
für den Restore relevante Nutzerinformation die allgemeine, tatsächlich geltende Grenze sichtbar
machen: WindowSafe stellt Fenster/Tabs wieder her; native WebApp-/Taskbar-Eigenschaften werden
nicht garantiert. Ein einzelner Restore darf keine native Sonderfenster-Vollständigkeit behaupten.

## 4. Delta zu Foundation §7.1 – Preimplementation Platform Gate

Der harte Preimplementation-Halt bleibt bestehen, wird aber präzisiert.

Vor produktiver Erfassung einer relevanten Sonderfensterklasse muss **entweder**

1. eine belastbare öffentliche Erkennung plus sichere spezifische Behandlung gebunden sein,

**oder**

2. eine ausdrücklich freigegebene, datenerhaltende Fallback-Grenze wie WS-P05 technisch
   qualifiziert und gebunden sein.

Für die qualifizierten WebApp-/Taskbar-Tab-Fälle ist damit kein nicht vorhandener öffentlicher
Discriminator mehr Voraussetzung. F01 muss vor Wiederaufnahme betroffener Produktarbeit noch
auf Qualification-Ebene belegen:

- die regulär sichtbaren Tab-/Sitzungsdaten sind über die akzeptierten öffentlichen APIs
  ohne privilegierte Sondermechanismen zugänglich;
- gewöhnliche Fenster/Tabs sind ein technisch tragfähiger öffentlicher Restore-Zielpfad;
- kein interner Discriminator ist für diesen Daten-/Tab-Fallback erforderlich;
- die allgemeine sichtbare Limitierung ist als später testbarer Produktvertrag eindeutig;
- die bereits gebundenen Ausschluss-/Sicherheitsgrenzen für unterscheidbare Sonderfälle bleiben intakt.

F01 implementiert dabei **keine** WindowSafe-Capture-/Restore-Produktlogik und keine finale UX.
Die tatsächliche Produktimplementierung und ihr nutzerseitiger Fallback-/Hinweisnachweis folgen
erst in den dafür vorgesehenen Features und der späteren Acceptance-/F05-Evidence.

## 5. Verifikations- und Acceptance-Folgewirkung

Die spätere WS-AC-08-Evidence muss zusätzlich prüfen:

- öffentlich nicht unterscheidbare WebApp-/Taskbar-Tab-Fälle verlieren keine innerhalb der
  akzeptierten API sichtbaren Tabdaten;
- WindowSafe stellt diese Daten nur über gewöhnliche Fenster/Tabs wieder her;
- keine privilegierte Erkennung oder Heuristik wird als Produktidentität verwendet;
- die allgemeine Einschränkung zu nativen WebApp-/Taskbar-Eigenschaften ist sichtbar;
- Erfolgsaussagen beziehen sich auf den gebundenen WindowSafe-Daten-/Tab-Restore und behaupten
  keine native WebApp-Rekonstruktion.

Diese Acceptance-Folgewirkung ist **kein F01-Produktimplementierungsauftrag**.

## 6. Berechtigungen, Architektur und Datenfluss

Keine neue Produktberechtigung und kein neuer Provider werden durch dieses Delta eingeführt.

Unverändert insbesondere:

- öffentliche Firefox-WebExtension-APIs;
- MV3 Event Page;
- IndexedDB als kanonische Recovery-Datenbank;
- kleine Session-Werte nur als Hints;
- Downloads-basierter Backup-Pfad;
- kleine native HTML/CSS-Oberfläche;
- kein Server, keine Cloud, keine Telemetrie;
- keine allgemeinen Host Permissions, kein `scripting`, kein `nativeMessaging`;
- keine privaten Firefox-/Chrome-Schnittstellen im Produkt.

## 7. F01-Folgewirkung nach vollständigem Rebinding

Erst nach dem gesamten vorgeschriebenen Product/Foundation/Project-Foundation/Epic-Rebinding
darf F01 unter neuer Ausführungsautorisierung fortgesetzt werden.

Der verbleibende F01-Scope bleibt eng:

1. WS-P05-Fallbackgrenze auf Basis bereits vorhandener Windows-/Ubuntu-Evidence abschließend
   qualifizieren, ohne Produktcode zu implementieren;
2. verbleibende Ubuntu Display-/Geometry-/State-Evidence schließen;
3. Cross-OS Measurement-/Memory-/Peak-Methodik fertig qualifizieren.

`TARGET_EQUIVALENT_RESTART` bleibt geschlossen, sofern keine neue gegenteilige Evidence entsteht.

Die Nutzerentscheidung schließt **nicht automatisch**:
- `WINDOWS_DESKTOP`;
- `SPECIAL_NATIVE_GUI_CASES`;
- `MEASUREMENT_FINAL_ATTRIBUTION`.

## 8. Risiko und erforderliche Reviews

Das Delta bleibt mindestens `ELEVATED`, weil es eine gebundene Plattform-/Recovery-Grenze
ändert und spätere Capture-/Restore-Fidelität sowie Nutzerstatus beeinflusst.

Daher gilt:

```text
CRITICAL_PREPARATION_REVIEW
-> INDEPENDENT_TECHNICAL_FOUNDATION_PREPARATION_REVIEW
-> CORRECT_AND_REREVIEW_IF_REQUIRED
-> EXACT_TECHNICAL_FOUNDATION_DELTA_BINDING
-> CODING_AGENT_MATERIALIZES_ONLY_NEEDED_PROJECT_FOUNDATION_DELTA
-> PROJECT_FOUNDATION_READY_FOR_REVIEW
-> INDEPENDENT_PROJECT_FOUNDATION_REVIEW
```

Der Implementierer besitzt keine unabhängige Verdict-Autorität.

## 9. Brownfield-Materialisierungsgrenze

Der spätere Coding-Agent darf nach Exact Binding nur das notwendige Project-Foundation-Delta
materialisieren.

Append-only bleiben:

- `WS-PD-20260917-01` und dessen Approval;
- `WS-PD-DELTA-20260924-01` und dessen Approval;
- `WS-TFP-20260917-01 r6`;
- historische V6-Foundation-Quellen;
- bestehende Project-/Epic-/F01-/Review-Evidenceoriginale.

Zulässige Materialisierungsrichtung:

- neue Product-Delta-/Approval-Locators;
- neue Technical-Foundation-Delta-/Binding-Locators;
- minimale aktive Router-/Guard-Anpassung zur neuen Sonderfenstergrenze;
- erforderliche aktuelle Project-Foundation-Evidence.

Nicht zulässig in diesem Schritt:
- F01-Restqualifikation;
- F02/Product-Code;
- Feature Acceptance;
- Merge von PR #3;
- Release/Signierung/Production;
- Überschreiben historischer gebundener Dateien.

## 10. Nachgelagerter Epic-Pfad

Nur nach `PROJECT_FOUNDATION_REVIEW = PASS`:

```text
WS-E01_EPIC_PREPARATION_DELTA
-> EPIC_PREPARATION_CRITICAL_SELF_REVIEW
-> INDEPENDENT_EPIC_PREPARATION_REVIEW
-> EXACT_EPIC_REBINDING
-> NEW_F01_EXECUTION_AUTHORIZATION
-> F01_REMAINDER_QUALIFICATION
```

Bis dahin bleibt PR #3 Draft/ungemergt und F01 gestoppt.

## 11. Offene materielle Nutzerentscheidungen

```text
OPEN_MATERIAL_USER_DECISIONS: NONE
```

Die noch offenen Fragen sind Review-/Evidence-/Implementierungsfragen innerhalb der bereits
freigegebenen Grenze. Eine neue materielle Nutzerentscheidung wäre nur erforderlich, wenn der
Review oder spätere Evidence eine weitere Product-/Scope-/Security-/Architekturabweichung zeigt.
