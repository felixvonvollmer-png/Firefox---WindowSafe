# WS-E01 Epic Preparation Delta Korrektur: Evidence und Rereview-Handoff

Run WS-E01-EPDELTA-CORR-20260929-01 unter WS-EA-20260929-03 (Original byteidentisch als
`execution-authorization.json`, SHA-256 unabhängig im Harness gepinnt). Materializer
`CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_01`. Kein unabhängiger Verdict, kein Merge,
kein Rebinding, keine Ausführungsautorisierung. Basis main
`1cb82c926903b2fd6b497d008db61c71c5d92aca`; Start-Head (CORRECTION_REQUIRED-Subject)
`48d7b0f97eacecd7515f7cbf064955303b0d5767`, Tree `3393b5c6de0dd0c11988b702ca602698f736e290`.
Branch `prep/ws-e01-delta-20260929-02`, PR #5. Neuer Subject:
`epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json`. Der End-SHA stammt aus dem
kanonischen Request; kein selbstreferenzieller Head in diesem Dokument. End-Head/Tree und
CI-URLs stehen im Delivery-Handoff am PR.

## Preflight vor der ersten Mutation

REPOSITORY_OR_REMOTE_VERIFIED: Origin `felixvonvollmer-png/Firefox---WindowSafe`,
Repository-ID 1374094477. Remote-main `1cb82c9…`, lokaler Head = Remote-Branch = PR-#5-Head
`48d7b0f…` (offen, ungemergt), Tree `3393b5c…`, genau ein Commit vor main.
Worktree, Index und untracked sauber (nur ignorierte `build/`, `qualification/`, Caches).
PR #3 Draft/offen/ungemergt, Head `7d66ca5b025c8f748d7f97b961c496ee450daaa7`; kein
F01-Checkout oder -Write. Der Zustand wurde unmittelbar vor dem ersten Write erneut geprüft.

LOCAL_AGENT_REPORTED: Paket-ZIP 20987 Bytes, SHA-256
`e08bd90dd4e9f9b40bb6ba3219925252192c86dddcfe9b759ce26cc3371c1ec5`; alle acht in
`SHA256SUMS.json` gelisteten Dateien erfüllen Bytelänge und SHA-256. Nicht materialisiert
(nur Provenienz): README_FIRST `21dec43a…`, Handoff `48ded2d7…`, Startprompt `a05b5b9c…`,
Manifest selbst `2ad36772…`.

## Pflicht-Reads vor dem ersten Write (Finding F03)

Vor jeder Repository-Mutation wurden alle vier Quellen am Head `48d7b0f…` vollständig
gelesen (LOCAL_AGENT_REPORTED) und ihre Blobs sowohl über `git rev-parse HEAD:<pfad>` als
auch `git hash-object` bestätigt (REPOSITORY_OR_REMOTE_VERIFIED):

| Pfad | Git-Blob | Bytes |
|---|---|---|
| `foundation/architecture.md` | `923c8e5820067376f3ea6660bf0307e7bfaa9d6a` | 7748 |
| `foundation/sources/v6-final-20260918/README.md` | `c9c0a47d108268059ca5b5825d2d445b44179775` | 6377 |
| `foundation/sources/v6-final-20260918/foundation-1.md` | `0c10e10eebcb2b23336cc9cdf4a88305a209fd22` | 38421 |
| `foundation/sources/v6-final-20260918/foundation-2.md` | `3034da0fbee6ab79318da25ed65ccdc0933074e5` | 43439 |

Relevante Schlussfolgerungen: F1 §27 / F2 §34 (Verdict-Autorität getrennt vom
Implementierer), F2 §32 (Konsum fail-closed gegen Subject/Evidence/Authority), F1 §18 /
F2 §17 (Pflichtkorrektur = neuer exakter Subject + Rereview), Architektur WS-ADR-003
(Strukturprüfung authentifiziert keine Person). Kein weiterer Widerspruch gefunden.
Alle vier Pfade sind kanonische Evidence des neuen Subjects; der Harness prüft ihre Blobs
gegen `MANDATORY_PREWRITE_READS` der Autorisierung.

## Konsum des CORRECTION_REQUIRED-Originals vor Mutation

Paketdatei `WS-E01-EPR-DELTA-20260929-01.json`: 13760 Bytes, SHA-256
`e438cc1fba49bc472e78adbf4b12aa9475e24c2dac0cd187c8a29c5682f16048`, byteidentisch mit der
separaten Downloadkopie. `python3 tools/foundation.py validate-result --file <paketdatei>`
am unveränderten Head `48d7b0f…` mit CPython 3.14.4: `VALIDATE-RESULT OK`. Verdict
`CORRECTION_REQUIRED`, Subject `WS-E01-EP-DELTA-20260929-02@48d7b0f…`. Erst danach wurden
dieselben Bytes unverändert nach `reviews/results/WS-E01-EPR-DELTA-20260929-01.json`
übertragen. Die Originalfindings bleiben dort OPEN; ihre Schließung ist Sache des Rereviews.

## Materialisierung (append-only, Originalbytes)

| Pfad im Korrekturverzeichnis | Original | Bytes | SHA-256 |
|---|---|---|---|
| `correction.md` | Korrektur WS-E01-EP-CORR-20260929-02 | 8551 | `aee88ae8…7b3e` |
| `correction-disposition.json` | Disposition WS-E01-EP-CORR-DISP-20260929-02 | 2385 | `9f268ea3…c1aa` |
| `correction-critical-self-review.md` | Self-Review WS-E01-EP-CORR-CR-20260929-02 | 1945 | `30254913…0692` |
| `execution-authorization.json` | Autorisierung WS-EA-20260929-03 | 7254 | `1672b457…6ef` |

