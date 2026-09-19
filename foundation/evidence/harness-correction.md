# WS-HC-20260917-01 — Korrekturevidence und Delta-Review-Handoff

Subject: `foundation/subject.json` am exakten ungemergten Branch-/PR-Head aus dem
Abschlusshandoff. Baseline `4ba2c473fe4d90c85d94ee2b2f5cc5777d115109`, Tree
`2cdf2d0484463c9639d924f0aa239499637e941b`; Arbeitsbranch
`fix/ws-hc-20260917-01`. Aktuelle Execution Authorization: WS-EA-20260917-02.

Status: **PROJECT_FOUNDATION_READY_FOR_REVIEW**, sobald alle unten genannten
Pflichtchecks und CI am finalen Kandidaten erfolgreich abgeschlossen sind.
Interner Review: implementierender Coding-Agent / SELF_REVIEW. Kein unabhängiges
Verdict und keine externe Finding-Closure. Inkrementrisiko: **ELEVATED** wegen
Ausgabeschreibpfad und allgemeiner Durchsetzung des Reviewvertrags.
Der interne Gesamtdiff-Review ist abgeschlossen: keine zusätzlichen offenen
Selbstbefunde. Die externen historischen Befunde bleiben bis zur unabhängigen
Bestätigung in der unten beschriebenen offenen Disposition.

## Autorisierung, Inputs und tatsächlicher Transfer

ZIP-SHA-256:
`12942363cb86e2318d23edd0f97010ceeee6aa1758ccae1324d8d3c1b98d2020`.
27 äußere Manifestentries und 21 Entries des verschachtelten Rücklaufmanifests
nach Hash/Bytelänge geprüft; keine Duplikate, Traversal-/Symlinkentries oder CRC-
Fehler. Autorisierungsbindungen sowie historische Quellkopien stimmen mit dem
exakten Baseline-Git überein. Beide V6-Blobs nach Git-Objektidentität geprüft.
Paketpfad-/Hashmapping: `foundation/evidence/harness-inputs.json`. Nur benötigte
fünf Originalrecords separat übernommen, kein Paketdump und keine Änderung des
alten Bootstrapmanifests. Diese fünf Inputs sind auch mechanisch hashgeschützt.

Vollständiger historischer Reviewtransfer:
`reviews/results/WS-PFR-20260917-01.json`, **10136 Byte**,
SHA-256 `c4c908eb70c99252f185ee89d077919ecc9598cc2842b2f0b1209734f115c19f`.
Tatsächlicher Transfercommit:
`48224840e68da6c66c0f129f0564fcaad9c1ad8e`. Keine erneute Dekodierung,
Reserialisierung oder Feldänderung. Separater tatsächlicher Transportrecord:
`foundation/evidence/harness-transfer.json`. Noch keine Übernahme in main.

PASS bleibt am alten Subject; WS-PFR-20260917-01-F01 bleibt MINOR/OPEN mit
unveränderter ausdrücklich nichtblockierender Disposition. Der separate
WS-HARNESS-RESIDUAL-20260917-01 bleibt als historischer CONFIRMED_OPEN-Record
erhalten. Keine rückwirkende Erweiterung der Reviewfindings und keine Übertragung
des alten PASS auf den neuen Code. Nutzerübergebene Provenienz wird erhalten,
nicht als extern signiert oder erneut unabhängig authentifiziert ausgegeben.

## Implementierte Korrekturen und Reichweite

**Ausgabeschutz:** Root und build-Verzeichnis werden mit O_DIRECTORY/O_NOFOLLOW
geöffnet; Blattöffnung ist relativ zum gehaltenen Verzeichnis-FD und verwendet
O_NOFOLLOW/O_NONBLOCK ohne O_TRUNC. Vor Trunkierung prüft fstat regulären Typ und
einfachen Linkcount. Writes verwenden ausschließlich den geöffneten FD. Keine
automatische Linklöschung, kein unlink/replace eines fremden Zielpfads. Fehler
schließen FDs und führen zu fehlgeschlagenem Build. Partielle Writes werden
vollständig abgearbeitet; null Fortschritt bleibt ein Fehler.

