# Kanonischer Reviewkanal und aktuelle Review-Locators

## Aktueller Auftrag: EPIC_PREPARATION_REVIEW (Rereview) des zweifach korrigierten WS-E01-Deltas

Subject **WS-E01-EP-DELTA-20260929-04**, Locator
`epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json` am vollständigen End-SHA aus
dem Delivery-Handoff von PR #5 (`prep/ws-e01-delta-20260929-02`, ungemergt; Basis main
`1cb82c926903b2fd6b497d008db61c71c5d92aca`). Rolle `INDEPENDENT_EPIC_PREPARATION_REVIEWER`,
Vertrag unverändert V3, Resultat `reviews/results/<REVIEW_ID>.json` mit neuer Review-ID.
Der Request enthält `review_excluded_identities`; `request` scheitert, wenn eine transitiv aus
der Preparation-/Correction-/Supersession-Linie abgeleitete Autoren-/Materializeridentität
fehlt. Keine dieser Identitäten darf als `reviewer.identity` auftreten (Vollgleichheit nach
Rand-Whitespace/Case-Normalisierung; ersetzt keine Provenienzprüfung). Kanonische Prüfung in
einem sauberen Checkout des End-SHA (lokale ignorierte Agentenkonfiguration beeinflusst
sonst `files()`; nichtblockierender Follow-up N01).

```sh
python3 tools/foundation.py request --sha <END_SHA> --subject epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/subject.json
python3 tools/foundation.py schema-preflight --sha <END_SHA> --schema reviews/review-contract.json
python3 tools/foundation.py history --base 1cb82c926903b2fd6b497d008db61c71c5d92aca
```

Prüfbereich: Schließung von WS-E01-EPR-DELTA-20260929-03-F01 aus der Ersatz-Evidence
`results/WS-E01-EPR-DELTA-20260930-04.json` (`RECONSTRUCTED_FROM_REVIEW_TRANSCRIPT`, nicht das
verlorene Original) und F04 aus `results/WS-E01-EPR-DELTA-20260929-02.json` (BLOCKED),
kumulativer Delta-/Harness-Stand seit main, unveränderte fachliche Delta-Aussage, historische
Unveränderlichkeit, Tests, Exact-Head-CI. Die alten Locators -02/-03 liefern weiter die Requests
an ihren reviewed Heads `48d7b0f…` bzw. `dee7ab5…`. Kritische Eigenprüfung und grüne CI sind
kein unabhängiges PASS.

## Historischer Stand: Project Foundation Delta angenommen

[Subject](../foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json): **WS-PFDELTA-MAT-20260928-01**,
reviewed Head `bbca750fab1e760714cf409b8751287db6b93041`, unverändert.
Unabhängiges Resultat: [WS-PFR-DELTA-20260928-01](results/WS-PFR-DELTA-20260928-01.json),
**PASS**, 13537 Bytes, SHA-256 `3dbc5884e32529fd4a7097a055b6ab77d5874b398b15e6048e329a42beee9992`,
byteidentisch übertragen. Separates [Acceptance-Binding](../foundation/deltas/WS-PFDELTA-MAT-20260928-01/binding.json)
unter [WS-EA-20260929-01](../foundation/evidence/pf-delta-integration-authorization.json)
(Lauf WS-PFDELTA-INT-20260929-01): Harness akzeptiert nur diesen gebundenen
Post-Review-Übergang und genau einen normalen Mergecommit von PR #4 auf
`3bdd7439c221b8f8c83e7374c8bb29898891a4fd`. Der aktuelle Request liefert weiter
den exakten reviewed Request. Externer Sync **PENDING**; nächstes Gate
`REQUIRED_EXTERNAL_REVIEW_BOOTSTRAP_INSTALL_SYNC_OR_NOT_APPLICABLE`. Kein Epic Delta,
Rebinding, F01, Feature Acceptance oder Production.

Die folgenden Review-Anweisungen des Delta-Reviews sind historisch:
Kanonischer V3-Vertrag und Resultatkanal bleiben unverändert; kein alternativer
Reviewvertrag für das Delta. Neue Foundation-Subjects besitzen versionierte Locator,
`foundation/subject.json` bleibt historisch. TF-Preparation-Resultate liegen als
externe Originalinputs vor, nicht als neu erzeugte Repository-Reviewresultate.

