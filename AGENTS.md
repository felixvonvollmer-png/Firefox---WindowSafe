# WindowSafe: Agenteneinstieg

Zuerst [foundation/context.md](foundation/context.md), die auftragsrelevanten Originalinputs
und [Engineeringregeln](foundation/engineering.md) laden. Aktive finale V6 Foundation 2:
`foundation/sources/v6-final-20260918/foundation-2.md`; Foundation 1 daneben trennt
unabhängige Reviewautorität. Alte `foundation/sources/foundation-[12].md` sind historisch.

Project Foundation Delta **WS-PFDELTA-MAT-20260928-01** ist angenommen: unabhängiges
[WS-PFR-DELTA-20260928-01 PASS](reviews/results/WS-PFR-DELTA-20260928-01.json) am
reviewed Head `bbca750fab1e760714cf409b8751287db6b93041`, integriert durch
**WS-PFDELTA-INT-20260929-01** unter [WS-EA-20260929-01](foundation/evidence/pf-delta-integration-authorization.json).
[Acceptance-Binding](foundation/deltas/WS-PFDELTA-MAT-20260928-01/binding.json); der
[reviewed Subject](foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json) bleibt unverändert.
Externer Project-Context-Sync: **CONFIRMED_BY_USER** (WS-EXTCTX-SYNC-20260929-01, separater
Record im Epic-Delta; das Foundation-Binding bleibt unverändert).

**Aktuelles Gate:** WS-E01-EP-DELTA-20260929-02 erhielt das unabhängige
WS-E01-EPR-DELTA-20260929-01 **CORRECTION_REQUIRED**
(`reviews/results/WS-E01-EPR-DELTA-20260929-01.json`) und bleibt historisch unverändert. Der korrigierte Subject **WS-E01-EP-DELTA-20260929-03**
(WS-E01-EPDELTA-CORR-20260929-01 unter WS-EA-20260929-03) ist
**EPIC_PREPARATION_DELTA_CORRECTED_READY_FOR_REREVIEW**: Subject
`epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/subject.json`, Binding REVIEW_REQUIRED,
drei review-ausschließende Autorenidentitäten. Das historische WS-E01-Binding bleibt
unverändert und autorisiert kein F01. Danach frischer unabhängiger Rereview, exaktes
Rebinding, separate breite WS-E01-Autorisierung.

WS-P05 ergänzt Product Truth und TF r6 durch exakt gebundene Originale im Kontextrouter.
F01 / PR #3 bleibt ausschließlich externe Read-only-Evidence am Head
`7d66ca5b025c8f748d7f97b961c496ee450daaa7`, Draft/offen/ungemergt; F01 ist gestoppt.
Keine F01-Fortsetzung, Browserprobe, Produktimplementation, F02 oder Feature Acceptance
ohne diese späteren Gates. Hier nichts davon ausführen.

Repository ist System of Record. Vor Mutation Root, Remote, Ref, HEAD, Worktree und Index
prüfen; fremde/untracked Arbeit schützen. Nur benannte Pfade stagen. Kein History-Rewrite,
Gate-Abschwächen, Überschreiben historischer Inputs/Subjects/Reviews oder Production.
Keine Dependency-/Lock-/Toolchainversionsänderung. Keine Agentendelegation.
Weitere Router: [Architektur](foundation/architecture.md), [Reviews](reviews/README.md),
[Epic Preparation](epics/README.md). Historische Annahmen gelten nur für ihre Subjects.
