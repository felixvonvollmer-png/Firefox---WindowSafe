# WindowSafe – begrenzter Harness-Korrekturauftrag

```text
HANDOFF_ID: WS-HC-20260917-01
STATUS: PREPARED__AWAITING_SEPARATE_EXECUTION_AUTHORIZATION
ROLE_AFTER_AUTHORIZATION: CODING_AGENT
SCOPE: EXISTING_PROJECT_FOUNDATION_HARNESS_CORRECTION_ONLY
TARGET_REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
BASELINE_SHA: 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
BASELINE_TREE: 2cdf2d0484463c9639d924f0aa239499637e941b
REVIEW_RESULT: reviews/results/WS-PFR-20260917-01.json
REVIEW_RESULT_SHA256: c4c908eb70c99252f185ee89d077919ecc9598cc2842b2f0b1209734f115c19f
NORMAL_PRODUCT_FEATURES: PROHIBITED
EPIC_START: PROHIBITED
AUTOMATIC_MERGE: NOT_AUTHORIZED
```

**Dieses Dokument ist ein vorbereiteter Auftrag, keine neue Ausführungsfreigabe.**
Die Bootstrap-Autorisierung WS-EA-20260917-01 war auf das damals leere Repository
und den initialen Lauf bis PROJECT_FOUNDATION_READY_FOR_REVIEW gebunden. Sie darf
nicht als unbegrenzte Fortsetzungs- oder Merge-Autorisierung ausgelegt werden.
Der Projekt-LLM hat hier keine Repository-Korrekturen implementiert.

## Anlass und unveränderte Autorität

Der unabhängige WS-PFR-20260917-01 ist PASS für den obigen Commit, mit offenem,
ausdrücklich nichtblockierendem MINOR WS-PFR-20260917-01-F01. Er bleibt vollständig
unverändert. Daneben steht der separat vom Nutzer gemeldete und durch
Komponentenprüfungen bestätigte WS-HARNESS-RESIDUAL-20260917-01. Dieser neue Befund
wird nicht nachträglich in das Reviewresultat eingefügt.

Maßgeblich sind die aktuellen Git-Quellen am Baseline-SHA:
`foundation/sources/foundation-1.md` (Blob 3b139a7dfd70da3ae6c83bbdfa703cb98ef94193),
`foundation/sources/foundation-2.md` (ff49e56aba09881e9e4a22dc8225949fbc4b54f6),
`foundation/context.md`, `foundation/engineering.md`, `reviews/README.md`,
`reviews/review-contract.json` und die exakt gebundenen Inputs. Alte Chats sind
keine zusätzliche kanonische Product Truth. Das beigefügte Rücklaufprotokoll
liefert Herkunft, Hash des vollständig dekodierten Resultats und Prüfgrenzen.

## Freizugebender Ausführungsumfang

Nach ausdrücklicher separater Autorisierung: exakte Resultatübernahme, additive
Befund-/Statusdokumentation, enger Fix des bestehenden Harness mit zugehörigen
Tests/Vertragsklarstellungen, kurzer Branch/PR und CI. Die Freigabe muss den
aktuellen Ausgangscommit, vorhandene Agentenumgebung sowie konkrete Write-/Push-/
CI-Rechte binden. Kein Force-Push, keine fremden Änderungen, Admin-/Secretänderung,
neuer Provider, neue Kosten, Browserprofile, AMO, Veröffentlichung oder Produktion.
Kein Merge vor hinreichendem unabhängigen Review und separater Mergeberechtigung.

Unmittelbar vorher Root, Remote, HEAD, Worktree, Index, untracked Dateien,
Repoidentität und Remote-main prüfen. Bei Drift weder auf das alte EMPTY-Schema
zurückfallen noch fremde Arbeit zurücksetzen. Baselineabweichungen ausdrücklich
disponieren/rebinden. Ein bereits vorhandener Ergebnislocator darf nur bei
Bytegleichheit als identischer bereits erfolgter Transfer behandelt werden;
abweichende Bytes blockieren, kein Überschreiben.

## Korrekturziele – keine Implementierungsmikroplanung

**A. Ausgabe-Sicherheit (bestehender MINOR).** Der Inventar-Writer darf keine
vorhandene symbolisch verknüpfte Ausgabedatei verfolgen oder dadurch ein anderes
Ziel überschreiben/erzeugen. Ausgabeordner und Blattpfad müssen geschützt sein;
ein bloßes Vorab-is_symlink mit anschließend ungeschütztem Folgen ist bei einer
möglichen Pfadersetzung keine ausreichende allgemeine Sicherheit. Die konkrete
sichere Schreibstrategie und ihre Plattformgrenzen sind agent-owned. Keine
behauptete Vollsicherheit über unqualifizierte Umgebungen.

Tests mindestens für vorhandenen Ausgabe-Dateisymlink zu einer synthetischen
Datei außerhalb des Testrepos, dangling link, verlinkten Ausgabeordner, ungeeignete
Zieltypen/Fehler sowie erfolgreichen wiederholten deterministischen Build am
zulässigen Ausgabeort. Außerhalb liegende synthetische Ziele bleiben nach dem Fix
unverändert beziehungsweise werden nicht erzeugt. Tests dürfen keine realen
Nutzerdateien verwenden. Bis zur Korrektur nur ausdrücklich geprüfte linkfreie
Ausgabeorte; keine automatische Löschung eines vorgefundenen fremden Links.

