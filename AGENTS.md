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

**Aktuelles Gate:** Historisch: -02 erhielt WS-E01-EPR-DELTA-20260929-01 **CORRECTION_REQUIRED**,
-03 (`dee7ab5c9c5b53accd8602105e87523510582e40`) erhielt WS-E01-EPR-DELTA-20260929-02 **BLOCKED**
und die nutzerautorisierte Ersatz-Evidence WS-E01-EPR-DELTA-20260930-04 **CORRECTION_REQUIRED**
(`RECONSTRUCTED_FROM_REVIEW_TRANSCRIPT`; das Original -20260929-03 ist verloren). Aktuell:
**WS-E01-EP-DELTA-20260929-04** (WS-EA-20260930-01) am reviewed Head
`fa109e1b2cea025918d1cff61a2aaee2ee2b2083` erhielt das unabhängige WS-E01-EPR-DELTA-20260930-05
**PASS**. Exaktes Rebinding READY_FOR_AGENT:
`epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/rebinding.json` unter WS-EA-20260930-02 (der
Pending-Binding und das historische WS-E01-Binding bleiben unverändert), integriert in main
`714b440c26167f6411420fbbda4be69deb2e9670`. Separate breite WS-E01 Execution Authorization
WS-EA-20261001-03: `epics/WS-E01/evidence/broad-execution-authorization.json` (autonom
F01 -> F02 -> {F03,F04} -> F05 bis EPIC_CONVERGED, dann STOP; kein Folge-Epic). Ausstehend:
Nutzerentscheidung WS-UD-20261003-01 (`epics/WS-E01/evidence/user-decision-ws-ud-20261003-01.json`,
Windows ohne Performance-Nachweis) wirkt erst nach TF-Delta, Review und Binding; bis dahin sind die
Windows-Messarbeiten pausiert und die bisherige Bindung gilt.

WS-P05 ergänzt Product Truth und TF r6 durch exakt gebundene Originale im Kontextrouter.
F01 / PR #3 bleibt ausschließlich externe Read-only-Evidence am Head
`7d66ca5b025c8f748d7f97b961c496ee450daaa7`, Draft/offen/ungemergt (historisch).
Ab WS-EA-20261001-03 wird F01 auf neuer Basis fortgesetzt (PR #3 bleibt Read-only-Evidence).
Produktimplementation erst hinter den gebundenen Plattform-/Messgates (TF §7.1, §§9.1/9.3);
Browserproben nur in künstlichen Wegwerfprofilen; Feature Acceptance nur durch frische
unabhängige Reviewer mit vollständiger Autoren-Ausschlussmenge.

Repository ist System of Record. Vor Mutation Root, Remote, Ref, HEAD, Worktree und Index
prüfen; fremde/untracked Arbeit schützen. Nur benannte Pfade stagen. Kein History-Rewrite,
Gate-Abschwächen, Überschreiben historischer Inputs/Subjects/Reviews oder Production.
Während Review-/Correction-Transporten kein Dependency-/Toolchain-Drift; nach gültigem Epic
Rebinding JIT innerhalb Product Truth/TF (Lizenz, Provenienz, Supply Chain, Reproduzierbarkeit).
Worker/Subagenten/Reviewer JIT im gebundenen Scope (WS-EA-20260930-01, WS-EA-20261001-03); unabhängige Verdicts
nur aus frischem/isoliertem Kontext, nie Self-PASS. Neue Provider, Server, Secrets,
Datenoffenlegung, privilegierte Rechte oder materielle Kosten bleiben Nutzer-/Foundation-Sache.
Weitere Router: [Architektur](foundation/architecture.md), [Reviews](reviews/README.md),
[Epic Preparation](epics/README.md). Historische Annahmen gelten nur für ihre Subjects.
