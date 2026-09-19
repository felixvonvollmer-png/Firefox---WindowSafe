# WindowSafe – begrenzte Harness-Fortsetzung nach BLOCKED

```text
HANDOFF_ID: WS-HC-20260918-01
STATUS: DRAFT__SEPARATE_EXECUTION_AUTHORIZATION_AND_BASELINE_REBIND_REQUIRED
ROLE: CODING_AGENT_AFTER_AUTHORIZATION
REPOSITORY: felixvonvollmer-png/Firefox---WindowSafe
PR: 1
BRANCH: fix/ws-hc-20260917-01
EXPECTED_CONTINUATION_HEAD: 9b6dd621deec1193bfdfbdfa730e8f9349c73fd6
EXPECTED_MAIN_AND_ORIGINAL_CORRECTION_BASELINE: 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
REVIEW_RETURN: WS-PFR-20260918-01 / BLOCKED
REVIEW_RETURN_SHA256: 0275bfcbad98bd727b861bd5b972af635139cc0986ef99eed1965331eda5f6b2
MERGE_AUTHORIZED: NO
EPIC_PRODUCT_BROWSER_OR_PRODUCTION_AUTHORIZED: NO
```

## 1. Autorität und Grenzen

Dieser Entwurf ist kein Agentenstart und keine neue Execution Authorization.
Er wird aus dem unveränderten Rücklauf und Foundation 2 §§26, 28–35 abgeleitet.
Der vorige WS-EA-20260917-02-Lauf endete am reviewbereiten ungemergten Head.
Seine Freigabe wird nicht still auf eine neue Runde ausgedehnt. Vor Ausführung ist
nur der begrenzte Fortsetzungs-/Transport-/Umgebungsumfang neu zu autorisieren.
Keine erneute Produktentscheidung, keine Änderung an T05-R2, Product Definition,
Approval, TFP r6, READY-Binding, Foundation-1/2-Bytes oder bereits gebundener Historie.

Das neue Resultat bleibt BLOCKED. Es ist kein PASS und wird nicht in
CORRECTION_REQUIRED umbenannt. Der Writer-MINOR ist darin RESOLVED für den begrenzten
POSIX/Linux-Scope; dies ist zu erhalten, nicht als vollständige Gate-Freigabe zu
verwenden. Der historische Review mit MINOR/OPEN bleibt ebenfalls unverändert.

## 2. Start und exakter Transfer nach Autorisierung

Root, Remote, Repository-ID, PR, Branch, main, HEAD, Working Tree, Index und fremde
Dateien vor jeder Mutation prüfen. Nicht zum alten Empty-Repository-Start zurückkehren.
Bei Abweichung stoppen/rebinden; kein Reset, Stash oder Force-Push fremder Arbeit.
Fortsetzung bleibt auf dem vorhandenen ungemergten Arbeitsbranch, sofern der
neu gebundene Preflight dies bestätigt. main bleibt geschützt.

Die Originaldatei results/WS-PFR-20260918-01.json dieses Pakets ist 12581 Byte lang.
Vor einem separat autorisierten Git-Transfer sind der kanonische Verbraucher am
gebundenen Subject, der V2-Vertrag, alle 18 tatsächlichen Evidence-Hashes, Autorität,
Provenienz und Ergebnislocator zu prüfen. Der Return-Processor hat diese vollständige
kanonische Konsumprüfung nicht durchgeführt. Erst bei erfolgreicher Konsumprüfung
bytegenau nach reviews/results/WS-PFR-20260918-01.json übertragen. Ein vorhandener
identischer Inhalt ist idempotent; andere Bytes bedeuten Halt, kein Überschreiben.
Ein Konsumfehler berechtigt nicht zur Payload-Änderung. Provenienz/Konsumbeleg stehen
separat, nicht als zusätzliche Felder im Originalresultat.

## 3. Korrektur A – V1 nicht nachträglich zur V2-Syntax zwingen

Finding: WS-HARNESS-RESIDUAL-20260917-01, MAJOR/OPEN.

V2 darf die exakte explizite Markierung plus Begründung weiterhin deterministisch
fordern. V1 wird nach dem unveränderten am historischen Subject gebundenen Vertrag
und dessen Nichtblockierungssemantik beurteilt. Die erst in V2 eingeführte
Präfixpflicht darf nicht rückwirkend als V1-Syntax ausgegeben werden. Insbesondere
muss der damalige positive V1-Fall `nonblocking follow-up with next-review trigger`
berücksichtigt werden. Ebenso muss das echte unveränderte historische Resultat
weiterhin zulässig sein. Keine Sonderfreistellung nach Review-ID oder Commit.

Das bedeutet nicht, wieder jeden nichtleeren V1-Text automatisch durchzulassen.
Explizit blockierende oder nicht disponierte Inhalte sind kein akzeptabler PASS.
Unklare freie V1-Texte dürfen weder blind akzeptiert noch als V2-Syntaxverletzung
umgedeutet werden; eine notwendige separate semantische Disposition ist sichtbar,
provenienz- und originalresultatgebunden zu behandeln. Keine behauptete vollständige
NLP-Prüfung oder neue LLM-/Providerabhängigkeit für jeden Validatoraufruf.
Die konkrete proportionale kompatible Lösung bleibt agent-owned.

