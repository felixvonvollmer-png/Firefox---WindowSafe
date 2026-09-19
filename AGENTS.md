# WindowSafe: Agenteneinstieg

Lade zuerst [foundation/context.md](foundation/context.md), dann die für den
Auftrag relevanten Originalinputs und [Engineeringregeln](foundation/engineering.md).
Die exakte Foundation 2 liegt in `foundation/sources/foundation-2.md`.
Foundation 1 grenzt die unabhängige LLM-/Reviewrolle ab.

Aktuelle Autorisierung: **WS-E01-MAT-20260919-01** nach **WS-EA-20260919-04**,
Originalbytes in `epics/WS-E01/evidence/preparation-authorization.json`.
Nur Materialisierung der sechs gelieferten WS-E01-Artefakte und minimaler
generischer Preparation-Harness-/Living-Context-Übergang auf
`prep/ws-e01-20260919-01` ab `dc9c1c37a264cc80f79ec08bf166ec42cdd73b95`.
Project Foundation ist mit WS-PFR-20260918-02 PASS integriert;
External Context Sync NOT_APPLICABLE. WS-E01: EPIC_PREPARATION_READY_FOR_REVIEW,
unabhängiger Review PENDING, kein Epic READY_FOR_AGENT. Keine direkten main-Writes,
kein Merge/Auto-Merge; STOP am geprüften ungemergten Draft-PR. Mindestens
ELEVATED; unabhängiger Preparation-Review und spätere Autorisierung sind getrennt.
Keine normalen Produktfeatures, keine Epic-Ausführung, keine Browser-/Profiltests,
keine Signierung, Veröffentlichung oder Production. Bei materiellem Konflikt
stoppen. Kein Selbst-PASS für externe Reviews; keine Gate-Abschwächung.

- Architektur und vorgelagerte Plattform-/Performance-Gates: `foundation/architecture.md`.
- Reviewkanal V3, V1-/V2-Kompatibilität und Evidence: `reviews/README.md` und
  `foundation/evidence/followup-correction.md`. Historisches PASS/Finding nicht ändern.
- Historische Reviewer-Umgebung: `foundation/reviewer-environment.md`;
  der integrierte Rücklauf WS-PFR-20260918-02 bindet die damalige F02-Auflösung.
- Epic-Preparation/Binding: `epics/README.md`; kein Epic ist READY_FOR_AGENT.
- Prüfungen und Git-/Risikoregeln: `foundation/engineering.md`.

Repository ist System of Record. Fremde/untracked Änderungen schützen; vor
Mutation Root, Remote, Ref, HEAD, Worktree und Index prüfen. Named paths stagen.
Die verifizierten Eingaben und historische Reviewresultate nicht überschreiben.
Künftige autorisierte Phasen ändern den Lifecycle durch eigene gebundene Records.
