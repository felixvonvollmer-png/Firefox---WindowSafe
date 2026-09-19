# WindowSafe – autorisierter Codex-Folgeauftrag WS-HC-20260918-01

STATUS: AUTHORIZED_EXECUTION_HANDOFF__PREFLIGHT_REQUIRED
ROLE: CODING_AGENT_EXISTING_HARNESS_FOLLOWUP_ONLY
AUTHORIZATION: WindowSafe_Execution_Authorization_WS-EA-20260918-01.json@sha256:f3f0c51070e51974bfc6979e5db4ead2cdfa131315c0654ebad8773e467320ed
REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
BRANCH: fix/ws-hc-20260917-01
PR: 1 / DRAFT / UNMERGED
RUN_START_HEAD: 9b6dd621deec1193bfdfbdfa730e8f9349c73fd6
CUMULATIVE_REVIEW_AND_HISTORY_BASELINE: 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
EXPECTED_MAIN: 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
MERGE_AUTHORIZED: NO

## 1. Maßgebliche Inputs und Freigabe

Lies zuerst die oben exakt gebundene neue Execution Authorization und prüfe das
äußere SHA256SUMS.json. Unter return/ liegen alle Dateien des vorigen Rücklaufpakets
bytegleich, einschließlich seines eigenen Manifests. Die ursprünglichen Entwürfe
bleiben historische Evidence ihrer damaligen Nichtfreigabe; die neue Autorisierung
setzt den darin beschriebenen begrenzten Fortsetzungsumfang jetzt frei. Sie ändert
weder deren Bytes noch Product Truth oder ein Reviewresultat.

Verbindlicher Korrekturumfang:
`return/WindowSafe_Harness_Followup_WS-HC-20260918-01_DRAFT.md`
SHA-256 `77f91ef8333959c6e69c2af510600101fc3fcd241fd5b5be49eee475967582f7`.
Die vollständigen Abschnitte 2–6 einschließlich der Testanforderungen gelten.
Das ist kein Mikroplan für Klassen/Funktionen oder neue Produktarchitektur.

Reviewpayload:
`return/results/WS-PFR-20260918-01.json`
SHA-256 `0275bfcbad98bd727b861bd5b972af635139cc0986ef99eed1965331eda5f6b2` / 12581 Byte.
Verdict bleibt BLOCKED. Nicht neu formatieren, umdeuten, kürzen oder ergänzen.

Umgebungsvorbereitung:
`WindowSafe_Reviewer_Environment_WS-REVENV-20260918-01_AUTHORIZED_PREPARATION.md`
SHA-256 `263a209c0a8233e72fec5020fe5cdb2716f9a4d07c2b3c3b862d104e62a5428d`.
Sie ist autorisiert, aber noch nicht tatsächlich qualifiziert. Der spätere
unabhängige Reviewer muss die Originalkommandos selbst ausführen.

Lade den übrigen kanonischen Kontext aus dem Repository am Laufstart: AGENTS.md,
foundation/context.md, foundation/engineering.md, reviews/README.md,
reviews/review-contract.json, foundation/subject.json und die dortigen Inputs.
Foundation-1-Blob: 3b139a7dfd70da3ae6c83bbdfa703cb98ef94193.
Foundation-2-Blob: ff49e56aba09881e9e4a22dc8225949fbc4b54f6.
Gitidentitäten prüfen; unveränderte High-Level-Discovery nicht wiederholen.

## 2. Startprüfung und zulässige Writes

Dieser Auftrag setzt auf dem vorhandenen Arbeitsbranch/PR fort. Kein erneuter
Empty-Repository-Bootstrap. Repo-ID 1374094477, öffentliche Sichtbarkeit, main,
Branchhead und PR-Zustand unmittelbar vor der ersten Mutation erneut prüfen.
PR muss offen, ungemergt und Draft sein; Auto-Merge darf nicht aktiviert sein.
Root/Remote/HEAD/Index/Worktree/untracked und fremde Änderungen prüfen. Unbekannte
Drift bedeutet Halt vor dem betroffenen Write, nicht Reset/Stash/Rebase/Force-Push.

Danach nur die nötigen Änderungen an Harness, Tests, Vertrag, Evidence, Kontext,
CI und neuem Subject; neue Commits als Fast-forward auf demselben Branch, PR als
Draft aktualisieren, erforderliche CI ausführen. Kein main-Write und kein Merge.
Keine automatische Fortsetzung nach dem Endbericht dieses Laufs.

## 3. Review-Transfer zuerst tatsächlich konsumieren