```sh
python3 tools/foundation.py request --sha <END_SHA> --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json
python3 tools/foundation.py schema-preflight --sha <END_SHA> --schema reviews/review-contract.json
python3 tools/foundation.py history --base 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
```

Review durch frischen/ausreichend isolierten unabhängigen Kontext, read-only am
exakten SHA. Kritische Eigenprüfung und grüne CI sind kein unabhängiges PASS.
Review umfasst WS-P05-Fidelität, finale V6-Router, historische Kompatibilität,
Scope-/Historyguards, lokale Tests und exakte CI. Resultat vor Transport mit dem
kanonischen Verbraucher validieren. Kein Merge, externer Sync, Epic-Rebinding,
F01-Start, Feature Acceptance oder Production durch dieses Review vorbereitet.


## Historischer Einstieg: Epic Preparation und Feature Acceptance

WS-E01 Preparation ist mit dem unveränderten unabhängigen
[WS-E01-EPR-20260919-02 PASS](results/WS-E01-EPR-20260919-02.json) angenommen.
Der exakte reviewed Subject ist `epics/WS-E01/subject.json` am SHA
`644b81f63dcc1990bc894a9c2c9bd8dc24a98c04`; das aktuelle
[Binding](../epics/WS-E01/binding.json) referenziert diesen historischen Zustand
als READY_FOR_AGENT. WS-EA-20260919-05 autorisiert ausschließlich den exakten
Resultattransfer, Accepted-Binding-/Harness-Übergang, diesen Routing-Follow-up und
geprüfte Normal-Merge-Integration von PR #2. Danach STOP. Kein WS-E01-F01-Start.

Für einen neuen Epic Preparation Review: `epics/<EPIC_ID>/subject.json` am dann
explizit gebundenen vollständigen SHA. Für spätere kumulative Feature Acceptance:
`features/<FEATURE_ID>/subject.json` am separat vorbereiteten Acceptance-SHA.
Der gemeinsame V3-Kanal bleibt `reviews/results/<REVIEW_ID>.json`; Reviewtyp,
Subject und tatsächliche Autorisierung sind getrennt zu prüfen. Feature-Locators
beschreiben den späteren Kanal; diese Integration materialisiert kein Feature.

Vor fachlichem Review führt der unabhängige Reviewer den Request mit explizitem
`--subject`, den V3-Schema-Preflight und den CPython-3.14.4-Umgebungspreflight selbst
aus; anschließend validiert er sein exaktes Original mit `validate-result`.
`request --sha HEAD --subject epics/WS-E01/subject.json` validiert bei akzeptiertem
Binding den Übergang und liefert den ursprünglichen Reviewrequest mit seinen
23 Evidence-Bindungen. Der Integrations-Head wird dadurch nicht zum reviewed Subject.

**Follow-up nach dem Review:** Das nichtblockierende MINOR
`WS-E01-EPR-20260919-02-F01` bleibt im Original OPEN mit seiner unveränderten
Disposition. Der dort verlangte Living-Context-Follow-up wurde in
WS-E01-INT-20260919-02 unter WS-EA-20260919-05 ausgeführt: aktueller Epic-/Feature-
Router oben, historischer WS-HC-Auftrag unten, konsistente Einstiege in README,
AGENTS, Epic-Karte und Foundationkontext. Trigger: dieser separat autorisierte
Integrationsübergang, vor weiterer Nutzung des Routers. Das ist die dokumentierte
Ausführung des Follow-ups, kein rückwirkend geändertes unabhängiges Finding.

## Historischer Auftrag: PROJECT_FOUNDATION_REVIEW (WS-HC, abgeschlossen)

Die folgenden damaligen Branch-/Baseline-/PENDING-Anweisungen sind ausschließlich
historischer Kontext und kein aktueller Reviewauftrag. Der spätere unabhängige
WS-PFR-20260918-02 PASS löste F02 auf und wurde in main
`dc9c1c37a264cc80f79ec08bf166ec42cdd73b95` integriert.

