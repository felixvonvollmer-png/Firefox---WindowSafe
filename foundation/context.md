# Kontext und Provenienz

## Rangfolge und Rolle

Aktuelle ausdrückliche Nutzerentscheidung und freigegebene Product Truth stehen
über harten technischen Invarianten, gebundener Epic Preparation und reversiblen
Engineeringentscheidungen. Dieser Lauf arbeitet als Coding-Agent nach Foundation 2.
Die Originaltexte sind Eingaben im ausdrücklich autorisierten Bootstrap;
historische Zustandsfelder sind keine neue Autorisierung und werden nicht editiert.

Alle Paketdateien liegen byteidentisch unter `foundation/inputs/`, einschließlich
des ursprünglichen `SHA256SUMS.json`. Die zwölf Einträge wurden gegen SHA-256 und
Bytelänge geprüft. Der Manifesthash lautet
`80203ae9f554aa4dba951d316a685bd20cbe57ef28a2912fd49608cdaf9cb6a8`.
Dieser Hash wurde beim Eingang beobachtet; separat vom Nutzer vorgegeben war der
Handoffhash `15701c717061773d9017cf3c884a7eb0cebcb0d66b67a93dc13e41acb7d98774`.
Die Handoffbindungen wurden zusätzlich gegen die tatsächlichen Dateien geprüft.

## Kanonische Locator

Alle folgenden Dateinamen sind relativ zu `foundation/inputs/`:

| Kontext | Pfad |
|---|---|
| Product Truth | `inputs/WindowSafe_Product_Definition_WS-PD-20260917-01.md` |
| Product Approval | `inputs/WindowSafe_Approval_Record_WS-PD-20260917-01.json` |
| Technical Foundation r6 | `inputs/WindowSafe_Technical_Foundation_WS-TFP-20260917-01_r6.md` |
| Technische Entscheidungen T05-R2 | `inputs/WindowSafe_Technical_Decisions_WS-TD-20260917-03.json` |
| Exakter T05-R2-Subject | `inputs/WindowSafe_Last_CPU_Decision_WS-T05-R2-20260917-01.md` |
| Unabhängiger Preparation-PASS | `inputs/WS-TFPR-20260917-04.json` |
| Preparation-Binding | `inputs/WindowSafe_Preparation_Binding_WS-TFP-20260917-01_READY_FOR_AGENT.json` |
| Execution Envelope | `WindowSafe_Execution_Authorization_WS-EA-20260917-01.json` |
| Start-Handoff | `WindowSafe_Project_Foundation_Agent_Start_Handoff_WS-PFBOOT-20260917-01.md` |

Historische Verweise im Paket (etwa `history/`, `product/`, frühere Reviews und
das Größenproben-Skript) sind keine zusätzlichen beigefügten Dateien. Die oben
gebundenen aktuellen Inputs sind vollständig vorhanden. Frühere Reviewbehauptungen
werden als Paketprovenienz übernommen, nicht als hier erneut ausgeführte Prüfung.
Insbesondere wurde die historische Größenprobe nicht reproduziert.

Die Product-Datei bleibt im historischen Status PROPOSED; ihr separater Approval
Record bindet APPROVED. r6 bleibt historisch REVIEW_REQUIRED; PASS 04 und das
separate READY-Binding binden den geprüften aktuellen Tuple. Erst die separate
Execution Authorization und der aktuelle Nutzerauftrag autorisieren diesen Lauf.

## V6-Quellen

Aus `felixvonvollmer-png/projektbeschreibung-und-geruest` wurden ausschließlich
die exakten Git-Blobs geladen und einschließlich Git-Blob-Header nachgehasht:

| Rolle | Lokale Originalbytes | Git-Blob |
|---|---|---|
| Foundation 2 / Coding-Agent | `foundation/sources/foundation-2.md` | `ff49e56aba09881e9e4a22dc8225949fbc4b54f6` |
| Foundation 1 / LLM und unabhängige Verdicts | `foundation/sources/foundation-1.md` | `3b139a7dfd70da3ae6c83bbdfa703cb98ef94193` |

Kein beweglicher Branch ersetzt diese Quellen; historische Candidate-Felder
werden nicht umgeschrieben. Kein neuer Foundation-Pair-Review.

## Historischer Lifecycle bis zur Epic-Integration

