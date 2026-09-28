# WindowSafe: Agenteneinstieg

Zuerst [foundation/context.md](foundation/context.md), die auftragsrelevanten Originalinputs
und [Engineeringregeln](foundation/engineering.md) laden. Aktive finale V6 Foundation 2:
`foundation/sources/v6-final-20260918/foundation-2.md`; Foundation 1 daneben trennt
unabhängige Reviewautorität. Alte `foundation/sources/foundation-[12].md` sind historisch.

Aktueller Lauf: **WS-PFDELTA-MAT-20260928-01**, Autorisierung **WS-EA-20260928-01**.
Original: `foundation/inputs/WS-PFDELTA-MAT-20260928-01/WindowSafe_Execution_Authorization_WS-EA-20260928-01.json`.
Nur Project-Foundation-Delta ab main `3bdd7439c221b8f8c83e7374c8bb29898891a4fd`
auf `foundation/ws-pf-delta-20260928-01`. Stop: **PROJECT_FOUNDATION_READY_FOR_REVIEW**.
[Subject](foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json), [Evidence und Review-Handoff](foundation/deltas/WS-PFDELTA-MAT-20260928-01/evidence.md).
Mindestens ELEVATED; kein unabhängiges Selbst-PASS, kein Merge.

WS-P05 ergänzt Product Truth und TF r6 durch exakt gebundene Originale im Kontextrouter.
F01 / PR #3 bleibt ausschließlich externe Read-only-Evidence am Head
`7d66ca5b025c8f748d7f97b961c496ee450daaa7`, Draft/offen/ungemergt.
Keine F01-Fortsetzung, Browserprobe, Produktimplementation, F02 oder Feature Acceptance.
Nach unabhängigem Project Foundation PASS folgt zuerst der bestätigte externe
Project-Context-Sync oder eine explizit begründete NOT_APPLICABLE-Disposition,
danach WS-E01 Epic Preparation Delta, kritischer und unabhängiger Review,
exaktes Epic-Rebinding und neue F01-Ausführungsautorisierung. Hier nichts davon ausführen.

Repository ist System of Record. Vor Mutation Root, Remote, Ref, HEAD, Worktree und Index
prüfen; fremde/untracked Arbeit schützen. Nur benannte Pfade stagen. Kein History-Rewrite,
Gate-Abschwächen, Überschreiben historischer Inputs/Subjects/Reviews oder Production.
Keine Dependency-/Lock-/Toolchainversionsänderung. Keine Agentendelegation.
Weitere Router: [Architektur](foundation/architecture.md), [Reviews](reviews/README.md),
[Epic Preparation](epics/README.md). Historische Annahmen gelten nur für ihre Subjects.