Neu verfasst: `subject.json`, `binding.json` (REVIEW_REQUIRED, `ready_for_agent: false`) und
dieses Dokument. Die fachliche Epic-/Product-/TF-Aussage ist unverändert: der neue Subject
referenziert Preparation, Self-Review, Sync, Beschreibung und Nutzerrichtung weiterhin im
unveränderten Verzeichnis `WS-E01-EP-DELTA-20260929-02` und bindet den alten Subject samt
Reviewresultat als `superseded_subject`. Der alte Namespace wurde nicht verändert.

## Schließung der drei Findings (mechanisch; Urteil beim Rereview)

**F01 (MAJOR, Self-Verdict):** Subject und Binding binden `review_excluded_identities` =
Project-LLM-Autor, ursprünglicher Materializer und Korrektur-Materializer, exakt gleich der
Autorisierung. `request()` transportiert diese Menge nur für den korrigierten Locator; für
jeden anderen Subject ist das Feld unzulässig. `validate_result()` und die V1-Sidecar-Prüfung
lehnen `reviewer.identity` ab, wenn sie nach `strip().casefold()` einer ausgeschlossenen
Identität gleicht. Requests ohne das Feld behalten die unveränderte Implementer-Regel.
Gleichheit statt Teilstring, weil legitime Reviewer ausgeschlossene Namen zitieren dürfen
(das CORRECTION_REQUIRED-Original tut das). Der Guard ersetzt keine externe Provenienz-/
Unabhängigkeitsprüfung; `FRESH_OR_SUFFICIENTLY_ISOLATED` bleibt Pflicht.

**F02 (MINOR, Locator):** WS-EA-20260929-03 bindet
`epics/WS-E01/binding.json` → `930b4c3176a9601e44f7a4b04ff1d4530488b6e1`. Subject und
Binding tragen `historical_epic_binding_git_blob` mit genau diesem Wert; der Harness verlangt
Gleichheit mit Autorisierung, Pin und tatsächlichem Blob. Verkürzte Werte werden abgelehnt.
WS-EA-20260929-02 bleibt mit seinem verkürzten Wert unverändert historisch.

**F03 (MINOR, Pflicht-Reads):** siehe oben; `foundation/architecture.md` und die drei
finalen V6-Quellen sind Pflicht-Evidence des neuen Subjects (45 Evidence-Pfade).

## Harness-/History-Grenze

- `request` für den alten Locator liefert bei vorhandener Korrektur den unveränderten
  Request am `48d7b0f…` (historischer CORRECTION_REQUIRED-Subject, 35 Evidence-Bindungen).
- Die Epic-Delta-Fortsetzung bleibt linear und mergefrei. Commits bis `48d7b0f…` prüfen
  weiter die alte Allowlist; danach gilt nur die Korrektur-Allowlist (neue Korrekturdateien,
  exaktes Reviewresultat, Router/Harness/Tests/CI). Der alte Namespace liegt außerhalb
  dieser Allowlist und ist zusätzlich append-only sowie bytegleich zum reviewed Head.
- Genau diese zwei versionierten Epic-Locators; jeder andere Delta-Pfad bleibt gesperrt.
- Kein READY-/Rebinding-Übergang; Binding feldgenau REVIEW_REQUIRED.

Risiko ELEVATED (Review-/Lifecycle-Guard). Kein Produktcode, Browser-/Profilzugriff,
Provider, Dependency- oder Toolchainwechsel, keine Änderung am V3-Reviewvertrag.

## Verifikation

Pflichtbefehle am committed Head (LOCAL_AGENT_REPORTED; Resultate im Handoff):

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build --verify-repeat
python3 tools/foundation.py validate-result --file reviews/results/WS-E01-EPR-DELTA-20260929-01.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json
python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json
python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca
git diff --check
```

Neue Regressionen in `tests/test_epic_correction.py`: exakte Ausschlussmenge im Request;
Ablehnung aller drei Autorenidentitäten (auch andere Großschreibung/Whitespace) im Resultat
und Sidecar; positiver Fall mit anderer Identität; unveränderte historische Requests;
fehlende/zusätzliche/falsche Ausschlussidentität, verkürzter Blob, fehlende Architektur-
Evidence, Mutation alter Delta-Dateien (auch mit Revert), anderer Delta-Pfad und Merge in der
Korrekturstrecke werden abgelehnt. CI_VERIFIED erst mit abgeschlossenem Exact-Head-Run.

## Offene Punkte

- Materielle Nutzerentscheidungen: keine.
- Das angenommene Foundation-Binding enthält weiter historisch `external_project_context_sync:
  PENDING`; der Sync bleibt über den separaten Record im alten Namespace gebunden.

## Stop

`EPIC_PREPARATION_DELTA_CORRECTED_READY_FOR_REREVIEW` bei grünen lokalen Gates und grüner
Exact-Head-CI. Danach bereitet der Project-LLM den frischen unabhängigen Rereview vor.
Kein Merge, kein Rebinding, keine breite WS-E01-Autorisierung, keine F01-Fortsetzung,
kein F02, keine Feature Acceptance, kein Release/Production.