Subject-ID **WS-HC-20260918-01**. Subject-Locator: `foundation/subject.json`
an dem **vollständigen End-SHA aus dem Coding-Agent-Handoff**. Den SHA einmal
read-only gegen `fix/ws-hc-20260917-01` und PR-Head verifizieren; `main` muss weiter
auf `4ba2c473fe4d90c85d94ee2b2f5cc5777d115109` liegen. Danach ausschließlich diesen Commit
reviewen. Der Subject enthält bewusst keinen selbstreferenziellen Commit-Hash.

Kontext: `foundation/context.md`, exakte Product-/Approval-/Preparation-/Binding-
und Execution-Inputs, `foundation/sources/foundation-2.md` und Foundation 1.
Evidence: `foundation/evidence/followup-correction.md`, Originalkonsumbeleg,
Followup-Inputs und die im Subject genannten Dateien; Tests/Guards selbst prüfen. CI-Run für exakt diesen head_sha
über GitHub Actions lesen. Keine Browserprofile, Produktimplementation oder
Subjectänderung während des Reviews. Das ist ein Reviewauftrag, kein Verdict.

Der unabhängige Reviewer prüft Product Fidelity, harte Invarianten, Architektur,
Harness, Traceability, reproduzierbare lokale/CI-Evidence, Scope, Security,
Reviewvertrag und langlebigen Kontext. Agentenclaims nicht ungeprüft übernehmen.
Der gezielte Review prüft V1-/V2-/V3-Verträglichkeit, den History-Fallback,
Originaltransfer, Umgebungsfähigkeit und Tests/CI am neuen Head. Laufstart bleibt
9b6dd621..., die gesamte unakzeptierte Strecke ab 4ba2c473... ist im Prüfbereich.
Der erhaltene Rücklauf bleibt BLOCKED. Die Vorbereitung schließt F02 nicht.
Vor fachlichem Review muss der Reviewer den [Umgebungspreflight](../foundation/reviewer-environment.md)
selbst erfolgreich ausführen; nach dem Review muss er sein Originalresultat selbst
mit dem kanonischen Verbraucher validieren. Unveränderte Bereiche dürfen über
den historischen PASS referenziert werden. Externe Finding-Closure ist noch offen.
PASS erfordert keine offenen Critical/Blocking/Major; BLOCKED benötigt passende
Rebindung statt verdecktem Korrekturloop. Findingsfreiheit wird nicht vorgegeben.

## Vertragsformat und Preflight

Autoritativer vollständiger Outputvertrag ist `reviews/review-contract.json` am
Subject-SHA. Er ist ein expliziter WindowSafe-Vertrag, **kein JSON-Schema-Dialekt**.
Das Feld `semantic_minimum_mapping` bindet alle Mindestfelder aus Foundation 2 §32.
Alle Objekte haben genau die dort angegebenen Felder; zusätzliche Felder sind
unzulässig. Neue Resultate verwenden `schema_version: 3` passend zu
`contract_version: 3` / `WINDOWSAFE_REVIEW_CONTRACT_V3`. SHA ist ein voller Git-SHA-1,
Evidencehash ein SHA-256. IDs enthalten nur Buchstaben, Ziffern, `_` oder `-`.
Alle sonstigen Textfelder sind nichtleer, `findings` darf leer sein.

