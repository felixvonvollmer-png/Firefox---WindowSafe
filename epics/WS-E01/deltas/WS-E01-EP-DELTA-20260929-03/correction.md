# WindowSafe — WS-E01 Epic Preparation Correction

```text
DOCUMENT_TYPE: EPIC_PREPARATION_REVIEW_CORRECTION
CORRECTION_ID: WS-E01-EP-CORR-20260929-02
EPIC_ID: WS-E01

SOURCE_SUBJECT_ID: WS-E01-EP-DELTA-20260929-02
SOURCE_SUBJECT_PATH: epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json
SOURCE_SUBJECT_END_SHA: 48d7b0f97eacecd7515f7cbf064955303b0d5767
SOURCE_SUBJECT_TREE: 3393b5c6de0dd0c11988b702ca602698f736e290
SOURCE_REVIEW_ID: WS-E01-EPR-DELTA-20260929-01
SOURCE_REVIEW_VERDICT: CORRECTION_REQUIRED
SOURCE_REVIEW_BYTES: 13760
SOURCE_REVIEW_SHA256: e438cc1fba49bc472e78adbf4b12aa9475e24c2dac0cd187c8a29c5682f16048

CORRECTED_SUBJECT_ID: WS-E01-EP-DELTA-20260929-03
CORRECTED_SUBJECT_PATH: epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json
CORRECTION_BASE_HEAD: 48d7b0f97eacecd7515f7cbf064955303b0d5767
CURRENT_CANONICAL_MAIN: 1cb82c926903b2fd6b497d008db61c71c5d92aca

PRODUCT_TRUTH_CHANGE: NONE
TECHNICAL_FOUNDATION_CHANGE: NONE
EPIC_PRODUCT_SCOPE_CHANGE: NONE
MATERIAL_USER_DECISION_REQUIRED: NONE

F01_CONTINUATION_AUTHORIZED: NO
EXACT_EPIC_REBINDING_AUTHORIZED: NO
BROAD_WS_E01_EXECUTION_AUTHORIZED: NO
```

## 1. Zweck und Korrekturgrenze

Der unabhängige `EPIC_PREPARATION_REVIEW` des Subjects `WS-E01-EP-DELTA-20260929-02` hat
`CORRECTION_REQUIRED` ergeben: ein OPEN MAJOR im mechanischen Self-Verdict-Guard und
zwei OPEN MINOR zur Locator-/Preflight-Provenienz.

Die fachliche WS-P05-/WS-E01-Preparation bleibt unverändert. Die Korrektur ist rein
Review-/Harness-/Provenienz-bezogen. Der alte Subject/Head sowie das Revieworiginal bleiben
append-only historische Evidence. Die Korrektur erzeugt einen neuen exakten Subject
`WS-E01-EP-DELTA-20260929-03` und danach einen frischen unabhängigen Rereview.

## 2. Finding F01 — MAJOR: vollständiger mechanischer Self-Verdict-Ausschluss

Der alte Subject hatte:
- Project-LLM-Autor `PROJECT_LLM_WS_E01_EP_DELTA_20260929_02`;
- Materializer `CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01`.

Der alte kanonische Request transportierte nur `implementer`; dadurch konnte der Materializer
mechanisch als Revieweridentität passieren.

### Pflichtkorrektur

Der korrigierte Subject muss eine explizite, mechanisch gebundene Ausschlussmenge enthalten:

```text
review_excluded_identities:
- PROJECT_LLM_WS_E01_EP_DELTA_20260929_03
- CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01
- CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_01
```

Begründung: Der Rereview umfasst sowohl die bereits materialisierten Harness-/Routing-Änderungen
des alten Materializers als auch die Korrekturänderungen des neuen Materializers. Beide
Coding-Agent-Autoren sowie der Project-LLM-Autor des korrigierten Subjects sind daher
review-ausschließend.

Der Harness muss:

1. für genau den korrigierten Subject diese vollständige Ausschlussmenge in den kanonischen
   Review-Request transportieren;
2. `reviewer.identity` case-insensitiv gegen **jede** Identität der Menge ablehnen;
3. für historische Requests ohne dieses Feld die bestehende Semantik unverändert erhalten;
4. externe Provenienz-/Unabhängigkeitsprüfung zusätzlich beibehalten;
5. Negativtests für Project-LLM-, alten Materializer- und neuen Korrektur-Materializer-Self-Review
   enthalten sowie einen positiven Test für eine andere, sonst gültige unabhängige Identität.

Die mechanische Equality-Prüfung ersetzt keine externe Authentifizierung; sie ist ein
zusätzlicher Fail-Closed-Guard.

## 3. Finding F02 — MINOR: vollständiger historischer Binding-Blob

Das immutable Original `WS-EA-20260929-02` bleibt unverändert. Sein 38-stelliger Wert wird
nicht rückwirkend korrigiert.

Der neue Korrektur-/Superseding-Record bindet stattdessen vollständig:

```text
PATH: epics/WS-E01/binding.json
GIT_BLOB: 930b4c3176a9601e44f7a4b04ff1d4530488b6e1
```

Dieser vollständige Locator ersetzt den verkürzten Wert **nur für den Korrektur- und
Rereviewpfad**. Künftige mechanische Prüfung des korrigierten Subjects darf sich nicht auf den
verkürzten Wert stützen.

## 4. Finding F03 — MINOR: Pflichtreads vor erster Mutation

Vor **jedem Repository-Write** des Korrekturlaufs muss der Coding-Agent tatsächlich lesen:

