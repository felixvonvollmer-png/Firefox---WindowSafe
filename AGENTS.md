# WindowSafe: Agenteneinstieg

Lade zuerst [foundation/context.md](foundation/context.md), dann die für den
Auftrag relevanten Originalinputs und [Engineeringregeln](foundation/engineering.md).
Die exakte Foundation 2 liegt in `foundation/sources/foundation-2.md`.
Foundation 1 grenzt die unabhängige LLM-/Reviewrolle ab.

Aktuelle Autorisierung: **PROJECT_FOUNDATION_ONLY** nach WS-EA-20260917-01.
Keine normalen Produktfeatures, kein erster Epic, keine Browser-/Profiltests,
keine Signierung, Veröffentlichung oder Production. Bei materiellem Konflikt
stoppen. Kein Selbst-PASS für externe Reviews; keine Gate-Abschwächung.

- Architektur und vorgelagerte Plattform-/Performance-Gates: `foundation/architecture.md`.
- Reviewkanal, Schema-Preflight und Evidence: `reviews/README.md`.
- Epic-Preparation/Binding: `epics/README.md`; kein Epic ist READY_FOR_AGENT.
- Prüfungen und Git-/Risikoregeln: `foundation/engineering.md`.

Repository ist System of Record. Fremde/untracked Änderungen schützen; vor
Mutation Root, Remote, Ref, HEAD, Worktree und Index prüfen. Named paths stagen.
Die verifizierten Eingaben und historische Reviewresultate nicht überschreiben.
Künftige autorisierte Phasen ändern den Lifecycle durch eigene gebundene Records.
