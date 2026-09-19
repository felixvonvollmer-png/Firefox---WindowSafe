# Engineering, Git, Risiko und Evidence

## Umgebung und Befehle

Bootstrap lokal: Python 3.14.4, Git 2.53.0, gh 2.98.0. Python-Standardbibliothek
genügt; keine Installation im Nutzerprofil. Git ist für immutable Reviewbindungen
erforderlich. CI pinnt Python 3.14.4 auf ubuntu-24.04; Runnerimage/OS bleibt ein
verwalteter beweglicher Unterbau und wird im jeweiligen CI-Log sichtbar.

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build
git diff --check
```

`check`: Paket-/Blobintegrität, JSON-Duplikate/Format, Syntax, lokale Dokumentlinks,
Scope-Allowlist, Lifecycle-/CI-Grenzen und sämtliche Repository-Reviewresultate.
`build`: validiertes deterministisches SHA-256-Dateiinventar (Foundation-Artefakt)
nach `build/foundation-inventory.json`. Zwei unveränderte Builds müssen identisch
sein. Add-on-Build/Typecheck/web-ext-Lint sind mangels Produktcode NOT_APPLICABLE.
`tests`: positive/negative/fail-closed Harness-Regressionen; keine Firefox-Tests.

CI wiederholt dieselben Prüfungen und vergleicht bei PR/Push vorhandene Inputs,
Foundationquellen und Reviewresultate gegen den vorherigen Git-Stand (append-only).
Die erste Root-Integration hat keinen Vorgänger; dies ist ausdrücklich zulässig.
Späterer Reviewkonsum prüft Resultate erneut gegen die exakten Subject- und
Evidencebytes. Beliebig viele unterschiedliche Review-IDs sind zulässig.

Actions sind auf volle Commit-SHAs gepinnt, nur `contents: read`, keine Secrets,
kein `pull_request_target`, keine Deployments/Uploads/Signierung. Herkunft und
Nutzung: [actions/checkout](https://github.com/actions/checkout),
[actions/setup-python](https://github.com/actions/setup-python),
[GitHub Workflow-Dokumentation](https://docs.github.com/en/actions/get-started/quickstart).
Beide Actions stehen unter MIT; keine Quellenkopie ins Produkt. Sie laden allein
den öffentlichen Repositorykontext und die gepinnte Entwicklungsruntime.
Keine Produktdependencies, keine neuen Provider oder bezahlten Dienste.

## Git und Integration

Vor jedem Write Root/Remote/Zielref/HEAD/Worktree/untracked/Index prüfen.
Historisch vor dem allerersten Bootstrap-Write zusätzlich Repository-ID 1374094477, public und
EMPTY_REPOSITORY_NO_BRANCH_OR_COMMIT; siehe `foundation/evidence/preflight.json`.
Bei Konflikten mit fremder Arbeit stoppen statt löschen/stashen/resetten.
Nur geprüfte benannte Pfade stagen; tatsächlichen staged Diff vor Commit prüfen.
Keine Force-Pushes, History-Rewrites, Repo-/Sichtbarkeits-/Admin-/Secretänderungen.
Vor Push Remote erneut prüfen; danach SHA-Gleichheit lokal/tracking/remote belegen.
Eigener Push ist keine unabhängige Acceptance.

Historisch galt für **WS-HC-20260918-01** WS-EA-20260918-01: Fortsetzung ab
`9b6dd621deec1193bfdfbdfa730e8f9349c73fd6`, kumulative Review-/Historybasis
`4ba2c473fe4d90c85d94ee2b2f5cc5777d115109`, nur `fix/ws-hc-20260917-01`.
Kein main-Write, Merge/Auto-Merge oder unabhängiges Selbst-PASS. Mindestens ELEVATED;
Delta-Review und spätere Integrationsfreigabe bleiben getrennt. Evidence unter
`foundation/evidence/followup-*`; Vorbereitung: [Reviewer-Umgebung](reviewer-environment.md).

CI checkt den PR-Head aus. `history --event-base` liest den echten vorherigen
Push-SHA beziehungsweise PR-Base-SHA. Bei 40 Nullzeichen stammt der Fallback aus
dem separat SHA-256-gepinnten Original `followup-authorization.json`, nicht aus
dem aktuellen Subject. Commit-/Tree-Bindungen und strikte Ancestors werden geprüft.
Subject und Worktree müssen die gleiche Autorisierung, kumulative und Laufbasis
nennen. HEAD, fremde oder nicht autorisierte Zwischen-Ancestors sind keine Basis.
Auch bei legitimen späteren Pushbasen bleiben kumulative Basis und Laufstart im
Abgleich. Alle Commits der unakzeptierten linearen Strecke werden auf Append-only
geprüft; auch spätere Reverts verstecken keine frühere Historyänderung.
Root-Bootstrap ohne Eltern bleibt strukturell zulässig, ohne festen Historycount.
Neue Phasen brauchen eigene explizite Bindung; diese enge Fortsetzung ist kein
allgemeiner automatisch erweiterter Lifecycle. Evidenceoriginale und separate
semantische Dispositionen sind ebenfalls append-only.

Für die historische Materialisierung gilt WS-EA-20260919-04 für WS-E01-MAT-20260919-01 auf
`prep/ws-e01-20260919-01` ab main `dc9c1c37a264cc80f79ec08bf166ec42cdd73b95`.
Der Preparation-Validator prüft generische Epic-IDs, Subject/Binding, sichere
Evidence, kritische Eigenprüfung, fehlende Ausführungsfreigabe und den bereits
in der gebundenen main-Basis enthaltenen validen Foundation-PASS samt Ancestry.
Die neue Originalautorisierung ist unabhängig vom Subject SHA-256-gepinnt;
eine weitere Preparation braucht eine eigene ausdrücklich gebundene Autorisierung.

Der History-Guard behält kumulative Altbasis, Laufstart und sämtliche
Append-only-Vergleiche bei. Ausschließlich der durch die neue Autorisierung
gebundene integrierte Foundation-Merge wird zusätzlich erkannt: zwei Eltern,
erster Elterncommit gleich kumulativer Altbasis, zweiter enthält den reviewed
Subject und ausschließlich dessen additive PASS-Resultatübertragung; Mergebaum
gleich zweitem Elternbaum. Jede andere Merge-Stelle bleibt gesperrt. Auch
Preparationoriginale sind append-only; Reverts verstecken keine Zwischenänderung.
Der autorisierte Folgeübergang WS-EA-20260919-05 ergänzt ausschließlich das
Accepted-Epic-Binding und den normalen PR-#2-Merge. Das separat SHA-256-gepinnte
Original `epics/WS-E01/evidence/integration-authorization.json` bindet den reviewed
Subject, unveränderte main-Basis, Review-ID, exakte Resultatbytes und den engen Scope.
Der kanonische V3-Verbraucher prüft den PASS erneut. Das aktuelle Binding darf nur
die definierten Acceptance-/Autorisierungs-/Follow-up-Felder ergänzen oder umstellen;
Originalsubject und Preparationevidence bleiben unverändert.

History erlaubt diese eine gerichtete Bindingänderung nur mit gleichzeitig
vorhandenem Originalsubject, exakter Autorisierung und exaktem Resultat. Andere
Änderungen, Löschungen und zwischenzeitliche Rewrites mit späterem Revert bleiben
gesperrt. Der Epic-Merge muss zwei Eltern haben: gebundene bisherige main-Basis
und Integrationshead mit akzeptiertem Binding, bei identischem Merge-/Head-Baum.
Kumulative Altbasis, Laufstart und jeder Zwischencommit werden weiter geprüft.
Kein allgemeiner Merge-/History-Bypass; keine Featureausführung.

Zusätzliche Pflichtbefehle am exakten committed Preparation-Head:

```sh
python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json
python3 tools/foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json
python3 tools/foundation.py build --verify-repeat
python3 tools/foundation.py history --base dc9c1c37a264cc80f79ec08bf166ec42cdd73b95
```

CI prüft den echten PR-/Push-Head. Bei Accepted-Binding führt der Request nach
Validierung des Übergangs zum ursprünglichen reviewed Subject
`644b81f63dcc1990bc894a9c2c9bd8dc24a98c04` mit unveränderten 23 Evidence-Bindungen.
Alle vorhandenen Reviewresultate werden weiter kanonisch konsumiert. WS-E01
Preparation ist mit WS-E01-EPR-20260919-02 PASS angenommen; External Context Sync
NOT_APPLICABLE. Unter WS-EA-20260919-05 sind Push, beide erfolgreichen Exact-Head-
CI-Jobs und normaler PR-#2-Merge mit unveränderter bisheriger main-Basis erforderlich.
Danach Post-Merge-Prüfung und STOP. Keine Dependencyinstallation, Produkt-/Browser-
arbeit, kein eigener unabhängiger Verdict, kein Auto-Merge und kein WS-E01-F01.

Der Inventar-Writer öffnet Root/Ausgabeordner/Blatt mit No-follow und relativen
Directory-FDs, prüft den geöffneten Dateityp/Linkcount vor dem Trunkieren und
folgt nach Öffnung keinem Pfad mehr. Es gibt keine automatische Linklöschung.
Qualifiziert sind die lokale Linux-Umgebung und Ubuntu-CI mit Python 3.14.4;
fehlende POSIX/dir_fd/No-follow-Fähigkeiten blockieren vor Ausgabe-Mutation.
Kein Windows-/Reparse-Point-Nachweis oder Schutz gegen feindliche Umbenennung
bereits geöffneter Verzeichnis-Inodes behauptet. Buildausgabe ist regenerierbar,
nicht atomar/crash-durable; Schreibfehler sind kein Erfolg.

`main` ist Development, ohne Deployment. Initialer Root-Commit darf direkt nach
lokalen Gates und internem Review integriert werden; CI-Verifikation folgt am
SHA. Spätere Inkremente: kurze Branches, kleine PRs, aktuelle Risikoprüfung und
erforderliche Reviewer **vor** Integration; kumulative Featureprüfung zusätzlich.
Unakzeptiertes Verhalten muss inert/isoliert bleiben; bei Productionwirkung
Release-/Containment-/Rollbackgate zuerst erfüllen. Operations sind nicht aktiviert.

## Risiko und Findings

LOW_RISK: Self-Review plus CI kann genügen. ELEVATED_RISK: unabhängiger technischer
Review erforderlich. HIGH_RISK: geeignete spezialisierte Reviewer und Rereview
nach Korrekturen. Sensitive Side Effects (Concurrency, destruktive Veröffentlichung,
schwer rückgängig zu machende Wirkung, Trust-/Securitygrenze) benötigen mindestens
Elevated Risk, sofern keine explizite evidenzbasierte LOW-Begründung vorliegt.

Severities: CRITICAL, BLOCKING, MAJOR, MINOR, NIT_OR_SUGGESTION.
Dispositionen: FIXED, FALSE_POSITIVE_OR_NOT_APPLICABLE, DUPLICATE,
FOLLOW_UP_TRACKED, EXPLICITLY_AUTHORIZED_NONCRITICAL_RISK_ACCEPTANCE.
Kein offener Critical/Blocking/Major darf als Follow-up versteckt oder allein vom
Implementierer heruntergestuft werden. Findingsfreiheit ist Ergebnis, kein Zielwert.
Nicht ausführbare Pflichtchecks halten das Gate offen. Policy wird nicht zur
Behebung eines aktiven Blockers abgeschwächt.

## Evidencevertrag

Jeder Nachweis nennt Klasse, Befehl/Methode, Subject-/Artefaktbindung, Ergebnis
und Reichweitenbegrenzung. Klassen strikt getrennt:

- LOCAL_AGENT_REPORTED: lokale Ausführung/Self-Review, nicht unabhängig.
- REPOSITORY_OR_REMOTE_VERIFIED: tatsächlich gelesene Git-/GitHub-Objekte.
- CI_VERIFIED: abgeschlossener CI-Run mit exaktem head_sha, URL und Ergebnis.
- RUNTIME_OR_OPERATION_VERIFIED: tatsächlicher autorisierter Lauf; hier keiner.

Die Reviewevidence liegt am Subject-SHA. Ein Reviewer bindet tatsächlich gelesene
Evidencebytes per SHA-256, verifiziert CI zusätzlich am selben head_sha und nennt
Grenzen. Dokumente beweisen keine Produktimplementation, CI keinen Browserbetrieb.
Ein dynamischer Branch-Link allein ist kein immutable Subject.

Spätere Featureevidence enthält F2 §31 vollständig: Product-/Workflow-/Foundation-
und Epicreferenzen, Start-/End-SHA, Changesets, intervenierende Änderungen,
integrierte Interaktionsprüfung, Acceptance Criteria, Tasks/Bugs/PRs, lokale/CI-
und kumulative Runtime-/E2E-Evidence, kumulatives Risiko mit Begründung,
Reviewabdeckung, spezialisierte Reviewer, Findings/Entscheidungen/Living-Docs/Follow-ups.

## Agenten- und Modellgrenzen

Dieser Lauf nutzt einen Coding-Agent und deterministische Tools; keine Delegation.
Shell, Git, gh und lokale Tests sind tatsächlich verfügbar; GitHub meldet push-
Berechtigung. Technische Capability autorisiert keine Adminaktionen.
Sessiontools bieten Subagenten-/Modellauswahl, aber es wurde kein Override benutzt
und kein Kostenvorteil behauptet. Kosten/Quota sind nicht gemessen.

Künftige Rollen/Modelle/Reasoningstufen nur JIT nach Risiko, Unsicherheit, Kontext,
Qualität und beobachtbaren Gesamtkosten innerhalb des aktuellen Execution Envelopes.
Keine eigenständigen Providerrouter oder Cross-Provider-Wechsel. Bei unbekannten
wiederkehrenden Klassen zuerst ausreichende Qualitätsbaseline; günstige Auswahl
erst mit Verifikation. Eine stärkere Modellstufe ersetzt keine Unabhängigkeit.
Fehlende Override-/Hook-/Branchschutzfähigkeiten offen benennen und durch die
in Foundation 2 beschriebenen funktionalen Workflows ersetzen.

## F01-Qualifikation unter WS-EA-20260919-06

Die oben als historisch beschriebenen Preparation-/Integrationsläufe bleiben an ihre Subjects
gebunden. Der neue Startrecord und das separate Original autorisieren ausschließlich F01.
Featureoriginale und Evidence sind append-only; state.json ist ein abgeleiteter Lifecyclezustand.
Feature-Subjects sind erst bei READY_FOR_ACCEPTANCE_REVIEW zulässig und bleiben unter dieser
Ausführungsautorisierung vollständig gesperrt. Das Harness konsumiert die akzeptierte
Epic Preparation an der exakten F01-Startbasis und prüft ihre fortgesetzte Unveränderlichkeit.
Alle alten kumulativen Historybasen, Zwischencommits und kanonischen Resultate bleiben geprüft.

Zusätzliche Befehle: `python3 qualification/ws-e01-f01/toolchain.py --setup` für statische
Toolchain-/Lint-/Auditprüfungen; synthetische Browserläufe ausschließlich nach dem
[Fortsetzungsprotokoll](../qualification/ws-e01-f01/README.md). CI führt statische Ubuntu-/Windows-
Toolchainprüfungen aus. Windows Server CI ist kein Windows-Desktop-/GUI-/Restartnachweis.
Unabhängiger allgemeiner technischer Review ist nach F01-Konvergenz erforderlich;
Feature Acceptance wird nicht durch diesen Coding-Agenten vorbereitet oder ausgestellt.