Tests: historischer markerloser positiver V1-Fall, echtes Altresultat, V2-Markerfälle,
leere/Whitespace-/beliebige/blockierende Dispositionen, versionenabhängige Ablehnung,
offene MAJOR/BLOCKING/CRITICAL bei PASS, alle Reviewtypen und zulässigen Verdicts,
Subject-/Evidence-/Authority-Mismatch und append-only History. Ein Flag ist kein
Nachweis von Authentizität oder sachlicher Nichtblockierung.

Historischen V1-Vertrag, historischen V2-Vertrag und Resultate an ihren alten
Commits nicht überschreiben. Neue Vertragsklarstellungen, ggf. neue Version und
versionsbewusster Verbraucher, werden am neuen Commit nachvollziehbar gebunden.

## 4. Korrektur B – Null-before-Startbasis unabhängig verifizieren

Finding: WS-PFR-20260918-01-F01, MAJOR/OPEN.

Im first-push-Fallback darf das aktuelle veränderliche Subject nicht allein wählen,
gegen welchen historischen Zustand geschützte Dateien verglichen werden. Die
Startbasis wird gegen eine unabhängig vom aktuellen Subject-Endstand gebundene
Autorisierungs-/Handoff-Quelle geprüft. Ein Selbstvergleich mit HEAD reicht nicht;
ebenso reicht kein beliebiger späterer Ancestor.

Wichtige Unterscheidung: Der nächste Lauf beginnt auf 9b6dd621deec1193bfdfbdfa730e8f9349c73fd6,
aber der vorangegangene vollständige Korrekturdelta begann auf 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109.
Ein Rebind des nächsten Ausführungslaufs darf die bisher unakzeptierte Strecke
nicht unsichtbar machen. Sowohl die neue Laufbaseline als auch die kumulative
Review-/Historienbaseline sind mit ihrem jeweiligen Zweck zu erhalten.

Tests müssen den tatsächlichen Kommando-/Fallbackpfad einschließen: erlaubte
gebundene Basis, manipuliertes HEAD beziehungsweise nicht autorisierter Ancestor,
fehlende/ungültige Bindung, geschützte Datenänderung/-löschung und legitime additive
Resultate. Root-Bootstrap, spätere Push-/PR-Basis und vollständige History dürfen
nicht durch einen Spezialfall oder einen hardcodierten Historycount ersetzt werden.
Die konkrete minimale Bindungsstrategie ist agent-owned; neue Credential- oder
Administrationsrechte sind dafür nicht freigegeben.

## 5. Writer erhalten, keine unnötige Neuimplementierung

Die bereits im Rücklauf technisch bestätigte Writer-Korrektur und ihre Tests bleiben
Regressionsevidence. Keine erneute Neuentwicklung ohne neue relevante Evidenz.
POSIX/Linux-Qualifikation, fail-closed Verhalten auf ungeprüften Plattformen sowie
fehlende Windows-/Reparse-/Atomizitäts-/Crash-Durability-Zusage bleiben ausdrücklich.
Dies ändert keine späteren Firefox-Produktzielplattformen.

## 6. Reviewer-Umgebung und neuer Kandidat

WS-PFR-20260918-01-F02 ist ein separater Ausführungsblocker, kein Auftrag zur
Lockerung des Python-Pins oder zur Ersetzung unabhängiger Prüfungen durch CI.
Den separaten Entwurf WS-REVENV-20260918-01 beachten. Die Umgebung wird vor dem
nächsten fachlichen Review auf Git-Objektzugriff und unveränderte Kommandos mit
gepinntem Python geprüft. Implementierertests sind kein unabhängiger Reviewer-Nachweis.

Am neuen Kandidaten: ursprüngliche und ergänzte Tests, Lint/Guards, Build,
Versions-/Vertrags-Preflight, historische Resultatkonsistenz und History tatsächlich
unter der gebundenen Umgebung ausführen; neue CI exakt an den neuen Head binden.
Subject, Correction-Disposition und Evidence bilden den neuen Stand ab. Die
früheren BLOCKED-/PASS-Dateien und ihre Aussagen bleiben unangetastet.

Risikofloor ELEVATED. Ende: getesteter ungemergter Candidate mit vollständigem
Reviewlocator und bereitgestelltem Reviewer-Ausführungskontext, dann STOP.
Keine selbst erteilte externe Closure, kein Merge, kein Epic/Feature, kein Browser.
Danach ein neuer gezielter unabhängiger Review mit erfolgreichem Preflight zuerst;
kein weiterer Voll-Preparation-Review unveränderter Produkt-/TFP-Unterlagen.
Auch nach PASS bleibt die Integration separat zu autorisieren.