```sh
python3 tools/foundation.py request --sha <END_SHA> --subject <SUBJECT_PATH> > /tmp/windowsafe-review-request.json
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

Für **jedes V2-/V3-OPEN/MINOR**, unabhängig vom Verdict und Reviewtyp, gilt exakt:
`EXPLICIT_NONBLOCKING_FOLLOW_UP: <nichtleere Begründung>`. Großschreibung und das
Leerzeichen nach dem Doppelpunkt sind verbindlich. Kein führender Text/Whitespace,
kein bloßer Follow-up-Satz, keine leere/Whitespace-Begründung. Zusätzliche
`EXPLICIT_...:`, `BLOCKING:` oder `NONBLOCKING:`-Marker in der Begründung werden
als mehrdeutig abgewiesen (auch bei anderer Großschreibung). Textliche Widersprüche
ohne Maschinenmarker und die sachliche Begründung muss der Reviewer inhaltlich
prüfen. Der Marker beweist weder authentische Autorität noch echte Nichtblockierung.
OPEN/MAJOR, BLOCKING oder CRITICAL bleiben bei PASS auch mit Marker unzulässig.

Historische V1-/V2-Subjects werden mit dem **jeweiligen unveränderten Vertrag am
alten SHA** konsumiert. V1 benötigt tatsächliche Nichtblockierungssemantik, keine
rückwirkende V2-Syntax. Der historische Text
`nonblocking follow-up with next-review trigger` ist ohne Marker zulässig; ebenso
der explizite Marker mit nichtleerer eindeutiger Begründung. Dies sind Textregeln,
keine Review-ID-/SHA-Ausnahmen. Das reale alte PASS bleibt unverändert gültig.

Andere nichtleere V1-Freitexte öffnen **V1_SEMANTIC_DISPOSITION_REQUIRED**. Der CLI
liefert einen gebundenen offenen Dispositionsrequest (Originalbytehash, Subject,
Evidence, Originalprovenienz, Reviewerrolle), Exit 1. Das ist weder ein V2-Syntaxfehler
noch ein akzeptierter beliebiger Freitext. Es gibt keine NLP-/Providerabhängigkeit.
Ein separat autorisierter unabhängiger Reviewer kann seine inhaltliche Beurteilung
in `reviews/dispositions/<REVIEW_ID>.json` oder einer extern zurückgegebenen Datei
liefern. Der V3-Vertragsabschnitt `legacy_v1_disposition` enthält die vollständigen
Felder. Die separate Datei bindet den SHA-256 der **Originalresultatbytes**, Subject,
Evidence und ursprüngliche Provenienz. `reviewer` und `provenance` haben dieselben
Felder/Rollen-/Unabhängigkeitsregeln wie der Reviewvertrag. Jede Entscheidung bindet
Finding-ID, SHA-256 des unveränderten UTF-8-Dispositionstextes, Entscheidung
`NONBLOCKING_FOLLOW_UP`, nichtleere Begründung, konkretes Follow-up und Trigger.
Genau alle unklaren OPEN/MINOR-Findings müssen einmal enthalten sein.

```sh
python3 tools/foundation.py validate-result --file /path/to/REVIEW_ID.json --semantic-disposition /path/to/separate-disposition.json
```

Leere Texte oder explizit blockierende/mehrdeutige Marker sind nicht durch den
Sidecar übersteuerbar, ebenso wenig V2-/V3-Regeln oder PASS mit offenen höheren
Severities. Für Repositoryresultate wird der kanonische Sidecar automatisch
mitgeprüft; verwaiste oder überflüssige Dispositionen sind unzulässig. Originale
werden nie editiert. Auch ein technisch gültiger Sidecar beweist keine Authentizität
oder sachliche Richtigkeit; Originalprovenienz und unabhängige Beurteilung sind
extern zu bestätigen. In diesem Lauf wurde **kein realer Sidecar** erfunden.
V1, V2 und V3 dürfen beim Schema-Preflight nicht gleichgesetzt werden.

## Ergebnislocator, Konsum und Transport

Für alle drei Typen: **`reviews/results/<REVIEW_ID>.json`**. Foundation, Epic
Preparation und Feature Acceptance bleiben durch `review_type` eindeutig getrennt.
Resultat-IDs sind über die gesamte History eindeutig; mehrere unabhängige Reviews
desselben Subjects sind möglich. Der Kanal entsteht JIT beim ersten echten Review;
keine Dummyresultate oder von diesem Coding-Agenten erzeugten PASS-Dateien.

```sh
python3 tools/foundation.py validate-result --file /path/to/REVIEW_ID.json
python3 tools/foundation.py history --base 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
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

Historisch galt: Für WS-HC endet der Coding-Auftrag am ungemergten reviewbereiten Head. Danach
unabhängiger Delta-Review und **separate Integrationsfreigabe**; PASS allein startet
keinen Merge. Erst nach autorisierter Integration folgen Kontext-Sync oder
NOT_APPLICABLE und FIRST_EPIC_PREPARATION mit seinen getrennten Gates.
