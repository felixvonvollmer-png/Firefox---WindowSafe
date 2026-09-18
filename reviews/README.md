# Kanonischer Reviewkanal und Foundation-Handoff

## Nächster Auftrag: PROJECT_FOUNDATION_REVIEW

Subject-ID **WS-HC-20260917-01**. Subject-Locator: `foundation/subject.json`
an dem **vollständigen End-SHA aus dem Coding-Agent-Handoff**. Den SHA einmal
read-only gegen `fix/ws-hc-20260917-01` und PR-Head verifizieren; `main` muss weiter
auf `4ba2c473fe4d90c85d94ee2b2f5cc5777d115109` liegen. Danach ausschließlich diesen Commit
reviewen. Der Subject enthält bewusst keinen selbstreferenziellen Commit-Hash.

Kontext: `foundation/context.md`, exakte Product-/Approval-/Preparation-/Binding-
und Execution-Inputs, `foundation/sources/foundation-2.md` und Foundation 1.
Evidence: `foundation/evidence/harness-correction.md`, Korrektur-Preflight und die im Subject
genannten Dateien; Tests/Guards selbst prüfen. CI-Run für exakt diesen head_sha
über GitHub Actions lesen. Keine Browserprofile, Produktimplementation oder
Subjectänderung während des Reviews. Das ist ein Reviewauftrag, kein Verdict.

Der unabhängige Reviewer prüft Product Fidelity, harte Invarianten, Architektur,
Harness, Traceability, reproduzierbare lokale/CI-Evidence, Scope, Security,
Reviewvertrag und langlebigen Kontext. Agentenclaims nicht ungeprüft übernehmen.
Der gezielte Review prüft beide Korrekturen, den unveränderten Reviewtransfer,
V1/V2-Verträglichkeit und Tests/CI am neuen Head. Unveränderte Bereiche dürfen über
den historischen PASS referenziert werden. Externe Finding-Closure ist noch offen.
PASS erfordert keine offenen Critical/Blocking/Major; BLOCKED benötigt passende
Rebindung statt verdecktem Korrekturloop. Findingsfreiheit wird nicht vorgegeben.

## Vertragsformat und Preflight

Autoritativer vollständiger Outputvertrag ist `reviews/review-contract.json` am
Subject-SHA. Er ist ein expliziter WindowSafe-Vertrag, **kein JSON-Schema-Dialekt**.
Das Feld `semantic_minimum_mapping` bindet alle Mindestfelder aus Foundation 2 §32.
Alle Objekte haben genau die dort angegebenen Felder; zusätzliche Felder sind
unzulässig. Neue Resultate verwenden `schema_version: 2` passend zu
`contract_version: 2` / `WINDOWSAFE_REVIEW_CONTRACT_V2`. SHA ist ein voller Git-SHA-1,
Evidencehash ein SHA-256. IDs enthalten nur Buchstaben, Ziffern, `_` oder `-`.
Alle sonstigen Textfelder sind nichtleer, `findings` darf leer sein.

```sh
python3 tools/foundation.py request --sha <END_SHA> > /tmp/windowsafe-review-request.json
git show <END_SHA>:reviews/review-contract.json > /tmp/windowsafe-review-output-contract.json
python3 tools/foundation.py schema-preflight --sha <END_SHA> --schema /tmp/windowsafe-review-output-contract.json
```

Erst nach erfolgreichem Schema-Preflight beginnt der externe Review. Das externe
Output-Schema muss strukturell exakt mit dem gesamten kanonischen Vertrag
übereinstimmen, einschließlich projektspezifischer Regeln. Keine alternative
Pflichtfeldliste handschriftlich erfinden. Der Request liefert Subject, Evidence-
Hashbindungen, autoritative Reviewerrolle und Implementiereridentität.

Das Ergebnis enthält `reviewer` mit `authority` gemäß Reviewtyp, tatsächlicher
`identity`, `run_reference` und `independence` gemäß Vertrag. `provenance` enthält
die tatsächliche `source_reference` und einen der erlaubten Transportwerte.
Subject und reviewed_evidence werden aus dem Request übernommen, nachdem der
Reviewer diese Evidence tatsächlich geprüft hat. Zusätzliche Prüfungsergebnisse,
etwa die tatsächliche CI-Run-URL, gehören in die provenance source_reference
oder Findingsbeschreibung; keine nicht geprüfte Evidence als geprüft ausgeben.
Jedes Finding bindet ID, Severity, OPEN/RESOLVED, Beschreibung und Disposition.
Offene Minor-Findings benötigen explizite nichtblockierende Disposition.

