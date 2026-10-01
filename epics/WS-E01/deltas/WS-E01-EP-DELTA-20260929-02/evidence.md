# WS-E01 Epic Preparation Delta: Materialisierungs-Evidence und Review-Handoff

Run WS-E01-EPDELTA-MAT-20260929-01 unter WS-EA-20260929-02 (Original byteidentisch als
`execution-authorization.json`, SHA-256 unabhängig im Harness gepinnt). Kein unabhängiger
Verdict, kein Rebinding, keine Ausführungsautorisierung. Basis: main
`1cb82c926903b2fd6b497d008db61c71c5d92aca`. Branch: `prep/ws-e01-delta-20260929-02`.
Subject: `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json`.
Der kanonische Request bindet Subject und Evidence an den vollständigen Commit-SHA;
kein selbstreferenzieller End-SHA in diesem Dokument. End-Head/Tree, PR und CI-URLs
stehen im Delivery-Handoff am PR. Unabhängig genau diese Git-/CI-Objekte verifizieren.

## Preflight vor der ersten Mutation

REPOSITORY_OR_REMOTE_VERIFIED: Root/Origin `felixvonvollmer-png/Firefox---WindowSafe`,
Repository-ID 1374094477, public. Worktree/Index/untracked sauber. Remote-main gleich
Startbasis; der neue Branch existierte weder lokal noch remote. Das lokale `main` stand
veraltet auf `3bdd7439c221b8f8c83e7374c8bb29898891a4fd` (Vorgänger, Fast-Forward-fähig)
und wurde ohne Worktreeänderung auf Remote-main vorgespult. PR #3 offen/Draft/ungemergt,
Head `7d66ca5b025c8f748d7f97b961c496ee450daaa7`; kein F01-Checkout oder -Write.
Gebundene Blobs auf der Basis gelesen: Project-Foundation-Binding
`8a85ff8481a6bd831b3e2ace3382404762476834` (`PROJECT_FOUNDATION_ACCEPTED`),
PASS-Resultat `ff96f8b1cac7d9a664339c7df55ddbf77947e3a8`, Product Delta
`c8d52f1720aa24544b0d24f652e6b9c8d14254ec`, TF Delta
`539dd9d35d40b832c07a779e351e7964af9f8705`, historische Epic-Preparation/-Subject/-Binding
`a92fbe87…`, `f12b4756…`, `930b4c3176a9601e44f7a4b04ff1d4530488b6e1`.
Lokale Basisgates vor Mutation: `check`, 109 Tests, `history` gegen Nullbasis und
`3bdd743…` bestanden (LOCAL_AGENT_REPORTED).

LOCAL_AGENT_REPORTED: Paket-ZIP 27673 Bytes, SHA-256
`deb5a3d4f89cec08bef0685fa636ae48844a52555d0f5c8917a216408e6a4a01`; eine zweite
Downloadkopie war byteidentisch. Elf Member; alle zehn in `SHA256SUMS.json` gelisteten
Dateien erfüllen Bytelänge und SHA-256. Nicht materialisierte Paketdateien (nur Provenienz):
README_FIRST `1775b462…`, Handoff `faa167b3…`, Startprompt `085fdc48…`, Manifest selbst.

## Materialisierung (append-only, Originalbytes)

| Pfad im Delta-Verzeichnis | Original | Bytes | SHA-256 |
|---|---|---|---|
| `preparation.md` | Epic Preparation Delta WS-E01-EP-DELTA-20260929-02 | 13661 | `ddd12e52…2115` |
| `critical-self-review.md` | Critical Self-Review WS-E01-EP-DELTA-CR-20260929-02 | 2872 | `12d1d400…e765` |
| `execution-direction.json` | Nutzerrichtung WS-UD-WS-E01-EXEC-20260929-01 | 1012 | `5b4f467e…a2de` |
| `external-context-sync.json` | Sync-Bestätigung WS-EXTCTX-SYNC-20260929-01 | 1499 | `d4bdc815…2062` |
| `project-description.md` | Synchronisierte V6-Projektbeschreibung | 7607 | `647d8fcf…4ba5` |
| `previous-preparation-delta.md` | Vorheriges Delta WS-E01-EP-DELTA-20260929-01 | 10859 | `e848043b…074f` |
| `execution-authorization.json` | Autorisierung WS-EA-20260929-02 | 6930 | `68ff1012…28ab` |

Vollständige Hashes stehen im Harness (`EPIC_DELTA_ORIGINALS`) und werden bei jedem
`check`/`request` gegen die Bytes geprüft. Die Autorisierung ist zusätzlich materialisiert,
weil der bestehende Harness für jede neue Preparation einen eigenen, vom Subject
unabhängigen Vertrauensanker verlangt; ohne ihn wäre der Subject selbstzertifizierend.
Neu verfasst: `subject.json`, `binding.json` (REVIEW_REQUIRED, `ready_for_agent: false`)
und dieses Dokument.

## Harness-Delta (minimal, fail-closed)

