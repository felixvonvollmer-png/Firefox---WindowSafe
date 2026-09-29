# Foundation Delta Evidence und Review-Handoff

Run WS-PFDELTA-MAT-20260928-01 unter WS-EA-20260928-01. Kein unabhängiger Verdict.
Basis: main `3bdd7439c221b8f8c83e7374c8bb29898891a4fd`.
Branch: `foundation/ws-pf-delta-20260928-01`.
Subject: `foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json`.
Der kanonische Request bindet Subject und Evidence an den vollständigen Commit-SHA;
kein selbstreferenzieller End-SHA in diesem Dokument. End-Head/Tree, PR und CI-URLs
stehen im Delivery-Handoff am PR. Unabhängig genau diese Git-/CI-Objekte verifizieren.

## Input- und Baselineprüfung

REPOSITORY_OR_REMOTE_VERIFIED: Root/Origin, Repository-ID 1374094477, public,
sauberer Worktree/Index/untracked; lokales und Remote-main gleich Startbasis.
Neuer Branch war vor Erstellung lokal/remote nicht vorhanden.
PR #3 offen/Draft/ungemergt, Head `7d66ca5b025c8f748d7f97b961c496ee450daaa7`.
Keine F01-Inhalte übernommen; nur externer Evidence-Locator.

LOCAL_AGENT_REPORTED: ZIP 41212 Bytes, SHA-256
`57799bfbd31c428a1c395916e40acded00e29a78da7d29ed0248c049379a4cff`.
Exakter Membersatz: 16 eindeutige Dateien; alle 15 manifestierten Dateien erfüllen
Bytelänge und SHA-256. Originalmanifest zusätzlich SHA-256
`bf6a4832c52860a136090790e3ec973b7a6536546a30dcc54711e0f09f69d757`.
Ablage: `foundation/inputs/WS-PFDELTA-MAT-20260928-01/`, unveränderte Originalbytes.
Base Product, Approval und TF r6 stimmen mit den SHA-256-Bindungen des Pakets überein.
Die PASS-/Authority-Provenienz stammt aus dem mitgelieferten unabhängigen Original;
dieser Implementierer hat keinen unabhängigen Review wiederholt oder ausgestellt.
Nicht mitgelieferte ältere Rereview-Handoff-/Schema-Dateien bleiben historische
Resultatreferenzen; ihre Bytes werden hier nicht als erneut geprüft behauptet.

REPOSITORY_OR_REMOTE_VERIFIED: Meta-main
`0dc8f145d27f796ea8ae230fae6ec4b21d6aa921`; alle sieben in der Autorisierung
gebundenen V6-Git-Blobs über GitHub gelesen, einschließlich Git-Blob-Header nachgehasht
und im exakten Commitbaum verifiziert. F1/F2/README additiv lokal unter
`foundation/sources/v6-final-20260918/`. Weitere Meta-Dokumente bleiben exakte
Locator in der Autorisierung; kein externer Projektbeschreibungstext installiert.

## Brownfield-Entscheidung und Risiko

KEEP: Product-/TF-/Epic-/Revieworiginale, alter Foundation-Subject, V1/V2/V3-Reviewkanal,
kanonischer Validator, kumulative historische Basis, normaler Integrationsnachweis,
Append-only-Zwischencommitprüfung, deterministischer POSIX-Inventarwriter, CI-Pins.
SIMPLIFY: ein neuer versionierter Foundation-Subject und dieses Evidence-Dokument;
keine zweite Review-Schema- oder Stateverwaltung. Originalinputs einmal bytegetreu.
REMOVE_FROM_ACTIVE_ROUTING: alte V6-Blobs und erledigte Integrationsaufträge;
Originale bleiben erhalten. Keine Toolchain-, Dependency- oder Architekturablösung.

ELEVATED: WS-P05 betrifft Recovery-/Plattformgrenzen; Harnessänderung betrifft
Subject-/Autoritätsrouting. Unabhängiger Project Foundation Review ist erforderlich.
Kein Produktcode, Browserzugriff, realer Datensatz, Provider oder neuer Dependency.
Der Delta-Scope wird an unabhängig gepinnte Autorisierung und Manifest gebunden.
Die frühere Accepted-Epic-Scopeprüfung wird an ihrer unveränderten integrierten Basis
weiter ausgeführt; die neue lineare Strecke erhält eine eigene enge Scopeprüfung.
Alle bisherigen kumulativen Historyprüfungen bleiben zusätzlich aktiv.
Historische Integrationstest-Fixtures verwenden historische Dokumentrouter, weil
heutige Router auf bewusst nicht in diesen alten Fixtures enthaltene Inputs zeigen.

