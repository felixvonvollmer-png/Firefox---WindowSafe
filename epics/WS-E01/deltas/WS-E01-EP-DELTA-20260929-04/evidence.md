# WS-E01 Epic Preparation Delta, zweite Korrektur: Evidence und Rereview-Handoff

Run WS-E01-EPDELTA-CORR-20260929-02 unter WS-EA-20260930-01 (`execution-authorization.json`,
SHA-256 unabhängig im Harness gepinnt). Materializer
`CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_02`; Project-LLM-Implementer laut Nutzerentscheidung
`PROJECT_LLM_WS_E01_EP_DELTA_20260929_04`. Kein unabhängiger Verdict, kein Self-PASS.
Basis main `1cb82c926903b2fd6b497d008db61c71c5d92aca`; Start-Head (reviewed -03)
`dee7ab5c9c5b53accd8602105e87523510582e40`, Tree `a62713f6d34c054d3064d0d6d999fbcc9cd694d3`.
Branch `prep/ws-e01-delta-20260929-02`, PR #5. End-SHA nur über den kanonischen Request;
End-Head/Tree und CI-URLs im Delivery-Handoff am PR.

## Autorisierung und Provenienzgrenze

WS-EA-20260930-01 ist eine strukturierte Aufzeichnung direkter Nutzerentscheidungen aus der
Claude-Code-Sitzung vom 2026-09-30 durch den Materializer, mit wörtlichen Auszügen. Sie ist
kein Project-LLM-Original und nicht bytegleich mit den Chatnachrichten. Eine separate
Project-LLM-Korrekturschrift für -04 existiert nicht; die Korrekturrichtung stammt aus der
Disposition von WS-E01-EPR-DELTA-20260929-03-F01 und der Nutzerentscheidung.

## Preflight vor der ersten Mutation

REPOSITORY_OR_REMOTE_VERIFIED: HEAD = Remote-Branch = PR-#5-Head `dee7ab5…`, Tree `a62713f…`,
main `1cb82c9…`, Worktree/Index/untracked sauber (ignoriert: `.claude/`, `build/`,
`qualification/`, Caches). PR #3 Draft/offen bei `7d66ca5b025c8f748d7f97b961c496ee450daaa7`.
Die in der Vorkorrektur vollständig gelesenen vier Pflichtquellen sind unverändert
(Blobs wie in -03; der Harness prüft sie erneut).

## Reviewresultate zum Subject -03@dee7ab5 (append-only)

| Resultat | Bytes | SHA-256 | Verdict | Provenienz |
|---|---|---|---|---|
| `reviews/results/WS-E01-EPR-DELTA-20260929-02.json` | 14361 | `dd3cc147…dfa8` | BLOCKED | exaktes Original (zwei identische Downloadkopien) |
| `reviews/results/WS-E01-EPR-DELTA-20260930-04.json` | 14038 | `3096a1fe…49cf` | CORRECTION_REQUIRED | `RECONSTRUCTED_FROM_REVIEW_TRANSCRIPT` |

Beide vor Mutation mit `validate-result` am unveränderten Head `dee7ab5…` geprüft: Exit 0.
Das ursprüngliche Original WS-E01-EPR-DELTA-20260929-03 (19012 Bytes, `e4ab16e7…6edd`) lag
nur unter `/tmp` und ging bei einem Neustart verloren. Es wurde vom Coding-Agenten weder
rekonstruiert noch ersetzt; die Ersatz-Evidence wurde vom Nutzer bereitgestellt und
autorisiert und erklärt ihre Rekonstruktion selbst in `reviewer` und `provenance`.

BLOCKED-F04 (Reviewer ohne exakten Checkout) verlangt keine Subject-Korrektur; der nächste
Rereview läuft in einem sauberen lokalen Checkout des End-SHA.

## Finding WS-E01-EPR-DELTA-20260929-03-F01 (MAJOR): Fehlerklasse geschlossen

Ursache: -03 band eine manuell gepflegte Ausschlussliste; die unverändert übernommene -02-
Preparation mit Autorin `PROJECT_LLM_WS_E01_EP_DELTA_20260929_02` fehlte darin.

Korrektur: `review_exclusion_closure` (Harness) leitet die Ausschlussmenge mechanisch ab. Ab dem
Subject folgt sie jeder semantischen Referenz (alle Stringwerte außer `evidence_paths`) in einen
`epics/`-Namespace zum besitzenden Epic-Preparation-Subject, transitiv, und sammelt dort
`implementer`, `materializer` und die gebundenen `review_excluded_identities` der Vorgänger
(die eigene Liste des geprüften Subjects ist nie Quelle der Ableitung). Ein Mutationstest mit
nicht-transitiver Ableitung lässt 12 Lineage-Tests scheitern. Reine
Product-/Foundation-/Reviewinputs (`foundation/…`, `reviews/…`) und bloße Evidence sind keine
Autorenschaft. Keine feste Kardinalität. `request` und `check` scheitern mit
`REQUEST_INVALID: review exclusion closure incomplete`, wenn eine abgeleitete Identität fehlt.