KEEP: kanonischer V3-Vertrag `reviews/review-contract.json`, Rolle
`INDEPENDENT_EPIC_PREPARATION_REVIEWER`, historischer Epic-Request (liefert weiter den
reviewed Request am `644b81f63dcc1990bc894a9c2c9bd8dc24a98c04`), Foundation-Acceptance,
kumulative Historyprüfung, alle bisherigen Tests.

ADD: genau ein zusätzlicher Subject-Locator. `request` akzeptiert
`EPIC_PREPARATION_REVIEW` nur an diesem exakten Pfad außerhalb der bisherigen
`epics/<ID>/subject.json`-Regel; jeder andere verschachtelte Pfad fällt weiter auf
`subject locator mismatch`. `scope()` erlaubt nur die zehn exakten Delta-Dateien.
Der Subject und das Binding werden feldgenau (inklusive JSON-Typen) gegen feste
Pre-Review-Werte geprüft; ein Accepted-/READY-Übergang existiert bewusst nicht.
Gepinnte Git-Blobs: historische Epic-Dateien, Foundation-Binding/-PASS, Product/TF-Delta.

Notwendige Anpassung des Foundation-Guards: Die Acceptance-Prüfung des Foundation-Deltas
verlangte, dass sich nach `bbca750…` nur Integrationspfade ändern. Sie prüft jetzt,
wenn und nur wenn der exakte Epic-Delta-Subject vorhanden ist, die Strecke
`bbca750…..1cb82c9…` unverändert vollständig und die Fortsetzung `1cb82c9…..HEAD`
separat: keine Merges, pro Commit exakte Pfad-Allowlist, Append-only-Schutz, erneute
Original-/Blobprüfung. Ohne den Subject bleibt das bisherige Verhalten bitgleich.
CI führt den neuen Request unbedingt aus; `check` erzwingt diese Zeile.

Risiko ELEVATED: betrifft Review-/Lifecycle-Routing und Recovery-/Plattformgrenzen
(WS-P05). Unabhängiger `EPIC_PREPARATION_REVIEW` erforderlich. Kein Produktcode,
Browser-/Profilzugriff, Provider, Dependency- oder Toolchainwechsel.

## Global Guidance

REPOSITORY_OR_REMOTE_VERIFIED: `felixvonvollmer-png/projektbeschreibung-und-geruest`
main `47816eecb9df524aa1d91d564496dea5bc4b94b7`; Router `docs/guidance/README.md`
Blob `6533828691dd918dc9303b216d78bed616364fd2`; Route AI_AGENT
`docs/ai_agent_playbook.md` Blob `58d80fe4e45bd64667df92769cbd23654e2a55e2`
(nur §1, §7–9, §11, §13 gelesen). Angewendet: exakter Pfad-Freeze, weil die
Dateigrenze hier Teil der Review-/Governance-Eigenschaft ist; ein Writer, keine
Delegation (AGENTS.md). Keine Governance- oder Scope-Autorität aus der Guidance.

## Verifikation

Lokale Pflichtbefehle am committed Head (LOCAL_AGENT_REPORTED; Resultate im Handoff):

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build --verify-repeat
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/subject.json
python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json
python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca
git diff --check
```

Neue Regressionen in `tests/test_epic_delta.py`: positiver Request/Check/History auf
synthetischer Fortsetzung; Ablehnung zweiter Delta-Pfade, Subject-/Pfad-/Epic-Mismatch,
historischer Subject-/Binding-/Preparation-Mutation (auch mit späterem Revert),
READY vor Review, offener Entscheidung, falscher Foundation-/Sync-/Product-/TF-Referenz,
F01-/Produktstart-Claims, Out-of-Scope-Dateien, Merges in der Fortsetzung und einer
Fortsetzung ohne Basis-Ancestry. CI_VERIFIED erst mit abgeschlossenem Exact-Head-Run.

## Kritische Eigenprüfung und offene Punkte

- NIT (offen, nichtblockierend): Die Autorisierung nennt den historischen Binding-Blob
  mit 38 statt 40 Zeichen (`930b4c3176a9601e44f7a4b04ff1d4530488b6`). Präfix stimmt;
  das Delta-Original nennt den vollständigen Wert, der Harness pinnt ihn. Autorisierungsbytes
  bleiben unverändert.
- Das angenommene Foundation-Binding enthält weiterhin `external_project_context_sync:
  PENDING` und das alte `next_gate`. Es ist exakt gebunden und append-only; der Sync wird
  durch den separaten Record `external-context-sync.json` gebunden, nicht durch Überschreiben.
- Der Sync beruht auf der Nutzerbestätigung „ok sie ist drin“; die ChatGPT-Projekt-UI wurde
  hier nicht geprüft (Grenze aus dem Original übernommen).
- Offene materielle Nutzerentscheidungen: keine.

## Stop

`EPIC_PREPARATION_DELTA_READY_FOR_REVIEW` bei grünen lokalen Gates und grüner
Exact-Head-CI. Danach bereitet der Project-LLM den frischen unabhängigen Epic Preparation
Review vor. Kein Merge, kein Rebinding, keine breite WS-E01-Autorisierung, keine
F01-Fortsetzung, kein F02, keine Feature Acceptance, kein Release/Production.
