# WindowSafe – autorisierter Codex-Handoff für WS-HC-20260917-01

```text
HANDOFF_ID: WS-HC-20260917-01
HANDOFF_REVISION: 2
STATUS: AUTHORIZED_FOR_CODING_AGENT_EXECUTION
AUTHORIZATION_ID: WS-EA-20260917-02
SCOPE: REVIEW_TRANSFER_AND_EXISTING_FOUNDATION_HARNESS_CORRECTION_ONLY
BASELINE_SHA: 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
WORK_BRANCH: fix/ws-hc-20260917-01
STOP_STATE: PROJECT_FOUNDATION_READY_FOR_REVIEW_ON_UNMERGED_CORRECTION_HEAD
MERGE_AUTHORIZED: NO
PRODUCT_OR_EPIC_START_AUTHORIZED: NO
```

## Verbindliche Eingänge

Lies zuerst `WindowSafe_Execution_Authorization_WS-EA-20260917-02.json` (SHA-256 `25f0ee35f9cafe89230f47e218d31a43c2aecb57f4f67446008c4a8c4eb3e0ab`). Es dokumentiert das aktuelle
Nutzerwort „frei“ im eindeutigen Kontext dieses begrenzten Folgeauftrags.
Die alte Bootstrap-Autorisierung ist keine neue Freigabe für dieses Inkrement.

Der vollständige fachliche Korrekturumfang steht unverändert in
`review-return/WindowSafe_Harness_Correction_Handoff_WS-HC-20260917-01_DRAFT.md` (SHA-256 `83fee934ec31863b808af771481fcda6d65954b74e62628c1b73e8e24d61bffe`). Dessen damalige Formulierungen
„awaiting authorization“ und „vorgeschlagen“ bleiben historische Metadaten.
Erst diese separate neue Execution Authorization gibt den dort beschriebenen Lauf frei;
sie verändert weder Product Truth noch alte Reviewresultate. Keine neue Epic Preparation
und kein erneuter kompletter Technical-Preparation-Review werden dadurch vorgezogen.

Das vollständige zu transportierende Reviewpayload liegt in `review-return/results/WS-PFR-20260917-01.json`
(SHA-256 `c4c908eb70c99252f185ee89d077919ecc9598cc2842b2f0b1209734f115c19f`, 10136 Byte).
Es bleibt `PASS` für `4ba2c473fe4d90c85d94ee2b2f5cc5777d115109` mit seinem offenen,
ausdrücklich nichtblockierenden MINOR. Der neue Validator-Residual steht separat in
`review-return/WindowSafe_Harness_Residual_WS-HARNESS-RESIDUAL-20260917-01.json` (SHA-256 `694ac89f40e9246ee8eb4c79b4a5f5712e0079270258fdc90529abe95d223a18`).
Der Rücklauf-/Dekodierungsrecord `review-return/WindowSafe_Review_Return_WS-PFRRETURN-20260917-01.json` und dessen gebundene Dateien erläutern
Herkunft und Grenzen; sie sind keine zusätzlichen unabhängigen Reviewverdikte.

## Kanonischer Kontext und Startprüfung

Ziel: `felixvonvollmer-png/Firefox---WindowSafe`, Repository-ID `1374094477`, öffentlich.
Die aktuelle Read-only-Beobachtung ist `WindowSafe_Repository_Baseline_WS-RB-20260917-02.json`.
Vor dem ersten Write sind Remote-main, Root/Remote/HEAD/Index/Worktree/untracked Dateien
und Branch-/Pfadkollisionen erneut zu prüfen. Die erwartete Baseline ist nicht mehr leer.
Bei unzugeordneter Drift stoppen statt fremde Arbeit zurückzusetzen.

Lade am gebundenen Baseline-Commit `AGENTS.md`, `foundation/context.md`,
`foundation/architecture.md`, `foundation/engineering.md`, `reviews/README.md`,
`reviews/review-contract.json`, `foundation/subject.json` und die nötigen Originalinputs.
Maßgebliche Rollenquellen sind `foundation/sources/foundation-1.md` mit Git-Blob
`3b139a7dfd70da3ae6c83bbdfa703cb98ef94193` und `foundation/sources/foundation-2.md`
mit Git-Blob `ff49e56aba09881e9e4a22dc8225949fbc4b54f6`. Prüfe ihre Blobidentität.
Die Quellkopien im Rücklaufpaket sind historische Evidence, kein Ersatz für das
Verifizieren der tatsächlich bearbeiteten Git-Baseline.

## Erlaubte Arbeit und Ergebnis

Führe nach Preflight beide Korrekturziele des gebundenen Drafts autonom aus:
Ausgabe-Blattpfad/Ordner gegen unzulässige Linkverfolgung absichern und den expliziten
Nichtblockierungsvertrag für offene MINORs konsistent durchsetzen. Dazu gehören die
positiven/negativen Regressionen, History-/Altresultat-Kompatibilität, passende
Vertragsklarstellungen und exakt gebundene Korrektur-Evidence. Keine Mikroplanung
von Klassen, Funktionen oder Commitreihenfolgen durch diesen Handoff.

Das vollständige Resultat wird bytegenau auf dem Arbeitsbranch unter
`reviews/results/WS-PFR-20260917-01.json` übernommen, inklusive seiner unveränderten
Provenienz und Finding-Disposition. Nicht noch einmal formatieren oder dekodieren.
Vorhandene abweichende Bytes blockieren; identische Bytes machen einen erneuten
Transfer unnötig. Die echte Übernahme mit Hash und Autorisierung separat dokumentieren.
Eine Übernahme auf dem Arbeitsbranch ist noch keine Integration in `main`.

Die neue Autorisierung und notwendige Transport-/Befundprovenienz gehören getrennt
von den alten unveränderlichen `foundation/inputs/`- und `foundation/sources/`-Bytes
in angemessene Foundation-Evidence-Artefakte. Keine gesamte Paketkopie in die aktive
Foundation und keine Änderung des alten Inputmanifests, nur um neue Dateien aufzunehmen.

Branch-Commits/Push, ein PR gegen `main` und CI sind im begrenzten Scope autorisiert.
Vor jeglichem Aufruf des noch unkorrigierten Writers den Ausgabeort einschließlich
Blattpfad auf Linkfreiheit prüfen. Keine fremden Links oder Dateien automatisch löschen.
Gepinnte Original- und neue Tests, Lint/Guards, Build, Schema-Preflight sowie die erneute
Prüfung des unveränderten echten Resultats und der History ausführen. Test- und
CI-Claims an den tatsächlichen Kandidaten binden; keine Version-/Gate-Umgehung.

**Danach STOP am getesteten, noch nicht integrierten Branch-/PR-Head.** Liefere exakten
SHA, PR, CI, neue Subject-/Evidence-/Reviewvertrags-Locators, Prüfgrenzen und Findings.
Die beiden Korrekturen dürfen als implementiert und selbst geprüft berichtet werden;
die unabhängige Closure wird nicht durch den Coding-Agenten ausgestellt.

Mindestens ELEVATED: unabhängiger gezielter Foundation-/Harness-Delta-Review vor Merge.
Der spätere Reviewer darf die alte Foundation-Prüfung für unveränderte Bereiche nutzen,
muss aber den neuen Changeset und die Verträglichkeit tatsächlich prüfen.
**Auch ein späterer PASS löst in diesem Auftrag keinen Merge aus.** Dafür braucht es
anschließend eine separate Integrationsfreigabe. Kein Epic, Produktfeature, Firefox-/
Profiltest, keine Änderung der CPU-Ziele, kein Release und kein Providerwechsel.