Abgeleitete Linie für -04 (identisch mit dem autorisierten Minimum, keine Zusatzidentität):

| Identität | Quelle in der Linie |
|---|---|
| `PROJECT_LLM_WS_E01_EP_DELTA_20260929_04` | -04 `implementer` |
| `CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_02` | -04 `materializer` |
| `PROJECT_LLM_WS_E01_EP_DELTA_20260929_03` | -03 via `superseded_subject` |
| `CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_01` | -03 `materializer` |
| `PROJECT_LLM_WS_E01_EP_DELTA_20260929_02` | -02 via `epic_preparation_delta_reference` u. a. |
| `CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01` | -02 `materializer` |
| `PROJECT_LLM_WS_E01_PREPARATION_20260919_01` | historische WS-E01-Preparation via `historical_epic_preparation` |

Die historische WS-E01-Preparation (Materialisierung WS-E01-MAT-20260919-01) nennt keinen
Materializer als Feld; es wird keine Identität erfunden. `validate-result` und Sidecar prüfen
unverändert Vollgleichheit nach Rand-Whitespace-/Case-Normalisierung, keine Teilstrings.

## Routing-Ausrichtung (WS-EA-20260930-01)

KEEP: Repository als System of Record, Git-Preflight, benannte Pfade, kein History-Rewrite,
kein Gate-Abschwächen, historische Originale append-only, keine Production.
SIMPLIFY: Toolchainregel an TF ausgerichtet (kein Drift in Review-/Correction-Transporten;
nach gültigem Epic Rebinding JIT innerhalb Product Truth/TF). REMOVE_FROM_ACTIVE_ROUTING:
pauschales „Keine Agentendelegation“; ersetzt durch JIT-Worker/Reviewer im gebundenen Scope,
unabhängige Verdicts nur aus frischem/isoliertem Kontext, kein Self-PASS. Geändert nur
lebende Router (`AGENTS.md`, `foundation/engineering.md`); historische Dateien unverändert.

## Harness-/History-Grenze

- Genau ein weiterer Locator; Commits nach `dee7ab5…` nur in der -04-Allowlist (vier -04-Dateien,
  zwei Resultate, Router/Harness/Tests/CI). -02/-03-Namespaces und das -01-Resultat bleiben
  bytegleich zum reviewed Head und außerhalb der Allowlist.
- Alter -03-Locator liefert bei vorhandenem -04 den Request am `dee7ab5…` (45 Einträge), -02 am
  `48d7b0f…` (35 Einträge). Beliebige weitere Delta-Pfade bleiben gesperrt; keine Merges.
- Binding REVIEW_REQUIRED feldgenau; kein READY-/Rebinding-Übergang vor PASS.

Risiko ELEVATED (Review-/Lifecycle-Guard). Kein Produktcode, keine Dependency-/Toolchain-
Änderung, kein Browser-/Profilzugriff, keine Vertragsänderung.

## Verifikation

In einem sauberen Checkout des committed Head (LOCAL_AGENT_REPORTED; Resultate im Handoff):

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build --verify-repeat
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json
python3 tools/foundation.py request --sha HEAD --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json
python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json
python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca
git diff --check
```

Regressionen in `tests/test_epic_lineage.py`: jede abgeleitete Identität (inklusive Case-/
Whitespace-Varianten) wird als Reviewer und Sidecar-Autor abgelehnt; längere Identitäten mit
Teilstring bleiben zulässig; Entfernen jeder abgeleiteten Identität lässt `request` und `check`
scheitern; eine neu in die Linie eingebrachte Autorenidentität wird ohne Ausschluss abgewiesen;
alte Namespaces bytegleich; alte Requests reproduzierbar; beliebig viele Resultate zulässig.

## Offene Punkte

- NIT WS-E01-EPR-DELTA-20260929-03-N01 (nichtblockierend): `files()` sieht git-ignorierte lokale
  Agentenkonfiguration. Kanonische Prüfung im sauberen Checkout; keine Guard-Abschwächung.
- Materielle Nutzerentscheidungen: keine.

## Stop

Rereview-bereit bei grünen lokalen Gates und grüner Exact-Head-CI. Rebinding, Merge und breite
WS-E01-Autorisierung erst nach unabhängigem PASS.