Der historische Bootstrap-Subject am SHA
`4ba2c473fe4d90c85d94ee2b2f5cc5777d115109` erhielt WS-PFR-20260917-01 PASS mit
offenem nichtblockierendem MINOR. Vollständiger unveränderter Rücklauf:
`reviews/results/WS-PFR-20260917-01.json`. Das PASS gilt ausschließlich für den
alten Subject. Der separate Validator-Residual ist kein nachträgliches Finding
dieses Reviews. Beide historischen Befunde werden nicht vom Coding-Agenten geschlossen.

Die Korrektur WS-HC-20260918-01 am Subject
`fc3ee73c9bf1fab3878c480a0299fda4119e363b` erhielt den unabhängigen PASS
[WS-PFR-20260918-02](../reviews/results/WS-PFR-20260918-02.json).
Der Originalrücklauf löst alle vier Findings einschließlich F02 auf; frühere
PASS-/BLOCKED-Resultate und deren damalige Zustandsfelder bleiben unverändert.
Der genaue Resultattransfer und die autorisierte Normal-Merge-Integration sind
in main `dc9c1c37a264cc80f79ec08bf166ec42cdd73b95` enthalten.

Die historische Materialisierung WS-E01-MAT-20260919-01 unter WS-EA-20260919-04
lieferte den unveränderten Preparation-Subject am SHA
`644b81f63dcc1990bc894a9c2c9bd8dc24a98c04`. Dieser erhielt den unabhängigen
[WS-E01-EPR-20260919-02 PASS](../reviews/results/WS-E01-EPR-20260919-02.json).
Das Original hat 22666 Bytes und SHA-256
`1b59d6fc89c293e738ea4e9f16e4004abef5736da527e5c2f7c60533260977d7`.
Die lokale Originaldatei wurde unter CPython 3.14.4 kanonisch vor dem bytegenauen
Transfer validiert. Keine Rekonstruktion aus Chattext.

Damals autorisiert: **WS-E01-INT-20260919-02** durch **WS-EA-20260919-05**;
Original: [integration-authorization.json](../epics/WS-E01/evidence/integration-authorization.json).
Das [Accepted-Binding](../epics/WS-E01/binding.json) setzt READY_FOR_AGENT und bindet
weiterhin genau den reviewed Subject und dessen main-Basis. Der ursprüngliche
Subject, Product-/Foundationinputs und alle historischen Resultate bleiben unverändert.
Das einzige OPEN/MINOR bleibt im Reviewer-Original erhalten; der verlangte
Routing-Follow-up wird unter dieser Autorisierung in [reviews/README.md](../reviews/README.md)
dokumentiert. Der historische WS-HC/F02-Auftrag ist kein aktueller Reviewrouter.

Dieser Lauf umfasst nur Originaltransfer, Accepted-Binding-/Harness-Übergang,
Routing-Follow-up, lokale/Exact-Head-CI-Gates und normalen Mergecommit von PR #2.
STOP nach Post-Merge-Prüfung. READY_FOR_AGENT akzeptiert die Preparation und startet
kein WS-E01-F01. Für Feature-/Produkt-/Browser-/Profilarbeit bleiben spätere explizite
Ausführungsautorisierung und vorgelagerte Test-Envelopes erforderlich.

Ein externer installierter ChatGPT-Projektkanal ist hier nicht gebunden.
Der Review läuft über Git-Locators: externer Text-Sync ist für diesen Bootstrap
NOT_APPLICABLE. Wird später ein solcher Kanal verlangt, bleibt Installation/Sync
bis ausdrücklicher externer Bestätigung offen.

## Aktueller F01-Qualifikationslauf

WS-EA-20260919-06 autorisiert WS-E01-F01-START-20260919-01 ab main
`3bdd7439c221b8f8c83e7374c8bb29898891a4fd`. Sechs Startoriginale wurden bytegenau
nach `features/WS-E01-F01/` übertragen. Das bisherige Accepted-Epic-Binding und
alle Product-/Foundation-/Revieworiginale bleiben unverändert.

[Featurezustand](../features/WS-E01-F01/state.json) und
[Qualifikationsbericht](../features/WS-E01-F01/evidence/qualification-report.md)
sind die aktuellen Locator. Partial-Evidence ist keine technische Annahme; das finale
Auditgate ist wegen Registry-Wartung BLOCKED. Windows Desktop
und weitere native/instrumentelle Teilnachweise bleiben offen. Keine Produktimplementation,
kein F02, keine Feature Acceptance, kein Merge. Fortsetzung nur innerhalb des gebundenen
synthetischen Test-Envelopes; keine echten Browserprofile.
