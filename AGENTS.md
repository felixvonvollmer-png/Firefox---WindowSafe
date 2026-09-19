# WindowSafe: Agenteneinstieg

Lade zuerst [foundation/context.md](foundation/context.md), dann die für den
Auftrag relevanten Originalinputs und [Engineeringregeln](foundation/engineering.md).
Die exakte Foundation 2 liegt in `foundation/sources/foundation-2.md`.
Foundation 1 grenzt die unabhängige LLM-/Reviewrolle ab.

Aktuelle Autorisierung: **WS-EA-20260919-05** für **WS-E01-INT-20260919-02**;
Original: `epics/WS-E01/evidence/integration-authorization.json`.
Der exakte unabhängige WS-E01-EPR-20260919-02 PASS liegt unter
`reviews/results/WS-E01-EPR-20260919-02.json`. Das Accepted-Binding
`epics/WS-E01/binding.json` ist READY_FOR_AGENT und verweist weiterhin auf den
reviewed Subject `644b81f63dcc1990bc894a9c2c9bd8dc24a98c04` sowie die unveränderte
Foundationbasis `dc9c1c37a264cc80f79ec08bf166ec42cdd73b95`.
Nur exakter Originaltransfer, Accepted-Binding, minimaler generischer Lifecycle-
Support und nichtblockierender Routing-Follow-up, lokale Gates, Push/Exact-Head-CI
und normaler Mergecommit von PR #2 sind autorisiert. STOP nach Post-Merge-Prüfung.
Kein Auto-Merge, Squash, Rebase oder direkter Remote-main-Write.
READY_FOR_AGENT akzeptiert die Preparation; es autorisiert hier keinen WS-E01-F01-
Start. Keine Produkt-/Browser-/Profilarbeit, Signierung, Veröffentlichung oder
Production. Eine spätere Featureausführung benötigt eigene ausdrückliche
Autorisierung und die vorgelagerten Test-Envelopes. Bei materiellem Konflikt stoppen.
Mindestens ELEVATED; unabhängiger Preparation-PASS und Integrationsautorisierung
bleiben getrennte Gates. Spätere Inkremente brauchen ihre eigene Risikoprüfung.
Kein Selbst-PASS für externe Reviews; keine Gate-Abschwächung.

- Architektur und vorgelagerte Plattform-/Performance-Gates: `foundation/architecture.md`.
- Reviewkanal V3, V1-/V2-Kompatibilität und Evidence: `reviews/README.md` und
  `foundation/evidence/followup-correction.md`. Historisches PASS/Finding nicht ändern.
- Historische Reviewer-Umgebung: `foundation/reviewer-environment.md`;
  der integrierte Rücklauf WS-PFR-20260918-02 bindet die damalige F02-Auflösung.
- Epic-Preparation/Accepted-Binding: `epics/README.md`; WS-E01-F01 bleibt ungestartet.
- Prüfungen und Git-/Risikoregeln: `foundation/engineering.md`.

Repository ist System of Record. Fremde/untracked Änderungen schützen; vor
Mutation Root, Remote, Ref, HEAD, Worktree und Index prüfen. Named paths stagen.
Die verifizierten Eingaben und historische Reviewresultate nicht überschreiben.
Künftige autorisierte Phasen ändern den Lifecycle durch eigene gebundene Records.