Das schützt vorhandene/dangling Blattlinks, verlinkte Verzeichnisse und
Linkersetzung zwischen Beobachtung und Öffnung; ein nach Öffnung ersetzter
Verzeichnisname kann den FD nicht auf das Linkziel umlenken. Hardlinks und
Nicht-Regulärdateien werden vor Trunkierung abgewiesen. Grundlage sind die
[Python-os-APIs für No-follow und dir_fd](https://docs.python.org/3.14/library/os.html#os.open).
Qualifiziert: diese lokale Linux-Umgebung und Ubuntu-CI mit Python 3.14.4.
Fehlende Plattformfähigkeiten blockieren vor Ausgabe-Mutation. Kein Windows-/
Reparse-Point-PASS; keine uneingeschränkte Garantie gegen einen gleichberechtigten
feindlichen Prozess, der bereits geöffnete Verzeichnis-Inodes verschiebt oder
nach der Typprüfung weitere Hardlinks setzt. Vertrauen in Root/Workspace bleibt
Voraussetzung. Ausgabe ist regenerierbar, nicht atomar oder crash-durable;
ein I/O-Fehler kann ein unvollständiges Inventar hinterlassen und ist kein Erfolg.

**MINOR-Disposition:** Neuer Vertrag V2 beschreibt exakt
`EXPLICIT_NONBLOCKING_FOLLOW_UP: <Begründung>`. Alle OPEN/MINORs in allen drei
Reviewtypen und allen Verdicts brauchen Marker und nichtleere Begründung.
Zusätzliche Dispositionsmarker werden abgewiesen. Keine NLP-/Modellaufrufe.
Sachliche Begründung, Authentizität und textliche Widersprüche bleiben unabhängige
inhaltliche Prüfarbeit; Maschinenkonformität allein autorisiert keine Annahme.

**Vertragskompatibilität:** Resultat-Schemaversion muss zum am Subject-SHA
gebundenen V1- oder V2-Vertrag passen. Der historische V1-Vertrag bleibt unverändert.
Seine bestehende Nichtblockierungsregel wird jetzt tatsächlich durch denselben
expliziten Marker durchgesetzt, ohne Sonderausnahme für Review-ID oder SHA.
Das echte Resultat erfüllt die Regel bereits. Neue V2-Felder werden alten
Resultaten nicht hinzugefügt. Schema-Preflight vergleicht den vollständigen
jeweiligen Vertrag, nicht nur das Versionsfeld. History bleibt append-only und
unabhängig von der Anzahl legitimer Resultate.

**CI-Bindung:** PR-Checkout pinnt ausdrücklich den PR-Head, sodass Prüfungen
denselben Code wie der Delta-Review sehen. Neue Branch-Pushes mit Null-before-SHA
nutzen die im Subject deklarierte Startbaseline und weiterhin die Ancestor-/
Historyprüfung. Kein Überspringen der Prüfung und keine Änderung der read-only
Permissions, Action-/Python-Pins oder Produktgates.

## Lokale Pflichtchecks und CI

LOCAL_AGENT_REPORTED: Am unveränderten ursprünglichen Stand wurden check,
alle **23 Originaltests** und deterministischer Build ausgeführt, nach expliziter
Linkfreiheitprüfung beider Ausgabepfade. Die ursprünglichen Tests bleiben als
Regressionen erhalten; nur ihre Schemaversion wird aus dem Vertrag abgeleitet und
ein positiver MINOR-Test verwendet jetzt die erforderliche explizite Markierung.

Am korrigierten Stand umfasst die Suite **42 Tests** einschließlich 19 neuer
Testmethoden und einer Matrix mit **252 negativen MINOR-Fällen** (14 Texte ×
2 Vertragsversionen × 3 Reviewtypen × 3 Verdicts). Neue positive Fälle umfassen
das byteidentische reale Resultat, weitere legitime Historyresultate, leere
Findings und zulässig disponierte Zustände. Alte Subject-/Evidence-/Authority-
Mismatchprüfungen bleiben aktiv. Writerfälle: vorhandener/dangling Blattlink,
Verzeichnislink, Directory/FIFO/Hardlink, Berechtigungsfehler, Pfadersetzung
vor/nach Öffnung, fehlende Fähigkeiten, Short-write/I/O-Fehler und wiederholter
deterministischer Erfolg. Alle Ziele sind künstlich in temporären Verzeichnissen.

Pflichtbefehle am Kandidaten:

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build --verify-repeat
python3 tools/foundation.py validate-result --file reviews/results/WS-PFR-20260917-01.json
python3 tools/foundation.py history --base 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
python3 tools/foundation.py request --sha <CANDIDATE_SHA>
python3 tools/foundation.py schema-preflight --sha <CANDIDATE_SHA> --schema <EXACT_V2_CONTRACT_COPY>
git diff --check
```

Zusätzlich V1-Schema-Preflight am alten Subject, reale Resultatvalidierung gegen
dessen tatsächliche Git-Evidence und Historyprüfung gegen den Transfercommit;
Originalinputs/Quellen/T05-R2 werden byteidentisch mit der Baseline verglichen.
REPOSITORY_OR_REMOTE_VERIFIED: Remote-main bleibt gebunden, finaler Branchhead
ist lokal/tracking/remote identisch; konkrete SHAs und PR im Abschlusshandoff.

CI_VERIFIED wird erst bei abgeschlossenem erfolgreichen Foundation-Run mit
`head_sha == CANDIDATE_SHA` behauptet. Autoritative Run-/Job-URLs im finalen
Handoff und PR; Logs enthalten Testanzahl und deterministischen Inventarhash.
Dieses vor dem Commit verfasste Dokument erfindet keinen eigenen CI-Run-SHA.
RUNTIME_OR_OPERATION_VERIFIED: NOT_EXECUTED. Keine Browser-/Profil-, Produkt-,
AMO-, Release-, CPU-/RAM- oder Productionaktionen.

## Offene Grenzen und externer Auftrag

Implementierung und Self-Review beider Korrekturen sind lokale Evidence,
**keine unabhängige Closure**. Offen bis zum gezielten Delta-Review:
WS-PFR-20260917-01-F01 (MINOR) und Bestätigung der Korrektur des separat als
MAJOR_FOR_GENERAL_GATE_ENFORCEMENT bewerteten Residuals. Keine neue materielle
Produktentscheidung; keine Änderung T01–T05-R2 oder der Vorab-Gates.

Reviewer laden `reviews/README.md`, den V2-Vertrag und den neuen Subject am
exakten ungemergten Head. Resultatkanal bleibt `reviews/results/<REVIEW_ID>.json`;
neue Review-ID, neuer Subject, kein Edit alter Resultate. Unabhängige Prüfung
kann zugleich technische Pre-Integration-Abdeckung liefern. Auch danach ist
**separate Integrationsfreigabe** erforderlich. Dieser Coding-Agent stoppt bei
PROJECT_FOUNDATION_READY_FOR_REVIEW und führt keinen Merge/Auto-Merge aus.