Für **jedes OPEN/MINOR**, unabhängig vom Verdict und Reviewtyp, gilt exakt:
`EXPLICIT_NONBLOCKING_FOLLOW_UP: <nichtleere Begründung>`. Großschreibung und das
Leerzeichen nach dem Doppelpunkt sind verbindlich. Kein führender Text/Whitespace,
kein bloßer Follow-up-Satz, keine leere/Whitespace-Begründung. Zusätzliche
`EXPLICIT_...:`, `BLOCKING:` oder `NONBLOCKING:`-Marker in der Begründung werden
als mehrdeutig abgewiesen (auch bei anderer Großschreibung). Textliche Widersprüche
ohne Maschinenmarker und die sachliche Begründung muss der Reviewer inhaltlich
prüfen. Der Marker beweist weder authentische Autorität noch echte Nichtblockierung.
OPEN/MAJOR, BLOCKING oder CRITICAL bleiben bei PASS auch mit Marker unzulässig.

Historische V1-Subjects werden weiterhin mit dem **V1-Vertrag am alten SHA**
konsumiert, einschließlich dessen tatsächlicher Regel
`MINOR_OPEN_HAS_NONBLOCKING_DISPOSITION`. Der korrigierte Verbraucher verlangt
auch dort denselben expliziten Marker; keine ID-/SHA-Ausnahme und kein pauschales
Grandfathering beliebiger Alttexte. Das reale WS-PFR-20260917-01 enthält bereits
diesen Marker und bleibt vollständig unverändert gültig. V1-Resultate werden
nicht als V2 reserialisiert; Schema-Preflight darf V1 und V2 nicht gleichsetzen.

## Ergebnislocator, Konsum und Transport

Für alle drei Typen: **`reviews/results/<REVIEW_ID>.json`**. Foundation, Epic
Preparation und Feature Acceptance bleiben durch `review_type` eindeutig getrennt.
Resultat-IDs sind über die gesamte History eindeutig; mehrere unabhängige Reviews
desselben Subjects sind möglich. Der Kanal entsteht JIT beim ersten echten Review;
keine Dummyresultate oder von diesem Coding-Agenten erzeugten PASS-Dateien.

```sh
python3 tools/foundation.py validate-result --file /path/to/REVIEW_ID.json
python3 tools/foundation.py history --base <PREVIOUS_CANONICAL_SHA>
```

Der Validator lädt Subject, vollständigen Vertrag und Evidence erneut aus dem
im Resultat angegebenen Commit. Er prüft die Zusammengehörigkeit von ID/Typ,
Subjectpfad/SHA, Reviewerrolle/Implementierer, Evidencebytes und Resultatlocator.
Verträge und Resultate können syntaktisch korrekt sein, ohne authentisch zu sein:
Reviewautorität, unabhängiger Kontext, tatsächliches Lesen der Evidence und
Transportautorisierung sind zusätzlich anhand der externen Originalprovenienz zu
kontrollieren. Ein Name allein beweist keine Unabhängigkeit. Mechanisches PASS ist
kein Reviewverdikt und verleiht keine Ausführungs- oder Annahmeautorität.

Reviewer mit separat autorisiertem Kanalschreibrecht schreiben das vollständige
Originalresultat. Ohne Schreibrecht: provenancegebundenes Payload zurückgeben;
erst ausdrücklich autorisierter exakter Transfer, keine Umdeutung/Reklassifikation.
Vor Konsum erneut validieren. Bei Mismatch vor Konsum/Mutation stoppen, nicht den
Kanal passend abschwächen. Originalbytes und historische Resultate bleiben
append-only; Korrekturen bekommen neue IDs und neue genaue Subjectbindungen.

Für WS-HC endet der Coding-Auftrag am ungemergten reviewbereiten Head. Danach
unabhängiger Delta-Review und **separate Integrationsfreigabe**; PASS allein startet
keinen Merge. Erst nach autorisierter Integration folgen Kontext-Sync oder
NOT_APPLICABLE und FIRST_EPIC_PREPARATION mit seinen getrennten Gates.