**B. Dispositionsvertrag (separater Residual).** OPEN + MINOR darf nicht allein
wegen eines nichtleeren Dispositionstextes mechanisch als vertragskonform gelten.
Der kanonische Vertrag und der Validator müssen eine ausdrücklich nichtblockierende
Disposition eindeutig prüfbar repräsentieren. Eine kleine definierte Markierung
mit Begründung oder eine strukturierte Repräsentation sind mögliche Richtungen,
keine vorgegebene Datenmodellentscheidung. Keine neue LLM-/NLP-Prüfung für jeden
Validatoraufruf. Keine willkürliche Textannahme oder Entfernung der Vertragsregel.

Negative Fälle: leer, Whitespace, beliebiger Follow-up-Text ohne explizite
Nichtblockierung, explizit blockierende Disposition sowie ungültige/mehrdeutige
Maschinenkennzeichnung. Positiv: explizit nichtblockierende Disposition mit
Begründung; insbesondere das unveränderte echte Resultat WS-PFR-20260917-01.
OPEN MAJOR/BLOCKING/CRITICAL bei PASS bleiben auch mit Nichtblockierungskennzeichen
unzulässig. Alle drei Reviewtypen, leere Findings, zulässig disponierte Zustände,
History und Subject-/Evidence-/Authority-Mismatches mitprüfen.

Maschinelle Kennzeichnung beweist weder Revieweridentität noch sachliche
Nichtblockierung. Authentizität, Begründung und widersprüchliche Aussagen bleiben
zusätzlich inhaltlich zu prüfen. Keine Voll-Natural-Language-Semantik versprechen.

## Historien- und Vertragskompatibilität

Originalresultat, frühere Subjects und sämtliche `foundation/inputs/`- und
`foundation/sources/`-Bytes bleiben unverändert. Die aktuelle lokale Transferdatei
wird, nach Autorisierung, vollständig nach `reviews/results/WS-PFR-20260917-01.json`
übernommen; nicht nur das Verdict oder eine Zusammenfassung. Dekodierung und
Transportprovenienz bleiben separat, nicht als neue Felder im Reviewpayload.

Neue Vertragsdetails werden am neuen Commit dokumentiert. Wird die Struktur
versioniert, sind versionsbewusste Konsumregeln nötig; alte gültige Resultate
werden nach ihrem exakt gebundenen Vertrag plus dessen tatsächlicher Semantik
beurteilt, nicht nach zufälligen aktuellen Feldern und nicht durch eine pauschale
Altfall-Freistellung. Den historischen Vertrag nicht rückwirkend ändern.

Nur die betroffenen Harness-/Test-/Reviewkanal-/Evidence-/Status-/Subjectdateien
im neuen Changeset bearbeiten. Ein neuer Project-Foundation-Subject samt neuer
Evidence/Commitbindung repräsentiert den korrigierten Stand. Kein Selbst-PASS und
kein Übertragen des alten PASS auf den neuen Code. Historische PENDING-Felder
oder offene Befunde im ursprünglichen Commit werden nicht rückwirkend bereinigt;
eine spätere Annahme-/Closure-Aussage ist ein separates gebundenes Artefakt.

Product Definition/Approval, TFP r6, READY-Binding, T01–T05-R2, CPU-Grenzen,
Safety-Invarianten und Plattform-/Mess-Vorabgates ändern sich nicht. Kein neuer
Preparation-Subject, keine neue T05-Entscheidung und kein wiederholter vollständiger
Preparation-Review sind für diesen reinen Harness-Fix erforderlich.

## Prüfnachweise und Stop

Mit gepinnter Python-Umgebung die originalen und neuen Tests, Lint/Guards,
deterministischen Build, Schema-Preflight und History/Konsumprüfung tatsächlich
laufen lassen; lokale, CI- und Komponenten-Evidence trennen. Neue CI an den genauen
Korrektur-/PR-Head binden. Kein behaupteter Erfolg bei fehlendem Pflichtcheck.
Den Validator nicht abschwächen, damit ein alter oder neuer aktiver Fall grün wird.

Der kombinierte Fix wird wegen Review-Vertrauensgrenze und Ausgabeschreibpfad
mindestens als ELEVATED behandelt: unabhängige technische Reviewabdeckung vor
Integration. Diese kann in einem gezielten unabhängigen PROJECT_FOUNDATION_REVIEW
für den neuen Commit einschließlich Delta, Tests und History-Kompatibilität
zusammengeführt werden; kein zweiter identischer Vollreview nur aus Formalität.
Scope erweitert sich nur bei neuer relevanter Evidence.

**Ende dieses vorgeschlagenen Coding-Laufs:** korrigierter, getesteter exakter
Branch-/PR-Head mit reviewbereitem Subject, Evidence, aktuellem Risikostatus und
kanonischem Reviewlocator; danach STOP. Kein selbst geschlossener externer Befund,
kein automatischer Merge, kein Epic/Feature/Browserstart.

Nach unabhängig akzeptiertem Korrekturstand und autorisierter Integration folgt
der kanonische Kontextabgleich (hier begründet NOT_APPLICABLE für einen externen
installierten Projekttext) und FIRST_EPIC_PREPARATION. Auch danach gelten die
separaten Epic-Review-/Execution- und Plattform-/Messgates.
