# WindowSafe: Agenteneinstieg

Lade zuerst [foundation/context.md](foundation/context.md), dann die für den
Auftrag relevanten Originalinputs und [Engineeringregeln](foundation/engineering.md).
Die exakte Foundation 2 liegt in `foundation/sources/foundation-2.md`.
Foundation 1 grenzt die unabhängige LLM-/Reviewrolle ab.

Aktuelle Autorisierung: **REVIEW_TRANSFER_HARNESS_FOLLOWUP_AND_REVIEWER_ENVIRONMENT_PREPARATION_ONLY**
nach WS-EA-20260918-01, Originalbytes in `foundation/evidence/followup-authorization.json`.
WS-HC-20260918-01 arbeitet ausschließlich auf `fix/ws-hc-20260917-01` ab
`9b6dd621deec1193bfdfbdfa730e8f9349c73fd6`; kumulative Review-/Historybasis bleibt
`4ba2c473fe4d90c85d94ee2b2f5cc5777d115109`. Keine direkten main-Writes,
kein Merge/Auto-Merge; STOP am geprüften ungemergten Korrekturhead. Mindestens
ELEVATED; unabhängiger Delta-Review und spätere Integrationsfreigabe sind getrennt.
Keine normalen Produktfeatures, kein erster Epic, keine Browser-/Profiltests,
keine Signierung, Veröffentlichung oder Production. Bei materiellem Konflikt
stoppen. Kein Selbst-PASS für externe Reviews; keine Gate-Abschwächung.

- Architektur und vorgelagerte Plattform-/Performance-Gates: `foundation/architecture.md`.
- Reviewkanal V3, V1-/V2-Kompatibilität und Evidence: `reviews/README.md` und
  `foundation/evidence/followup-correction.md`. Historisches PASS/Finding nicht ändern.
- Reviewer-Umgebung: `foundation/reviewer-environment.md`; F02 bleibt bis zum
  eigenen unabhängigen Preflight und abschließenden Resultatkonsum offen.
- Epic-Preparation/Binding: `epics/README.md`; kein Epic ist READY_FOR_AGENT.
- Prüfungen und Git-/Risikoregeln: `foundation/engineering.md`.

Repository ist System of Record. Fremde/untracked Änderungen schützen; vor
Mutation Root, Remote, Ref, HEAD, Worktree und Index prüfen. Named paths stagen.
Die verifizierten Eingaben und historische Reviewresultate nicht überschreiben.
Künftige autorisierte Phasen ändern den Lifecycle durch eigene gebundene Records.
