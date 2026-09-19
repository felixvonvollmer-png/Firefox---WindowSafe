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

## Aktueller Lifecycle

Der historische Bootstrap-Subject am SHA
`4ba2c473fe4d90c85d94ee2b2f5cc5777d115109` erhielt WS-PFR-20260917-01 PASS mit
offenem nichtblockierendem MINOR. Vollständiger unveränderter Rücklauf:
`reviews/results/WS-PFR-20260917-01.json`. Das PASS gilt ausschließlich für den
alten Subject. Der separate Validator-Residual ist kein nachträgliches Finding
dieses Reviews. Beide historischen Befunde werden nicht vom Coding-Agenten geschlossen.

Aktuell autorisiert: **WS-HC-20260918-01** durch **WS-EA-20260918-01**:
Reviewtransfer nach Originalkonsum, V1-/V2-Verträglichkeit, unabhängig gebundene
Historybasis und Vorbereitung der Reviewer-Umgebung. Fortsetzung auf
`fix/ws-hc-20260917-01` ab `9b6dd621deec1193bfdfbdfa730e8f9349c73fd6`;
kumulative Review-/Historybasis und main bleiben
`4ba2c473fe4d90c85d94ee2b2f5cc5777d115109`.
Originalinputs: `foundation/evidence/followup-inputs.json` und die dort gebundenen
`followup-*`-Dateien. WS-EA-20260917-02 und seine Evidence bleiben historisch.

Der neue unveränderte Rücklauf `reviews/results/WS-PFR-20260918-01.json` ist
**BLOCKED**. Sein POSIX/Linux-Writer-Finding ist RESOLVED; das ursprüngliche
PASS-Resultat bleibt mit MINOR/OPEN unverändert. Die zwei MAJOR-Korrekturen werden
als Implementiererarbeit zur erneuten Prüfung vorgelegt. Der Umgebungsblocker F02
bleibt OPEN: Vorbereitung und CI ersetzen nicht den eigenen unabhängigen Preflight
und die abschließende Resultatvalidierung. Das neue Subject ist reviewbereit,
nicht akzeptiert. Kein unabhängiger Review wurde durch diesen Lauf gestartet.

Korrektur → lokale Pflichtchecks/CI → PROJECT_FOUNDATION_READY_FOR_REVIEW auf
exaktem **ungemergtem** Branch-/PR-Head → **STOP** → unabhängiger gezielter
PROJECT_FOUNDATION_REVIEW → separate Integrationsfreigabe. Auch ein späterer PASS
autorisiert hier keinen Merge. Erst nach angenommener und autorisierter Integration
folgen Kontext-Sync/NOT_APPLICABLE und FIRST_EPIC_PREPARATION. Keine Epic-/Feature-
oder Browserarbeit in diesem Lauf; alle bestehenden Vorab-Gates bleiben bestehen.

Ein externer installierter ChatGPT-Projektkanal ist hier nicht gebunden.
Der Review läuft über Git-Locators: externer Text-Sync ist für diesen Bootstrap
NOT_APPLICABLE. Wird später ein solcher Kanal verlangt, bleibt Installation/Sync
bis ausdrücklicher externer Bestätigung offen.