Vor dem Transfer unter echter CPython 3.14.4 mit vollständiger Git-Lesekopie den
Originalverbraucher am alten Subject 9b6dd621deec1193bfdfbdfa730e8f9349c73fd6 benutzen.
request, vollständigen V2-Vertrag und schema-preflight sowie validate-result
wirklich ausführen; alle 18 Evidence-Hashes, Authority-/Provenienz-/Locatorbindung
prüfen. Eigene Logs getrennt festhalten. Vorhandene grüne CI allein genügt nicht.

Der bisherige Return-Processor hat die vollständige Originalausführung nicht
belegt. Ein Fehler erlaubt weder Payload-Korrektur noch Verbraucher-Abschwächung.
Nach Erfolg bytegenauer Transfer nach `reviews/results/WS-PFR-20260918-01.json` auf den
Arbeitsbranch und tatsächlicher Git-Byteabgleich. Identischer vorhandener Inhalt
ist idempotent, andere Bytes sperren den Transfer. BLOCKED bleibt BLOCKED; dieser
Konsum ist kein unabhängiger Review und schließt F02 nicht rückwirkend.

## 4. Zwei Korrekturen und Erhalt des Writer-Fixes

**V1/V2:** V2 darf seine definierte Markerpflicht erzwingen. V1 darf nicht nachträglich
an V2-Syntax gebunden werden; der damalige markerlose positive Fall
`nonblocking follow-up with next-review trigger` und das echte historische Resultat
müssen nach ihrer alten Bindung berücksichtigt werden. Keine ID-/SHA-Ausnahme und
kein Rückfall auf „beliebiger nichtleerer Text genügt“. Unklare freie V1-Dispositionen
benötigen die im Entwurf beschriebene sichtbare, originalevidenz-/provenienzgebundene
semantische Behandlung. Keine NLP-/Providerpflicht pro Validatoraufruf. Konkrete
proportionale Lösung und nötige prospektive Vertragsversion sind agent-owned.

**History:** Der first-push-Fallback darf seine Vergleichsbasis nicht allein aus dem
veränderlichen eigenen Subject wählen. Prüfe sie gegen eine unabhängig gebundene
Autorisierungs-/Handoffquelle. Neue Laufbaseline 9b6dd621deec1193bfdfbdfa730e8f9349c73fd6
ist nicht die kumulative History-/Reviewbaseline 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109.
Beide Prüfstrecken bleiben sichtbar. Negative CLI-/Fallbacktests für HEAD als Basis,
falsche Ancestors, fehlende/ungültige Bindung und manipulierte geschützte Dateien;
legitime additive History und echte Root-/Push-/PR-Fälle bleiben zulässig.

Der im BLOCKED-Rücklauf für POSIX/Linux als RESOLVED geführte Writer-Fix bleibt
inklusive Tests erhalten. Keine Neuentwicklung ohne neue relevante Evidence.
Keine Windows-/Reparse-, Atomizitäts- oder Crash-Durability-Zusage hinzufügen.

Die alten PASS-/BLOCKED-Resultate und die darin enthaltenen Status bleiben exakt.
Neue Korrektur-Evidence darf IMPLEMENTED_PENDING_INDEPENDENT_CONFIRMATION nennen,
aber keine selbst erteilte externe Closure oder PROJECT_FOUNDATION_ACCEPTED.

## 5. Reviewumgebung und Ende

Bereite eine isolierte Umgebung mit echter CPython 3.14.4 und verifizierbaren
Gitobjekten für den späteren unabhängigen Reviewer vor. Liefere tatsächliche
Setup-/Zugriffsbelege und Wiederholungsbefehle; kein bloßes Checklisten-PASS.
Fehlende Fähigkeiten oder verbotene nötige Rechte/Kosten bleiben ein gemeldeter
Blocker. Eigene Implementiererchecks sind keine Reviewer-Ausführung.

Am neuen Head alle unveränderten und ergänzten Pflichtchecks ausführen: Tests,
Lint/Guards, deterministischer Build, Versions-/Schema-Preflight, Altresultatkonsum
und History. CI muss genau diesen Kandidaten prüfen; Git-/Inputschutz nicht
abschwächen. Gepinnte und tatsächliche Umgebung sowie Evidenzklasse benennen.

Liefere den exakten neuen Head/Tree, PR und main, Diffumfang, Tests/CI, offene
Findings, Reviewer-Umgebung und kanonischen Subject-/Evidence-/Resultatlocator.
Risikofloor ELEVATED. Ziel ist ausschließlich ein getesteter ungemergter
PROJECT_FOUNDATION_READY_FOR_REVIEW-Kandidat samt vorbereitetem Ausführungskontext.
Dann STOP. Keine unabhängige Abnahme, kein Merge/Auto-Merge, keine Epic-/Produkt-,
Browser-/Profil-, AMO- oder Productionarbeit. Neuer unabhängiger Reviewauftrag und
spätere Integration bleiben getrennt; kein nochmaliger Voll-Preparation-Review
unveränderter Produkt-/TFP-Unterlagen.
