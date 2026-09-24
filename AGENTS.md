# WindowSafe: Agenteneinstieg

Zuerst [foundation/context.md](foundation/context.md), die auftragsrelevanten Originalinputs
und [Engineeringregeln](foundation/engineering.md) laden. Exakte Foundation 2:
`foundation/sources/foundation-2.md`; Foundation 1 trennt unabhängige Reviewautorität.

Aktuelle Fortsetzung: **WS-E01-F01-WIN-20260924-01**, Autorisierung **WS-EA-20260919-08**.
Original: `features/WS-E01-F01/evidence/target-authorization.json`.
Fortsetzungsstart: `7b52f6655e4478caa4864801b24877d22c33fa83`, ursprüngliche Featurebasis
`3bdd7439c221b8f8c83e7374c8bb29898891a4fd`, Branch
`feature/ws-e01-f01-qualification`. Aktueller Zustand und offene Gates:
[features/WS-E01-F01/state.json](features/WS-E01-F01/state.json),
[Bericht](features/WS-E01-F01/evidence/win-qualification.md).
Windows Desktop wurde ausgeführt; exakter 156-Neustart ist für beide OS belegt.
Windows-/Sonderfensterabgrenzung und finale Messattribution bleiben offen.
Ubuntu-Nachweise nicht auf Windows übertragen. Audit-Recovery ist abgeschlossen.
Keine Dependency-/Lock-/Toolchainversionsänderung und keine finale V6-Migration.

Nur Plattform-/Toolchain-/Messqualifikation, generischer JIT-Lifecycle, synthetische Probes
und eigene Wegwerfprofile. Kein Produktcode, F02, reales Profil, AMO/Signing/Release/Production,
Feature-Acceptance-Selbstverdikt oder Merge. Mindestens ELEVATED. Bei fehlenden Zielnachweisen
PARTIAL; keine Acceptance-Subject-Datei. Fortsetzung:
[qualification/ws-e01-f01/README.md](qualification/ws-e01-f01/README.md).

Die akzeptierte Epic Preparation bleibt unverändert READY_FOR_AGENT; historischer PASS:
`reviews/results/WS-E01-EPR-20260919-02.json`, reviewed Subject
`644b81f63dcc1990bc894a9c2c9bd8dc24a98c04`. Diese Annahme und die neue
Featureausführung sind getrennte Gates. Historische Resultate/Inputs nicht überschreiben.

Repository ist System of Record. Vor Mutation Root, Remote, Ref, HEAD, Worktree und Index
prüfen; fremde/untracked Arbeit schützen. Nur benannte Pfade stagen. Kein History-Rewrite,
Gate-Abschwächen oder Selbst-PASS. Unabhängiger technischer Review nach Qualifikationsabschluss;
Feature Acceptance und spätere Integration brauchen getrennte Freigaben.

Weitere Router: [Architektur](foundation/architecture.md), [Reviews](reviews/README.md),
[Epic Preparation](epics/README.md). Historische Reviewerumgebung und Rückläufe gelten weiterhin
nur für ihre exakt gebundenen Subjects. Dieser Lauf arbeitet ohne Agentendelegation.