- `foundation/architecture.md` — Blob `923c8e5820067376f3ea6660bf0307e7bfaa9d6a`;
- `foundation/sources/v6-final-20260918/README.md` — Blob `c9c0a47d108268059ca5b5825d2d445b44179775`;
- `foundation/sources/v6-final-20260918/foundation-1.md` — Blob `0c10e10eebcb2b23336cc9cdf4a88305a209fd22`;
- `foundation/sources/v6-final-20260918/foundation-2.md` — Blob `3034da0fbee6ab79318da25ed65ccdc0933074e5`.

Die Delivery-Evidence muss diese tatsächlichen Reads ausweisen.

`foundation/architecture.md` wird im korrigierten Subject zusätzlich in die kanonischen
`evidence_paths` aufgenommen. Die drei finalen V6-Dateien bleiben ebenfalls Evidence.

## 5. Exaktes CORRECTION_REQUIRED-Original

Vor erster Repository-Mutation muss der Korrekturagent die Paketdatei
`WS-E01-EPR-DELTA-20260929-01.json` prüfen:

```text
bytes: 13760
sha256: e438cc1fba49bc472e78adbf4b12aa9475e24c2dac0cd187c8a29c5682f16048
```

und anschließend mit dem kanonischen `validate-result` gegen das alte Subject
`WS-E01-EP-DELTA-20260929-02@48d7b0f97eacecd7515f7cbf064955303b0d5767` konsumieren. Fehler => STOP.

Erst nach erfolgreichem Konsum darf der Agent die **exakt unveränderten Bytes** nach

`reviews/results/WS-E01-EPR-DELTA-20260929-01.json`

übertragen. Keine Rekonstruktion, kein Reformatting, keine Umdeutung.

## 6. Neuer korrigierter Subject

Append-only unter:

`epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/`

Der alte Namespace `WS-E01-EP-DELTA-20260929-02` bleibt vollständig unverändert.

Der neue Subject bindet:
- die fachlich unveränderte Epic Preparation Delta v2;
- dieses Korrekturdokument;
- das exakte `CORRECTION_REQUIRED`-Revieworiginal;
- den neuen Korrektur-/Execution-Authorization-Record;
- WS-P05, TF-Delta, Project-Foundation-PASS, bestätigten Project-Context-Sync und Nutzerrichtung;
- `foundation/architecture.md` und die finalen V6-Quellen;
- die vollständige `review_excluded_identities`-Menge;
- korrigierte Harness-/Test-/CI-Evidence.

Pre-review bleibt:

```text
STATUS: EPIC_PREPARATION_DELTA_READY_FOR_REVIEW
INDEPENDENT_REVIEW_STATUS: PENDING
BINDING: REVIEW_REQUIRED
READY_FOR_AGENT: false
EXACT_EPIC_REBINDING: PENDING
F01_CONTINUATION_AUTHORIZED: false
BROAD_WS_E01_EXECUTION_AUTHORIZATION: NOT_CREATED
```

## 7. Harness-/History-Grenze

Kein generischer Nested-/Multi-Delta-Bypass.

Der Harness darf exakt:
- `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json` als historischen Correction-Required-Subject erhalten;
- `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json` als aktuellen Rereview-Subject erkennen.

History-/Scope-Guards müssen:
- `48d7b0f97eacecd7515f7cbf064955303b0d5767` und alle alten Delta-Dateien unverändert erhalten;
- ausschließlich die separat autorisierte lineare Korrekturfortsetzung zulassen;
- **keinen Merge** im Korrekturabschnitt zulassen;
- historische Epic-/Foundation-/Revieworiginale schützen;
- den bytegenauen `CORRECTION_REQUIRED`-Reviewtransfer append-only erlauben;
- keine READY-/Rebinding-Transition vor Rereview-PASS zulassen.

## 8. Mindesttests

- korrigierter Request enthält exakt die drei `review_excluded_identities`;
- `PROJECT_LLM_WS_E01_EP_DELTA_20260929_03` als Reviewer => reject;
- `CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01` als Reviewer => reject;
- `CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_01` als Reviewer => reject;
- andere unabhängige Revieweridentität bei sonst gültigem Payload => zulässig;
- historische Requests/Resultate bleiben kompatibel;
- fehlende/zusätzliche/falsche Ausschlussidentität im korrigierten Subject => reject;
- verkürzter historischer Binding-Blob im neuen Korrekturrecord => reject;
- fehlendes `foundation/architecture.md` in neuer Review-Evidence => reject;
- Mutation alter `WS-E01-EP-DELTA-20260929-02`-Dateien => reject;
- beliebiger anderer Nested-/Delta-Pfad => reject;
- Merge im Korrekturabschnitt => reject.

## 9. Rereview

Nach grünem korrigiertem Exact Head:

```text
EPIC_PREPARATION_DELTA_CORRECTED_READY_FOR_REREVIEW
-> FRESH INDEPENDENT_EPIC_PREPARATION_REVIEW
-> PASS | CORRECTION_REQUIRED | BLOCKED
```

Ein späteres PASS erzeugt noch keine F01-Ausführungsautorität.

## 10. Stop

Bis zum erfolgreichen Rereview:
- kein Merge von PR #5;
- kein Exact Rebinding;
- keine breite WS-E01-Ausführungsautorisierung;
- keine F01-Fortsetzung;
- kein F02/Product-Code;
- keine Feature Acceptance;
- kein Release/Production.