## Verifikation am Delivery-Head

Lokale Pflichtbefehle (LOCAL_AGENT_REPORTED; Resultate im Delivery-Handoff):

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build --verify-repeat
python3 tools/foundation.py request --sha HEAD --subject foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json
python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json
python3 tools/foundation.py history --base 3bdd7439c221b8f8c83e7374c8bb29898891a4fd
git diff --check
```

CI_VERIFIED erst nach tatsächlich abgeschlossenen erfolgreichen Foundation-Jobs mit
exaktem head_sha, Run-/Job-URL im PR-Handoff. CI wiederholt lokale Pflichtgates;
keine Runtime-, GUI-, Restart-, Windows-Desktop- oder Hard-Peak-Claims.
Vor Push: named-path staged Diff, Schutz historischer Originale und F01-Ref prüfen.
Nach Push: lokale/tracking/remote SHA-Gleichheit, main und PR #3 erneut prüfen.
Neue Regressionen decken Input-/Source-/Lifecycle-/Evidence-Drift, unzulässigen
Subject-Locator, Scope, unveränderte historische Requests und verdeckte
Zwischencommitänderungen ab. Grüne Tests authentifizieren keinen Reviewer.

## Kritische Eigenprüfung

WS-P05 wurde gegen Product Delta und TF Delta geprüft: gewöhnliche öffentliche
Tabs/Fenster, kein nativer Discriminator, keine native Wiederherstellungszusage,
sichtbare allgemeine Einschränkung, kein unnötiger per-Fenster-Marker.
Private-/Container-/Identitäts-/Recovery-/Ressourcengrenzen bleiben erhalten.
Kritische Punkte der Harnessprüfung: exact manifest inventory, unabhängig gepinnte
Autorisierung, additive Quellen, eindeutiger versionierter Subject, Scope jedes
Zwischencommits, unveränderte historische Epic- und Foundationbindungen.
Der erste Testlauf erkannte einen beim Einfügen verrutschten Manifest-Scope-Guard
(`epics/E/evidence/manifest.json`). Der bestehende Negativtest blieb unverändert;
der Guard wurde wieder direkt in `scope()` eingesetzt. Der vollständige erneute
Testlauf und die finalen CI-Gates müssen diese Korrektur bestätigen.
Lokale Eigenprüfung: alle 99 Tests bestanden; Foundation check und deterministischer
Build bestanden. `git diff --cached --check` meldet ausschließlich sechs originale
Leer-Kontextzeilen der bytegebundenen `.diff`-Inputdatei (Zeilen 4/20/24/36/57/75).
Disposition: unverändert bewahren; diese Leerzeichen sind Unified-Diff-Kontextsyntax,
keine neu verfassten Whitespacefehler. Der bestehende Harness nimmt gehashte
Originalinputs von Formatnormalisierung aus. Separater staged Whitespacecheck der
verfassten Pfade plus Bytevergleich aller Originale; keine Regel oder Inputbytes geändert.
Die abschließenden Testergebnisse und Self-Review-Dispositionen sind an den
Delivery-Head gebunden. Kein unabhängiges Selbst-PASS.

## Offene Gates und Stop

PROJECT_FOUNDATION_READY_FOR_REVIEW ist der Stop bei grünen Pflichtchecks;
unabhängiger Project Foundation Review steht aus. Keine offene materielle
Nutzerentscheidung aus der vorliegenden WS-P05-Bindung.
Externer Project Context Sync: PENDING_AFTER_PROJECT_FOUNDATION_REVIEW_PASS.
Danach erforderlicher tatsächlicher Sync mit Nutzer-/externer Bestätigung oder
explizit begründetes NOT_APPLICABLE, dann erst Epic Delta, kritischer und unabhängiger
Epic Review, exaktes Rebinding, neue F01-Ausführungsautorisierung und Restqualifikation.
PR #3 bleibt Draft/offen/ungemergt. Ubuntu Display/State und Messmethodik bleiben offen;
vorhandene exakte Restart-Evidence wird nicht wiederholt. Kein Feature Acceptance,
Merge, Release, Signing, AMO, Deployment oder Production. Keine Agentendelegation.
