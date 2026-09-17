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
Vor dem allerersten Write zusätzlich Repository-ID 1374094477, public und
EMPTY_REPOSITORY_NO_BRANCH_OR_COMMIT; siehe `foundation/evidence/preflight.json`.
Bei Konflikten mit fremder Arbeit stoppen statt löschen/stashen/resetten.
Nur geprüfte benannte Pfade stagen; tatsächlichen staged Diff vor Commit prüfen.
Keine Force-Pushes, History-Rewrites, Repo-/Sichtbarkeits-/Admin-/Secretänderungen.
Vor Push Remote erneut prüfen; danach SHA-Gleichheit lokal/tracking/remote belegen.
Eigener Push ist keine unabhängige Acceptance.

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
