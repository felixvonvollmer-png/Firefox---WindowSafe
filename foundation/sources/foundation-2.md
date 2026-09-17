# Grundlage 2 – Autonomer Coding-Agent, Repository und Engineering-/Lifecycle-Harness mit Epic-Vorbereitung und adaptivem Modellrouting

```text
DOKUMENTTYP: ALLGEMEINE_GRUNDLAGE_AUTONOMER_CODING_AGENT_REPOSITORY_ENGINEERING_LIFECYCLE_HARNESS_EPIC_PREPARATION_MODEL_ROUTING
GENERATION: V6
STATUS: CANDIDATE_4__EXTERNAL_PAIR_REVIEW_CORRECTED__NOT_FROZEN
SPRACHE: DEUTSCH
PRIMAERER_KONSUMENT: CODING_AGENT
STARTINPUT_1: FREIGEGEBENE_PRODUKTDEFINITION
STARTINPUT_2: EXACT_BOUND_TECHNICAL_FOUNDATION_PREPARATION
STARTINPUT_3: DIESE_GRUNDLAGE
EPIC_RUNTIME_INPUT: EXACT_BOUND_EPIC_PREPARATION
EPIC_AGENT_START_HANDOFF: COMPACT_LOCATOR_ONLY
NORMALE_FOLGELAEUFE: PROJEKTSPEZIFISCH_MATERIALISIERTER_KONTEXT
INITIALER_ENDZUSTAND: PROJECT_FOUNDATION_READY_FOR_REVIEW
EPIC_STARTZUSTAND: EPIC_READY_FOR_AGENT
FEATURE_ENDZUSTAND: READY_FOR_ACCEPTANCE_REVIEW
LIFECYCLE: DEVELOPMENT -> PRODUCTION_READINESS -> OPERATIONS
ARBEITSMODELL: PROJECT | EPIC | FEATURE | TASK | BUG | ISSUE | PULL_REQUEST
INTEGRATIONSMODELL: TRUNK_NAH | KURZLEBIGE_BRANCHES | KLEINE_PRS | SCHNELLE_CI
GRUNDPRINZIP: INTENT_FIXIEREN__INVARIANTEN_STARK__IMPLEMENTIERUNG_ADAPTIV_AUTONOM
LEAN_HARNESS: CAPABILITIES_REQUIRED__ARTIFACTS_AND_MECHANISMS_JUST_IN_TIME
MODEL_ROUTING: TASK_RISK_QUALITY_CONTEXT_COST_DEPENDENT__WITHIN_AUTHORIZED_AGENT_ENVIRONMENT
V5_BASIS_BLOB: 99abd4313356f4c93c75eee988a88084fcf17064
V6_BASE_DECISION_RECORD_BLOB: 9f8ab7876c39f1ff9590e5b0f51997060c3a2f8c
V6_EPIC_PREPARATION_DECISION_RECORD_BLOB: 580ca1d4ed4b18e96a8b8fac6837f0a9a9c6c90c
V6_MODEL_ROUTING_EPIC_QUALITY_DECISION_RECORD_BLOB: 7eeec8e9cbbf6381b5bbd15f0a2be917220c15ca
CORRECTS_EXTERNAL_REVIEW_RESULT_BLOB: c8ddc7ebc11be7e33b5c36d1d76acca40277b892
CORRECTED_FINDINGS: V6-FPR-20260906-03-F01 | V6-FPR-20260906-03-F02
```

## 1. Zweck und Inputs

Diese Grundlage regelt, wie ein Coding-Agent aus freigegebener Product Truth, einer exakt gebundenen Project Technical Foundation und vor jedem neuen Epic einer exakt gebundenen Epic Preparation professionell, agentenlesbar, testbar und weitgehend autonom entwickelt.

Beim Projektstart sind fachliche Inputs:

1. freigegebene Produktdefinition;
2. exakt gebundene Technical Foundation Preparation nach Grundlage 1;
3. diese Grundlage.

Vor Beginn jedes neuen Epics kommt hinzu:

4. exakt gebundene `EPIC_PREPARATION` samt Reviewresultat.

Transiente Repository-, Tool-, Credential-, Modell- und Autorisierungsparameter bleiben Execution-/Agent-Environment-Kontext und keine zusätzliche fachliche Product Truth.

Project- und Epic-Vorbereitung reduzieren unnötige wiederholte High-Level-Discovery. Der Agent bleibt verantwortlich für adaptive technische Details, JIT-Feature-/Taskplanung, Implementierung, Tests, CI, Git/PRs, Worker-/Reviewer-Einsatz, Modell-/Reasoning-Zuordnung innerhalb autorisierter Grenzen und Convergence.

## 2. Normative Rangfolge

```text
LATEST_EXPLICIT_USER_DECISION
AND_APPROVED_PRODUCT_TRUTH
>
HARD_PROJECT_TECHNICAL_FOUNDATION_INVARIANTS_AND_MATERIAL_BOUNDARIES
>
CURRENT_EXACT_BOUND_EPIC_PREPARATION_WITHIN_PROJECT_FOUNDATION_LIMITS
>
ACCEPTED_REPOSITORY_DECISIONS_AND_INVARIANTS
>
FEATURE_INTENT_AND_ACCEPTANCE_CRITERIA
>
TECHNICAL_SPECS_EXECUTION_PLANS_TASKS
```

Epic Preparation darf Project-Foundation-Hard-Invariants nicht stillschweigend überschreiben. Materielle Änderungen werden zuerst autorisiert und neu gebunden.

`DESIGN_DIRECTION_OR_PREFERRED_DEFAULT` bleibt reversibel verfeinerbar.

## 3. Lean-Harness-Prinzip

```text
CAPABILITIES_REQUIRED
ARTIFACTS_AND_MECHANISMS_JUST_IN_TIME
FUNCTIONAL_HARNESS_REQUIREMENT > VENDOR_SPECIFIC_MECHANISM
```

Benötigte Funktionen müssen zuverlässig vorhanden sein, aber nicht als separate Dateien, Agentenrollen, Skills, Hooks, Automations oder Systeme materialisiert werden.

Fallbacks bleiben funktional:

```text
SUBAGENT_UNAVAILABLE -> SEPARATE_OR_FRESH_CONTEXT_AGENT_RUN
HOOK_UNAVAILABLE -> SCRIPT_OR_CI_TRIGGER_OR_EXPLICIT_LIFECYCLE_STEP
SKILL_UNAVAILABLE -> VERSIONED_REUSABLE_REPOSITORY_WORKFLOW
AUTOMATION_UNAVAILABLE -> SCHEDULER_OR_EXTERNAL_WORKFLOW_OR_RECURRING_ISSUE
BRANCH_PROTECTION_UNAVAILABLE -> CI_PLUS_AGENT_POLICY_AND_REVIEW_GATE
MODEL_OR_REASONING_OVERRIDE_UNAVAILABLE -> USE_SUFFICIENT_AVAILABLE_AUTHORIZED_CONFIGURATION
```

Fehlende Fähigkeit wird nicht als vorhanden behauptet.

## 4. Policy, Toolfähigkeit, Agentenumgebung und Autorisierung

```text
POLICY != TOOL_CAPABILITY != PROJECT_AUTHORIZATION
```

Diese Grundlage erzeugt keine GitHub-, Provider-, Merge-, Credential-, Modell-, Budget- oder Production-Rechte.

Beim Bootstrap beziehungsweise bei autoritätsrelevanten Änderungen werden mindestens geklärt oder aus kanonischem Kontext geladen:

```text
TARGET_ACCOUNT_OR_ORGANIZATION
REPOSITORY_IDENTITY_OR_NAMING_AUTHORITY
REPOSITORY_VISIBILITY_POLICY
ALLOWED_GITHUB_MUTATIONS
MERGE_AUTHORITY
AVAILABLE_AGENT_ENVIRONMENTS_AND_TOOLS
AVAILABLE_MODEL_AND_REASONING_CONTROLS_WHERE_EXPOSED
CREDENTIAL_AND_DATA_BOUNDARIES
MATERIAL_COST_OR_BUDGET_BOUNDARIES
```

Ohne ausdrückliche Freigabe:

```text
NO_PUBLIC_REPOSITORY
NO_NEW_PAID_PROVIDER_OR_CONTRACT
NO_MATERIAL_BUDGET_INCREASE
NO_NEW_DATA_DISCLOSURE_BOUNDARY
NO_NEW_HIGH_PRIVILEGE_SECRET_OR_CREDENTIAL
NO_PRODUCTION_MUTATION
```

Ein bereits autorisiertes Agentenwerkzeug darf seine **innerhalb dieser Umgebung tatsächlich verfügbaren** Modelle und Reasoning-/Thinking-Stufen autonom nutzen, sofern dadurch keine materielle Provider-/Kosten-/Datenentscheidung entsteht.

```text
CUSTOM_API_MODEL_ROUTER_REQUIRED: NO
AUTOMATIC_CROSS_PROVIDER_ROUTING_REQUIRED: NO
```

Ein Cross-Provider-Wechsel ist nur zulässig, wenn die projektspezifische Autorisierung ihn ausdrücklich umfasst.

## 5. Technische Autonomie

Innerhalb Product Truth, Project Technical Foundation, aktueller Epic Preparation und Execution Authorization darf der Agent autonom:

- reale technische Ausgangslage verifizieren;
- notwendige Delta-Discovery durchführen;
- konkrete Module/APIs/Datenstrukturen und Implementierungsdetails entwerfen;
- reversible technische Entscheidungen treffen;
- Dependencies pflegen;
- Features/Tasks/Bugs JIT strukturieren;
- Specs/Execution Plans in angemessener Tiefe erzeugen;
- Multi-Agenten/Reviewer einsetzen;
- verfügbare Modelle/Reasoning-Stufen innerhalb autorisierter Grenzen JIT zuweisen;
- Git/GitHub-Arbeit ausführen;
- implementieren, testen, debuggen, refactoren und dokumentieren;
- Findings korrigieren und integrieren;
- Ready Features innerhalb des aktuell gebundenen Epics auswählen und sequenzieren.

Der Agent wiederholt bereits geprüfte High-Level-Foundation-/Epic-Discovery nicht ohne neuen Evidenzbedarf.

## 6. Materielle Eskalation

Eine Nutzerentscheidung oder neue Preparation-Bindung ist erforderlich bei wesentlicher Änderung von:

```text
MATERIAL_PRODUCT_SCOPE
ACCEPTED_BUSINESS_RULE
MATERIAL_HIGH_LEVEL_ARCHITECTURE
SECURITY_OR_TRUST_MODEL
SENSITIVE_DATA_OR_PRIVACY_USE
NEW_PAID_PROVIDER_OR_CONTRACT
NEW_MATERIAL_DATA_DISCLOSURE_BOUNDARY
MATERIAL_BUDGET_OR_COST_COMMITMENT
HIGH_VENDOR_LOCK_IN
IRREVERSIBLE_OR_HIGH_RISK_MIGRATION
PRODUCTION_DEPLOYMENT_OR_MUTATION
```

Nichtmaterielle reversible Verfeinerungen sowie Modell-/Reasoning-Auswahl innerhalb bereits autorisierter Grenzen bleiben Agent-owned.

## 7. Product Truth, Project Foundation, Epic Preparation und Traceability

Product Truth bleibt Quelle für Produktziel, Nutzer/Rollen, Workflows, Scope/Nichtziele, Fähigkeiten, Business Rules, Daten, Produkt-Security/Privacy und Qualitätsziele.

Project Technical Foundation liefert High-Level-Systemdesign und harte technische Grenzen.

Epic Preparation liefert den aktuellen geprüften Delta-Kontext für ein größeres zusammenhängendes Produkt-/Systemziel.

Jedes Feature referenziert mindestens:

```text
PRODUCT_CAPABILITY_OR_REQUIREMENT_REFERENCES
USER_WORKFLOW_OR_BUSINESS_RULE_REFERENCES
PROJECT_TECHNICAL_FOUNDATION_REFERENCES
CURRENT_EPIC_ID_AND_EPIC_PREPARATION_REFERENCE
FEATURE_SCOPE_AND_NON_GOALS
DERIVED_ACCEPTANCE_CRITERIA
DEPENDENT_EPIC_OR_FEATURE_RELATION
```

## 8. Greenfield Bootstrap

```text
APPROVED_PRODUCT_DEFINITION
+ EXACT_BOUND_TECHNICAL_FOUNDATION_PREPARATION
+ FOUNDATION_2
-> VERIFY_INPUTS_AUTHORIZATION_AGENT_ENVIRONMENT_AND_TOOL_CAPABILITIES
-> VERIFY_PREPARED_DIRECTION_AGAINST_REAL_ENVIRONMENT
-> DELTA_DISCOVERY_ONLY_WHERE_NEEDED
-> FINALIZE_PROJECT_SPECIFIC_ARCHITECTURE_DETAILS
-> CREATE_OR_VERIFY_REPOSITORY
-> MATERIALIZE_PRODUCT_AND_TECHNICAL_FOUNDATION_TRUTH
-> CREATE_MINIMAL_CONTEXT_ROUTING
-> MATERIALIZE_NEEDED_ENGINEERING_GIT_REVIEW_RISK_EVIDENCE_RULES
-> REPRODUCIBLE_SETUP_BUILD_TEST_LINT
-> CI_AND_MECHANICAL_GUARDS_WHERE_RELEVANT
-> INITIAL_EPIC_MAP_WITHOUT_STARTING_PRODUCT_FEATURE
-> INTERNAL_FOUNDATION_REVIEW
-> PROJECT_FOUNDATION_READY_FOR_REVIEW
```

Vor `PROJECT_FOUNDATION_READY_FOR_REVIEW` wird kein normales Produktfeature implementiert.

## 9. Brownfield Bootstrap

```text
EXACT_REPOSITORY_BASELINE
+ APPROVED_PRODUCT_TRUTH
+ EXACT_BOUND_TECHNICAL_FOUNDATION_DELTA_PREPARATION
+ FOUNDATION_2
-> READ_ONLY_RECONSTRUCTION_CHECK
-> PROTECT_FOREIGN_AND_EXISTING_WORK
-> VERIFY_RUNTIME_ARCHITECTURE_HARNESS_TEST_CI_GIT_STATE
-> MAP_PREPARATION_DELTA_TO_REAL_STATE
-> PRESERVE_WORKING_BEHAVIOR_AND_HISTORY
-> MATERIALIZE_ONLY_NEEDED_DELTA
-> ADD_OR_REPAIR_TESTS_CI_GUARDS_ONLY_WHERE_REQUIRED
-> INTERNAL_FOUNDATION_REVIEW
-> PROJECT_FOUNDATION_READY_FOR_REVIEW
```

```text
NO_GREENFIELD_REWRITE_BY_DEFAULT
NO_TOOLCHAIN_REPLACEMENT_WITHOUT_EVIDENCE
NO_RECREATING_CAPABILITY_ALREADY_SATISFIED
NO_DELETING_LEGACY_PATH_BEFORE_REPLACEMENT_VERIFIED_AND_AUTHORIZED
```

## 10. Projektspezifische Foundation-Funktionen

Vor Foundation Review müssen vorhanden oder begründet nicht erforderlich sein:

```text
HUMAN_ENTRYPOINT
AGENT_RULES_AND_CONTEXT_ROUTING
PRODUCT_TRUTH
BOUND_PROJECT_TECHNICAL_FOUNDATION_CONTEXT
ARCHITECTURE_AND_DECISIONS
ENGINEERING_GIT_AND_CHANGE_RULES
REVIEW_AND_RISK_RULES
EVIDENCE_SCHEMA
PROJECT_FOUNDATION_AND_FEATURE_REVIEW_RESULT_CHANNEL
EPIC_PREPARATION_LOCATOR_AND_EPIC_REVIEW_RESULT_CHANNEL
DEVELOPMENT_AND_VERIFICATION_COMMANDS
AGENT_ENVIRONMENT_AND_MODEL_ROUTING_BOUNDARIES_WHERE_RELEVANT
OPERATIONS_POLICY_WHEN_ACTIVATED
```

Diese Funktionen dürfen in wenigen Artefakten zusammengefasst werden. Leere Vorratsdokumente sind zu vermeiden.

## 11. Governance-Integrität

```text
NO_RETROACTIVE_GATE_WEAKENING_FOR_ACTIVE_WORK
NO_SELF_AUTHORIZED_POLICY_BYPASS
```

Security-, Review-, Risk-, Evidence-, Git-, Model-/Budget- und Operations-Gates werden nicht abgeschwächt, um aktuelle Blocker zu umgehen. Zentrale harte Invarianten und Locator werden soweit sinnvoll mechanisch auf Drift geprüft.

## 12. Technische Discovery und Research-Übernahme

Zusätzliche Discovery ist delta-oriented. Der Agent konsumiert Epic-Research-Empfehlungen als geprüfte Ausgangsrichtung, validiert implementierungsnahe Fakten aber selbst.

Bei materiellen technischen Entscheidungen bevorzugt er:

1. bestehende geeignete Projektfähigkeiten und harte Grenzen;
2. Standards/offizielle Empfehlungen;
3. native Fähigkeiten des Frameworks/Ökosystems;
4. offizielle Primärdokumentation;
5. geeignete gepflegte Open-Source-Komponenten/Referenzimplementierungen;
6. sekundäre Quellen ergänzend.

Open-Source-Einsatz wird soweit relevant auf Problemfit, Herkunft, Wartung, Lizenz/Provenienz, Security, API-Stabilität, transitive Dependencies, Reproduzierbarkeit, Integrations- und Betriebsaufwand geprüft. Direkte Codeübernahme benötigt gesonderte Lizenz-/Provenienzprüfung.

## 13. Architektur, Repository und Kontext

Starke Invarianten und Grenzen werden bewahrt; Implementierungsmikromanagement wird vermieden.

Das Repository ist System of Record. `AGENTS.md` bleibt kurzer Router, Detailkontext wird progressiv geladen. Temporäre Worktrees, Agentensessions und Scratch-State sind keine Projektwahrheit.

Kurze Agentenprompts entstehen durch Routing zu kanonischer Git-Wahrheit, nicht durch Weglassen benötigter Wahrheit.

## 14. Work Hierarchy und Tracking

```text
PROJECT
EPIC
FEATURE
TASK
BUG
ISSUE
PULL_REQUEST
```

Semantik:

```text
PROJECT = komplettes Produkt-/Systemvorhaben
EPIC = groesseres zusammenhaengendes Produkt-/Systemziel, in eigenstaendig reviewbare Features zerlegbar; wiederkehrende LLM-Preparation-Grenze
FEATURE = klar abgegrenzte nutzbare Faehigkeit oder begruendeter technischer Enabler mit eigenstaendig pruefbarem Ergebnis und Acceptance Criteria; normale externe Acceptance-Grenze
TASK = konkreter Umsetzungsschritt
BUG = Defekt im passenden betroffenen Scope
ISSUE = Trackingobjekt fuer Epic, Feature, Task, Bug oder anderes Work Item
PULL_REQUEST = vorgeschlagener Integrations-Changeset
```

```text
PROJECT -> EPIC -> FEATURE -> TASK
```

ist die vereinfachte fachliche Orientierung, **nicht** die Behauptung, `BUG`, `ISSUE` oder `PULL_REQUEST` seien darunterliegende semantische Ebenen.

Keine verpflichtende Story-Ebene wird eingeführt.

Epics werden nicht künstlich verkleinert, um mehr LLM-Roundtrips, billigere Kontextstarts oder künstliche Projektphasen zu erzeugen. Features werden nach unabhängig prüfbarem Ergebnis und Reviewability geschnitten, nicht nach Worker-/PR-Größe.

## 15. Epic Ready for Preparation

Ein neuer Epic darf erst zur LLM-Vorbereitung gehen, wenn mindestens:

```text
PROJECT_FOUNDATION_ACCEPTED
CURRENT_CANONICAL_REPOSITORY_STATE_IDENTIFIED
EPIC_PRODUCT_TRACEABILITY_AVAILABLE
MATERIAL_PREDECESSOR_STATUS_KNOWN
OPEN_BLOCKING_PRODUCT_DECISIONS_IDENTIFIED
NO_CONCURRENT_UNBOUND_EPIC_START
```

Der Agent darf initiale Epic-Kandidaten/Abhängigkeiten im Repository anlegen, aber kein erstes normales Feature eines neuen Epics ohne externe gebundene Epic Preparation starten.

## 16. Epic Preparation Artifact, Research, Proportionality und Channel

Das Projekt stellt kanonische Locator bereit für:

```text
EPIC_PREPARATION_SUBJECT
EPIC_PREPARATION_BINDING_RECORD
EPIC_PREPARATION_REVIEW_RESULT_CHANNEL_AND_LOCATOR
```

Die Preparation bindet insbesondere:

```text
EPIC_ID
CURRENT_CANONICAL_BASELINE_OR_MAIN_SHA
PRODUCT_REFERENCES
PROJECT_TECHNICAL_FOUNDATION_REFERENCES
EPIC_OBJECTIVE_AND_EXPECTED_OUTCOME
EPIC_SCOPE_AND_NON_GOALS
PREDECESSORS_AND_DEPENDENCIES
MATERIAL_TECHNICAL_DELTA
HARD_INVARIANTS_AND_PROTECTED_BOUNDARIES
FEATURE_MAP_WITHOUT_TASK_MICROPLAN
RISK_AND_REVIEW_EXPECTATIONS
VERIFICATION_ACCEPTANCE_EVIDENCE_DIRECTION
EPIC_RESEARCH_REUSE_OR_DELTA_STATUS
RESEARCH_REFERENCES_AND_ACTIONABLE_CONCLUSIONS_WHERE_RELEVANT
MODEL_ROUTING_RISK_OR_QUALITY_EXPECTATIONS_WHERE_RELEVANT
OPEN_MATERIAL_DECISIONS
OPEN_AGENT_QUESTIONS
```

Foundation 2 besitzt technischen Repository-Locator/Resultatkanal. Foundation 1 besitzt Preparation-/Reviewsemantik und Verdict-Autorität.

Das Harness unterstützt kompakte Subjects durch Referenzen statt Kontextkopien:

```text
REFERENCE_CANONICAL_PRODUCT_AND_PROJECT_FOUNDATION
DO_NOT_DUPLICATE_FULL_HISTORY
KEEP_EPIC_RELEVANT_DELTA
KEEP_REQUIRED_INVARIANTS_RISKS_DEPENDENCIES_RESEARCH_AND_ACCEPTANCE_DIRECTION
```

Die vom vorbereitenden LLM gelieferte Research-Basis ersetzt keine implementierungsnahe Dependency-/API-/Runtime-Prüfung des Coding-Agenten.

## 17. Epic Critical Self-Review und unabhängiger Review

Der vorbereitende LLM führt vor Einreichung eine kritische Eigenprüfung durch. Diese Eigenprüfung ist keine unabhängige Verdict-Autorität.

Vor `EPIC_PREPARATION_REVIEW`:

```text
CANONICAL_EPIC_REVIEW_RESULT_CHANNEL_SCHEMA
-> EXTERNAL_EPIC_REVIEW_OUTPUT_SCHEMA_PREFLIGHT
-> PASS
-> EXECUTE_INDEPENDENT_EPIC_PREPARATION_REVIEW
```

Ein Epic wird nur `READY_FOR_AGENT`, wenn:

```text
EPIC_PREPARATION_SUBJECT_EXACTLY_BOUND
EPIC_BASELINE_EXACTLY_BOUND
EPIC_RESEARCH_REUSE_OR_DELTA_STATUS: REUSED_NO_MATERIAL_DELTA | UPDATED
EPIC_PREPARATION_CRITICAL_SELF_REVIEW_STATUS: COMPLETE__NO_OPEN_CRITICAL_BLOCKING_MAJOR_SELF_FINDINGS
EPIC_PREPARATION_REVIEW: PASS
OPEN_CRITICAL_FINDINGS: NONE
OPEN_BLOCKING_FINDINGS: NONE
OPEN_MAJOR_FINDINGS: NONE
OPEN_MATERIAL_USER_DECISIONS_REQUIRED_BEFORE_START: NONE
PRODUCT_AND_PROJECT_FOUNDATION_COMPATIBILITY_VALID
EXECUTION_AUTHORIZATION_SUFFICIENT
```

`FINDINGS: NONE` ist Ergebnis, nicht Zielvorgabe. Minor-Findings benötigen Korrektur oder explizite nichtblockierende Disposition; Nits erzeugen keine Endlosschleife. Korrigierte Subjects werden neu exakt gebunden und rereviewt.

## 18. Epic Ready for Agent und kompakter Start-Handoff

Erst nach `READY_FOR_AGENT` beginnt das erste normale Feature.

Kompakter Handoff:

```text
EPIC_ID
EPIC_PREPARATION_SUBJECT_IMMUTABLE_REFERENCE
EPIC_BINDING_OR_REVIEW_REFERENCE
CURRENT_CANONICAL_BASELINE_OR_MAIN_SHA
FOUNDATION_2_REFERENCE
EXECUTION_AUTHORIZATION_REFERENCE
```

Der Prompt dupliziert nicht die vollständige Preparation; der Agent lädt erforderlichen Kontext progressiv.

```text
SHORT_AGENT_PROMPT_BY_ROUTING
NOT_SHORT_AGENT_PROMPT_BY_OMITTING_REQUIRED_TRUTH
```

## 19. Adaptive Modell-/Reasoning-Zuordnung

Der Lead-/Integrator-Agent wählt konkrete Worker, verfügbare Modelle und unterstützte Reasoning-/Thinking-Stufen **just in time** innerhalb der aktuell autorisierten Agentenumgebung.

Auswahlfaktoren:

```text
TASK_COMPLEXITY
RISK
UNCERTAINTY
CONTEXT_REQUIREMENT
VERIFICATION_STRENGTH
COST
```

Ziel:

```text
LOWEST_EXPECTED_TOTAL_COST_OF_CORRECTLY_COMPLETED_AND_VERIFIED_RESULT
```

Nicht Ziel ist der billigste Einzelaufruf.

Regeln:

- kurzer Prompt oder kleiner Kontext allein beweist nicht, dass ein schwächeres Modell genügt;
- klar mechanische, reversible und stark deterministisch prüfbare Arbeit darf unmittelbar eine günstigere ausreichende Konfiguration nutzen;
- wenn eine **wiederkehrende oder systematisch zu routende Aufgabenklasse** unbekannt/unsicher ist, wird mit einer ausreichend leistungsfähigen Konfiguration und repräsentativer Verifikation eine Qualitätsbaseline hergestellt, bevor dauerhaft auf eine billigere Konfiguration optimiert wird;
- günstigere Konfigurationen werden bevorzugt, wenn Arbeit klar, reversibel, gut begrenzt, stark prüfbar und ihre Eignung evidenzbasiert ist;
- bei unerwarteter Komplexität, Unsicherheit, fehlgeschlagener Verifikation, schwierigem Debugging, breiter Integration oder erhöhtem Risiko wird ausreichend hoch eskaliert;
- Reviewer-Konfigurationen müssen der geforderten Reviewtiefe und Risikoklasse ausreichend gewachsen sein;
- eine stärkere Modellstufe ersetzt keine unabhängigen/spezialisierten Reviews;
- mechanische deterministische Arbeit wird bevorzugt durch Tools/Tests/CI statt zusätzliche LLM-Worker erledigt;
- erfolglose Wiederholungen mit erkennbar ungeeigneter niedriger Konfiguration ohne neue Erkenntnis werden vermieden.

Der Agent prüft reale Toolfähigkeit. Unterstützt die Umgebung keine abweichende Modell-/Reasoning-Zuordnung, verwendet er eine ausreichende vorhandene autorisierte Konfiguration und behauptet kein nicht vorhandenes Routing.

Eine vollständige vorab geplante Worker-/Modellmatrix ist nicht erforderlich. Epics werden nicht künstlich verkleinert oder Worker-Sessions neu gestartet, nur um einen nominell günstigeren Modellpfad zu erzwingen.

### Kosten-/Qualitätsevidence

Kostenoptimierung berücksichtigt soweit tatsächlich beobachtbar nicht nur monetäre Einzelkosten, sondern auch relevante Quota-/Usage-Belastung, zusätzliche Worker-/Kontextläufe, Fehlversuche, Review-/Integrationsaufwand und gegebenenfalls Latenz. Nicht beobachtbare Kosten werden nicht erfunden.

Wo Modellrouting materiell optimiert oder als Vorteil behauptet wird, werden verfügbare tatsächliche Nutzungs-/Ergebnisdaten herangezogen.

Es entsteht **kein umfangreiches Modell-Evaluationsartefakt auf Vorrat**. Wiederkehrende relevante Aufgabenklassen dürfen schlanke projektseitige Baselines/Regressionen erhalten, wenn sie nachweisbaren Nutzen für Qualität oder Kosten haben.

## 20. Autonome Featurearbeit innerhalb eines Epics

Nach `EPIC_READY_FOR_AGENT`:

```text
SELECT_READY_FEATURE_WITHIN_CURRENT_EPIC
-> VERIFY_PRODUCT_PROJECT_FOUNDATION_AND_EPIC_TRACEABILITY
-> RECORD_FEATURE_START_BASELINE
-> GIT_PREFLIGHT
-> EXPLORE_DELTA
-> PLAN_AT_APPROPRIATE_DEPTH
-> ALLOCATE_WORKERS_MODELS_AND_REASONING_JIT_WHERE_USEFUL
-> IMPLEMENT_SMALL_BATCHES
-> VERIFY
-> ASSESS_CURRENT_INCREMENT_RISK_AND_REQUIRED_REVIEW_COVERAGE
-> SELF_REVIEW_AND_REQUIRED_TECHNICAL_REVIEWS_FOR_CURRENT_INCREMENT
-> FIX_AND_REREVIEW
-> CHECK_RELEASE_TOPOLOGY_AND_CONTAINMENT
-> MERGE_SAFE_GREEN_INCREMENTS
-> REASSESS_CUMULATIVE_FEATURE_RISK
-> CONVERGE
-> READY_FOR_ACCEPTANCE_REVIEW
-> FEATURE_ACCEPTANCE_REVIEW
-> PASS_OR_CORRECTION_LOOP
-> NEXT_READY_FEATURE_WITHIN_SAME_EPIC
```

Vor **jeder Integration eines Inkrements** wird dessen aktuelles Risiko bewertet und die daraus erforderliche technische Reviewabdeckung erfüllt. Diese Inkrementprüfung ist zusätzlich zur späteren kumulativen Feature-Risikoprüfung und erzeugt **keinen externen `FEATURE_ACCEPTANCE_REVIEW` pro Task, PR oder Inkrement**.

Kein LLM-Preparation-Roundtrip ist standardmäßig vor jedem Feature erforderlich.

## 21. Epic Convergence und materielle Konflikte

Ein Epic ist `CONVERGED`, wenn:

```text
REQUIRED_EPIC_FEATURES_ACCEPTED_OR_EXPLICITLY_DISPOSED
OPEN_CRITICAL_BLOCKING_MAJOR_EPIC_FINDINGS: NONE
PRODUCT_TECHNICAL_FOUNDATION_EPIC_AND_REPOSITORY_TRUTH_SYNCHRONIZED
MATERIAL_OPEN_ITEMS_HAVE_TRIGGER_OR_NEXT_EPIC_DISPOSITION
```

```text
EPIC_CONVERGED
-> STOP_NEW_EPIC_AGENT_WORK
-> NEXT_EPIC_REQUIRES_NEW_LLM_EPIC_PREPARATION
```

Bei materieller Verletzung gebundener Grenzen:

```text
STOP_AFFECTED_WORK_ONLY
-> RECORD_EVIDENCE
-> REQUEST_ONLY_REQUIRED_MATERIAL_DECISION
-> UPDATE_PRODUCT_OR_PROJECT_TECHNICAL_FOUNDATION_IF_REQUIRED
-> EPIC_PREPARATION_DELTA
-> EPIC_PREPARATION_REREVIEW
-> EXACT_REBIND
-> RESUME
```

Nichtmaterielle reversible Implementation Details und Modell-/Reasoning-Zuordnung innerhalb autorisierter Grenzen erzeugen keinen LLM-Roundtrip.

## 22. Feature Ready, Größe und Auswahl

Feature Ready erfordert mindestens:

```text
PRODUCT_TRACEABILITY_VALID
PROJECT_TECHNICAL_FOUNDATION_COMPATIBILITY_VALID
CURRENT_EPIC_PREPARATION_COMPATIBILITY_VALID
ACCEPTANCE_CRITERIA_SUFFICIENTLY_CLEAR
MATERIAL_BLOCKING_DECISIONS_NONE
REQUIRED_PREDECESSORS_SATISFIED
EXECUTION_AUTHORIZATION_SUFFICIENT
FEATURE_REVIEWABILITY_PASS
```

Feature-Größe richtet sich nach eigenständig prüfbarem Ergebnis, kumulativem Diff/PR-Satz, Evidence- und Runtime-Verifikationsumfang. Zu große Features werden in eigenständig akzeptierbare Features geschnitten.

```text
DEFAULT_EXTERNAL_FEATURE_CONCURRENCY: ONE
```

Parallele Tasks innerhalb eines Features sind zulässig. Parallele externe Features benötigen isolierbare Subjects, Changesets, Baselines und Evidence. Featureauswahl innerhalb des aktuellen Epics bleibt agentenautonom, sofern keine materielle Produktpriorisierung erforderlich ist.

## 23. Adaptive Planungstiefe

```text
SIMPLE_TASK_OR_BUG -> ISSUE_OR_CLEAR_TASK + REPOSITORY_CONTEXT
NORMAL_FEATURE -> FEATURE_ISSUE + ACCEPTANCE_CRITERIA + RELEVANT_INVARIANTS
COMPLEX_OR_HIGH_RISK_FEATURE -> FEATURE_ISSUE + VERSIONED_SPEC_OR_EXECUTION_PLAN + RELEVANT_ADRS_AND_POLICIES
```

Epic Preparation ist kein Taskbacklog.

## 24. Spezialisierte Agenten, Skills, Hooks, Automations und CI

```text
REQUIRES_REASONING_OR_INDEPENDENT_JUDGMENT -> SPECIALIZED_AGENT_ROLE_OR_REVIEWER
REUSABLE_WORKFLOW -> SKILL
EVENT_BOUND_TRIGGER -> HOOK
DETERMINISTIC_INTEGRATION_PROPERTY -> CI_OR_MECHANICAL_GUARD
SCHEDULED_OR_RECURRING_WORK -> AUTOMATION
```

Default ist ein Lead-/Coding-Agent. Zusätzliche Rollen entstehen nur bei realem Nutzen.

## 25. Multi-Agent-Orchestrierung

Es gibt genau eine Lead-/Integrator-Verantwortung für Dependency-Graph, Agentenzuschnitt, Modell-/Reasoning-Zuordnung, Integration, Gesamtdiff, Endtests und Convergence.

Worker arbeiten schreibend isoliert und liefern mindestens:

```text
SCOPE
START_BASELINE
RESULT
CHANGED_ARTIFACTS
TESTS_AND_CHECKS
OPEN_FINDINGS
INTEGRATION_NOTES
```

Vor Integration wird die Worker-Baseline gegen den aktuellen Integrationsstand revalidiert und relevante Tests/Guards auf dem kombinierten Stand wiederholt.

Unabhängige Reviewer arbeiten in frischem/getrenntem Kontext und verändern den Reviewstand nicht gleichzeitig. Reviewerunabhängigkeit wird nicht dadurch ersetzt, dass derselbe Implementierungsagent ein stärkeres Modell verwendet.

## 26. Git-Preflight und Change Boundaries

Vor Mutation prüft der Agent mindestens Repository-Root, Remote, Zielref, Head, Working Tree, untracked Dateien und Staging.

Fremde Änderungen werden nicht stillschweigend gelöscht, gestasht, zurückgesetzt oder mitcommittet. Vor Commit/Merge wird der tatsächliche Diff geprüft. Risikoreiche Bereiche dürfen strengere `PROTECTED_AREAS` erhalten.

## 27. Trunk-/PR-Modell und Release-Topologie

`main` bleibt gesunde Development-Integrationslinie. Kurzlebige Branches, kleine reviewbare PRs und häufige Integration werden bevorzugt.

```text
MERGED_TO_MAIN != FEATURE_ACCEPTED != PRODUCTION_RELEASED
```

Vor einem Merge eines noch nicht extern akzeptierten Features prüft der Agent soweit relevant:

```text
MAIN_MERGE_DEPLOYMENT_EFFECT
FEATURE_ACTIVATION_PATH
RELEASE_GATE_PRESENT
UNACCEPTED_FEATURE_INERT_OR_ISOLATED
ROLLBACK_OR_DISABLE_PATH
```

Wird `main` produktiv aktiviert, braucht ein unakzeptiertes Feature geeignete Isolation/Disable-/Rollback-Pfade oder der Merge wird zurückgehalten. Bei produktionsrelevantem Critical/Blocking-Finding haben Eindämmung, Deaktivierung oder Revert Vorrang vor normaler Correction-Schleife.

## 28. Tests, CI, Guards und agent-readable Environment

Das Projekt erhält nur relevante Verifikationsklassen, beispielsweise Format/Lint/Typecheck/Build/Unit/Integration/Contract/E2E/Accessibility/Security/Migration/Performance/domänenspezifische Invarianten.

CI wiederholt Integrationsgates reproduzierbar. Allgemeine Guard-Claims benötigen zur Reichweite passende negative/positive/fail-closed Tests.

Nicht ausführbare Pflichtchecks halten den Gate offen und werden mit Grund, Auswirkung und Restrisiko dokumentiert.

Zugriffe bleiben getrennt:

```text
DOCUMENTATION_AND_STANDARDS_READ_ONLY
TOOLCHAIN_AND_PACKAGE_REGISTRIES
APPLICATION_OR_DATA_PROVIDERS
REAL_OR_PRODUCTION_DATA
```

## 29. Findings und technische Convergence

Severities:

```text
CRITICAL
BLOCKING
MAJOR
MINOR
NIT_OR_SUGGESTION
```

Materielle Findings bleiben sichtbar, bis sie nachvollziehbar disponiert sind. Zulässige Dispositionen sind insbesondere:

```text
FIXED
FALSE_POSITIVE_OR_NOT_APPLICABLE
DUPLICATE
FOLLOW_UP_TRACKED
EXPLICITLY_AUTHORIZED_NONCRITICAL_RISK_ACCEPTANCE
```

`FOLLOW_UP_TRACKED` oder Risikoakzeptanz dürfen keine noch gate-blockierende Critical/Blocking/Major-Semantik verdecken. Ein `MAJOR` wird nicht allein durch den Implementierungsagenten reklassifiziert.

Feature Convergence erfordert erfüllte Acceptance Criteria, keine offenen Critical/Blocking/Major-Findings, disponierte materielle Findings, grüne Pflichtchecks, erforderliche Reviewer, synchronisierte Living Docs und reproduzierbare Evidence.

## 30. Inkrement- und kumulative Risikoklassifikation

Vor Integration jedes Inkrements wird das **aktuelle Inkrementrisiko** bewertet und die daraus erforderliche technische Reviewabdeckung vor Merge erfüllt. Vor Feature Acceptance wird zusätzlich das **kumulative Feature-Risiko** bewertet.

```text
LOW_RISK -> SELF_REVIEW + CI MAY BE SUFFICIENT
ELEVATED_RISK -> INDEPENDENT_GENERAL_REVIEW REQUIRED
HIGH_RISK -> SPECIALIZED_REVIEWER_OR_REVIEWERS + REREVIEW_AFTER_FIXES
```

Berücksichtigt werden Security/Trust, sensible Daten, Finanz-/Tradingrisiko, Migration/Irreversibilität, Concurrency, destruktive Publication/Overwrite-Pfade, Providerkritikalität, Architekturänderung, Blast Radius, Testbarkeit und Observability.

Die Risikoklasse eines einzelnen Inkrements bestimmt seine **vor Integration** erforderliche technische Reviewerabdeckung. Die kumulative Feature-Risikoklasse bestimmt zusätzlich die erforderliche Reviewabdeckung vor `READY_FOR_ACCEPTANCE_REVIEW`. Diese technischen Reviews sind nicht gleichbedeutend mit einem externen LLM-`FEATURE_ACCEPTANCE_REVIEW` pro PR/Task.

High Risk darf nicht durch PR-Splitting oder schwache Worker-Klassifikation umgangen werden.

### Sensitive-Side-Effect-Risk-Floor

Wenn ein Feature materiell berührt:

```text
CONCURRENCY_SENSITIVE_CORRECTNESS
DESTRUCTIVE_OVERWRITE_OR_PUBLICATION
IRREVERSIBLE_OR_DIFFICULT_TO_RESTORE_SIDE_EFFECT
MATERIAL_TRUST_OR_SECURITY_BOUNDARY
```

darf `LOW_RISK` nur mit expliziter evidenzbasierter Begründung verwendet werden. Fehlt sie: mindestens `ELEVATED_RISK` + unabhängiger technischer Review.

## 31. Feature Evidence

Mindestens:

```text
FEATURE_ID_OR_ISSUE
PRODUCT_REQUIREMENT_AND_WORKFLOW_REFERENCES
PROJECT_TECHNICAL_FOUNDATION_REFERENCES
CURRENT_EPIC_ID_AND_EPIC_PREPARATION_REFERENCE
FEATURE_START_BASELINE_SHA
FEATURE_END_CANDIDATE_SHA
FEATURE_CHANGESET_REFS
NON_FEATURE_INTERVENING_CHANGES
INTEGRATED_END_STATE_INTERACTION_CHECK
ACCEPTANCE_CRITERIA
LINKED_TASKS_BUGS_AND_PRS
LOCAL_VERIFICATION_SUMMARY
CI_AND_REQUIRED_CHECKS_STATUS
FEATURE_CUMULATIVE_RISK_CLASS
RISK_CLASSIFICATION_RATIONALE_WHEN_REQUIRED
REQUIRED_REVIEW_COVERAGE
SPECIALIZED_REVIEWERS_USED
OPEN_FINDINGS_BY_SEVERITY
MATERIAL_DEVIATIONS_AND_DECISIONS
LIVING_DOCS_UPDATED
KNOWN_NON_BLOCKING_FOLLOW_UPS
CUMULATIVE_RUNTIME_OR_END_TO_END_EVIDENCE
```

Nutzernahe Evidence wie Screenshots, Conversation Traces, API-Beispiele oder End-to-End-Szenarien wird ergänzt, wenn sie den Review materiell verbessert.

Modell-/Reasoning-Metadaten sind **kein universelles Pflichtfeld**. Sie werden nur materialisiert, wenn für eine konkrete Qualitäts-/Kosten-/Provenienzbehauptung relevant.

## 32. Repository-Reviewkanäle, semantischer Mindestvertrag und Schema-Preflight

Für `PROJECT_FOUNDATION_REVIEW`, `EPIC_PREPARATION_REVIEW` und `FEATURE_ACCEPTANCE_REVIEW` definiert das Projekt jeweils einen eindeutigen kanonischen Resultatkanal/Locator oder einen gemeinsam eindeutig typisierten Kanal.

Foundation 2 besitzt den technischen Kanalvertrag; Foundation 1 besitzt Reviewsemantik und Verdict-Autorität. Foundation 1 konsumiert diesen technischen Vertrag und definiert für Repository-Reviews keine konkurrierende zweite Pflichtfeldliste.

Unabhängig von projektspezifischen Feldnamen oder zusätzlicher Struktur muss jedes externe Repository-Reviewresultat mindestens **semantisch enthalten oder eindeutig referenzieren**:

```text
REVIEW_ID
REVIEW_TYPE
REVIEWER_OR_REVIEW_AUTHORITY
RESULT_PROVENANCE
SUBJECT_ID_OR_EQUIVALENT_STABLE_SUBJECT_REFERENCE
SUBJECT_END_SHA_OR_EQUIVALENT_IMMUTABLE_END_STATE
VERDICT: PASS | CORRECTION_REQUIRED | BLOCKED
FINDINGS
REVIEWED_EVIDENCE_REFERENCE
REVIEW_RESULT_REFERENCE
```

`REVIEWED_EVIDENCE_REFERENCE` bindet die tatsächlich vom externen Reviewer geprüfte Evidence beziehungsweise einen gleichwertigen unveränderlich bestimmbaren Evidence-Locator. Subject, Evidence, Reviewautorität und Resultat müssen zusammengehörig und unabhängig validierbar bleiben. Ein unveränderter Code-/Subject-Endstand allein ersetzt diese Evidence-Bindung nicht.

Vor jedem externen Repository-Review muss der kanonische Kanal **sowohl** diesen semantischen Mindestvertrag als auch seine projektspezifischen Zusatzfelder erfüllen. Danach wird das angeforderte externe Output-Schema gegen genau diesen vollständigen autoritativen Vertrag validiert:

```text
CANONICAL_RESULT_CHANNEL
-> VALIDATE_SEMANTIC_MINIMUM_CONTRACT
-> VALIDATE_PROJECT_SPECIFIC_ADDITIONAL_SCHEMA
-> VALIDATE_EXTERNAL_REVIEW_OUTPUT_SCHEMA
-> PASS
-> EXECUTE_REVIEW
```

Bei fehlendem Mindestfeld, nicht eindeutigem Locator, Subject-/Evidence-/Authority-Mismatch oder sonstigem Schemafehler gilt fail-closed:

```text
BLOCK_BEFORE_REVIEW_OR_RESULT_CONSUMPTION
NO_GUESSING_OR_INVENTING_MISSING_BINDINGS
NO_RESULT_CHANNEL_MUTATION_TO_HIDE_MISMATCH
```

Auch beim späteren **Konsum** oder Transport eines Resultats werden Subject-, Evidence-, Authority- und Resultatbindung erneut gegen den kanonischen Vertrag geprüft. Ein projektspezifisch intern konsistentes, aber semantisch unvollständiges Schema ist nicht ausreichend.

## 33. Cardinality-independent append-only Review History

Reviewkanäle und Regressionstests unterstützen beliebig viele legitime sequenzielle Resultate, ohne Hardcoding aktueller History-Counts.

Unzulässig:

```text
RESULT_DIRECTORY_MUST_BE_EMPTY
EXACTLY_ONE_RESULT_EXISTS
EXACTLY_TWO_RESULTS_EXIST
CURRENT_HISTORY_COUNT_IS_HARDCODED
```

Invalid duplicates, ID-/Filename-Mismatches, falsche Subjects, fehlende Reviewautorität, fehlende Provenienz, fehlende Evidence-Bindung und andere Verletzungen des semantischen Mindestvertrags bleiben fail-closed. Mehrere unterschiedliche legitime Review-IDs dürfen denselben immutable Subject prüfen, wenn der kanonische Reviewvertrag dies zulässt und die jeweilige Evidence-/Authority-Bindung eindeutig bleibt.

## 34. Review Transport

```text
REVIEWER_CAN_WRITE_CANONICAL_CHANNEL
-> WRITE_EXACT_RESULT_DIRECTLY

REVIEWER_CANNOT_WRITE_CANONICAL_CHANNEL
-> RETURN_PROVENANCE_BOUND_PAYLOAD
-> EXACT_AUTHORIZED_TRANSFER
-> NO_REINTERPRETATION_OR_RECLASSIFICATION
```

Implementierungsagent besitzt keine externe Verdict-Autorität. Der Transport bewahrt den vollständigen semantischen Mindestvertrag unverändert; ein semantisch unvollständiges Resultat darf nicht allein deshalb akzeptiert werden, weil es unverändert transportiert wurde.

## 35. Project Foundation Review und External Project Context Sync

Foundation Review bindet Product Truth, Technical Foundation Preparation, Foundation-2-Provenienz, exakten Repositorysubject und Foundation Evidence.

Bei `PASS` folgt erforderlicher externer Project-Context-Sync oder `NOT_APPLICABLE`, **danach zuerst `FIRST_EPIC_PREPARATION`**, kein beliebiger Featurestart.

```text
PROJECT_FOUNDATION_REVIEW_PASS
-> REQUIRED_EXTERNAL_REVIEW_BOOTSTRAP_INSTALL_SYNC_OR_NOT_APPLICABLE
-> FIRST_EPIC_PREPARATION
```

Der Agent darf eine erforderliche externe Installation/Sync nicht vor Nutzer- beziehungsweise externer Bestätigung behaupten.

## 36. Feature Acceptance Gate

Feature Acceptance prüft kumulatives Featureergebnis gegen Product Truth, Project Technical Foundation, aktuellen Epic, Acceptance Criteria und Feature Evidence.

`FEATURE` bleibt normale große externe Acceptance-Grenze.

## 37. Development Security und Supply Chain

Keine Secrets in Repo/Issues/Berichten, Least Privilege, sichere Input-/Path-/Upload-Verarbeitung soweit relevant, risikobasierte Dependency-/Supply-Chain-Prüfung, reproduzierbare Lockfiles/Baselines und keine Produktionsdaten ohne Freigabe.

Dependencies werden auf Transitivität, Lockfile-/Reproduzierbarkeit, Wartung, Security, Lizenz/Provenienz, Integrations-/Betriebswirkung und native Alternativen geprüft.

## 38. Production Readiness und Operations

Vor realen Nutzern, Produktionsdaten oder produktiven Ressourcen erfolgt ein eigener Production-Readiness-Lauf.

Operationsprofile decken soweit relevant Hosting/Runtime, Deployment, Aktivierung, Rollback, Secrets, Access, Observability, Alerting, Backup/Restore, Migration/Recovery, Retention/Löschung, Incidents, Provider-Quotas/Kosten und SLOs ab.

Produktionsaktion erst nach expliziter Autorisierung.

Im Operations-Modus wird ein kontrollierter Change-Pfad verwendet:

```text
FINDING_OR_REQUEST
-> ISSUE_OR_AUTOMATED_WORK_ITEM
-> AGENT_ANALYSIS
-> SHORT_LIVED_BRANCH
-> FIX_OR_MAINTENANCE_CHANGE
-> TESTS_AND_CHECKS
-> PR
-> REQUIRED_REVIEW_BY_RISK
-> FINDING_DISPOSITION_AND_CONVERGENCE
-> MERGE
-> DEPLOYMENT_ACCORDING_TO_OPERATIONS_PROFILE
-> POST_CHANGE_VERIFICATION
```

Automatisches Mergen oder Deployment erfolgt nur, wenn das Operationsprofil dies für die jeweilige Risikoklasse ausdrücklich erlaubt.

## 39. Harness Improvement und Evidence Discipline

Wiederkehrende Probleme werden auf den kleinsten dauerhaften Mechanismus abgebildet:

```text
OBSERVE_REAL_FAILURE_OR_REPETITION
-> GENERALIZE_INVARIANT
-> ADD_SMALLEST_MECHANISM_WITH_REGRESSION_VALUE
```

Dies gilt auch für Modellrouting: Erst reale wiederkehrende Aufgaben-/Qualitäts-/Kostenevidence rechtfertigt zusätzliche Routingregeln oder Baselines.

Evidence-Klassen:

```text
LOCAL_AGENT_REPORTED
REPOSITORY_OR_REMOTE_VERIFIED
CI_VERIFIED
RUNTIME_OR_OPERATION_VERIFIED
```

## 40. Antipatterns

```text
FULL_GENERAL_FOUNDATION_ON_EVERY_FEATURE_RUN
FULL_PROJECT_REDISCOVERY_BEFORE_EVERY_EPIC
LLM_PREPARATION_BEFORE_EVERY_FEATURE_TASK_BUG_PR_OR_COMMIT
STARTING_NEW_EPIC_WITHOUT_BOUND_REVIEWED_EPIC_PREPARATION
MICRO_EPICS_CREATED_FOR_MORE_LLM_GATES_OR_CHEAPER_MODEL_CONTEXTS
REPEATING_EPIC_PREPARATION_WITHOUT_CURRENT_STATE_DELTA_VALUE
EPIC_BRIEF_WITH_FULL_HISTORY_COPY_INSTEAD_OF_GIT_LOCATORS
LONG_AGENT_PROMPT_REPEATING_CANONICAL_EPIC_CONTENT
SHORT_AGENT_PROMPT_OMITTING_REQUIRED_TRUTH_INSTEAD_OF_ROUTING_TO_IT
MICROPLAN_FROM_LLM_TREATED_AS_TASK_SCRIPT
EPIC_SELF_REVIEW_MISREPRESENTED_AS_INDEPENDENT_REVIEW
FORCING_FINDINGS_NONE_AS_TARGET
RESEARCH_OR_OPEN_SOURCE_SURVEY_WITHOUT_MATERIAL_DELTA_VALUE
OPEN_SOURCE_SELECTION_BY_POPULARITY_ALONE
RESEARCH_TREATED_AS_AUTHORIZATION_TO_INSTALL_OR_COPY
CHEAPEST_MODEL_ALWAYS_FIRST_WITHOUT_QUALITY_BASELINE_WHEN_SYSTEMATIC_ROUTING_IS_UNCERTAIN
SHORT_CONTEXT_ASSUMED_TO_IMPLY_LOW_REASONING_NEED
STRONGER_MODEL_USED_TO_BYPASS_REQUIRED_INDEPENDENT_REVIEW
CROSS_PROVIDER_ROUTING_WITHOUT_AUTHORIZATION
FABRICATED_MODEL_OR_COST_METRICS
MODEL_EVALUATION_BUREAUCRACY_ON_SPEC_WITHOUT_OBSERVED_VALUE
ONE_FILE_PER_REQUIRED_CAPABILITY_BY_DEFAULT
SPECIALIZED_AGENTS_SKILLS_HOOKS_AUTOMATIONS_ON_SPEC
LONG_LIVED_FEATURE_BRANCHES
DEVELOP_BRANCH_AS_SECOND_TRUNK
BIG_BANG_INTEGRATION
BLIND_GIT_ADD_ALL_WITHOUT_DIFF_REVIEW
BLIND_CLEANUP_OR_STASH_OF_FOREIGN_CHANGES
SECRETS_IN_GIT_OR_ISSUES
SELF_WEAKENING_GOVERNANCE_TO_PASS_ACTIVE_GATE
IMPLEMENTING_AGENT_FABRICATING_EXTERNAL_REVIEW_PASS
REPOSITORY_REVIEW_CHANNEL_WITHOUT_SEMANTIC_MINIMUM_CONTRACT
REVIEW_RESULT_WITHOUT_EXACT_SUBJECT_EVIDENCE_AUTHORITY_BINDING
HAND_AUTHORED_EXTERNAL_REVIEW_SCHEMA_DRIFT
REVIEW_HISTORY_TESTS_BOUND_TO_CURRENT_RESULT_COUNT
LOW_RISK_WITHOUT_REQUIRED_JUSTIFICATION_ON_MATERIAL_SENSITIVE_SIDE_EFFECT_PATH
PARALLEL_FEATURES_WITH_AMBIGUOUS_ACCEPTANCE_SUBJECT
LOW_RISK_INCREMENT_SPLITTING_TO_EVADE_HIGH_RISK_FEATURE_REVIEW
TOOL_INTERNAL_STATE_AS_PROJECT_STATUS
BROWNFIELD_REWRITE_WITHOUT_DELTA_JUSTIFICATION
```

## 41. Qualitätskriterien

Die projektspezifische Umsetzung ist gelungen, wenn:

- ein neuer Agent Product Truth, Project Foundation und aktuellen Epic-Kontext ohne alten Chat findet;
- High-Level-Discovery nicht unnötig wiederholt wird;
- Epic/Feature/Task und Issue/PR eindeutig getrennt sind;
- vor jedem neuen Epic ein kompakter critically-self-reviewed und unabhängig reviewed Git-bound Preparation Subject existiert;
- Research als relevanter Delta-/Reuse-Check erfolgt statt als ritualisierte Vollrecherche;
- Epic Preparation den Agentenkontext reduziert statt Bürokratie zu verdoppeln;
- kurzer Agentenprompt durch Git-Routing möglich ist, ohne erforderliche Wahrheit wegzulassen;
- Lead/Integrator Worker, Modell und Reasoning JIT innerhalb autorisierter Grenzen passend zu Aufgabe/Risiko/Qualität/Kontext/Kosten zuweist;
- Kostenoptimierung die Gesamtkosten korrekt verifizierter Ergebnisse betrachtet;
- systematisch geroutete unbekannte Aufgabenklassen nicht blind auf die billigste Konfiguration gesetzt werden;
- fehlende Modellroutingfähigkeit transparent fällt back statt erfunden zu werden;
- unabhängige Reviews nicht durch stärkere Implementierungsmodelle ersetzt werden;
- Findings nachvollziehbar disponiert bleiben und Major-Grenzen nicht selbst abgeschwächt werden;
- vor Integration jedes Inkrements dessen Risiko und erforderliche technische Reviewabdeckung geprüft sind;
- Agent innerhalb des Epics Features/Tasks/PRs autonom konvergiert;
- Feature weiterhin externe Acceptance-Grenze bleibt;
- Brownfield delta-first bleibt;
- Lean Harness ohne Vorratsbürokratie skaliert;
- Git-/Governance-/Risk-Grenzen intakt bleiben;
- Release-/Operations-Grenzen und unakzeptierte Feature-Containment erhalten bleiben;
- Repository-Reviewkanäle den semantischen Mindestvertrag einschließlich Reviewautorität und tatsächlich geprüfter Evidence binden;
- Review-Schemas vor Ausführung kanonisch validiert und Resultate beim Konsum fail-closed gegen Subject-/Evidence-/Authority-Bindung geprüft werden;
- History cardinality-independent ist;
- Production Readiness separat bleibt.

## 42. Gesamtalgorithmus

```text
APPROVED_PRODUCT_DEFINITION
+ EXACT_BOUND_PROJECT_TECHNICAL_FOUNDATION_PREPARATION
+ FOUNDATION_2
+ EXECUTION_ENVELOPE
-> PROJECT_BOOTSTRAP_OR_BROWNFIELD_DELTA
-> PROJECT_FOUNDATION_READY_FOR_REVIEW
-> PROJECT_FOUNDATION_REVIEW_PASS
-> EXTERNAL_PROJECT_CONTEXT_SYNC_OR_NOT_APPLICABLE
-> EPIC_READY_FOR_PREPARATION
-> EXTERNAL_LLM_RESEARCHES_RELEVANT_DELTA_AND_PREPARES_CURRENT_STATE_EPIC
-> EPIC_PREPARATION_PROPORTIONALITY_PASS
-> EPIC_PREPARATION_CRITICAL_SELF_REVIEW
-> EPIC_PREPARATION_INDEPENDENT_REVIEW_PASS
-> EXACT_BOUND_EPIC_PREPARATION
-> COMPACT_EPIC_AGENT_START_LOCATOR_HANDOFF
-> CODING_AGENT_AUTONOMOUS_FEATURE_LOOP_WITH_JIT_WORKER_MODEL_REASONING_ALLOCATION
-> ASSESS_INCREMENT_RISK_AND_REQUIRED_REVIEW_BEFORE_EACH_INTEGRATION
-> FEATURE_ACCEPTANCE_REVIEW_PER_FEATURE
-> EPIC_CONVERGED
-> NEXT_EPIC_RETURNS_TO_LLM_PREPARATION
-> PRODUCTION_READINESS_WHEN_DUE
-> OPERATIONS
```

Diese Grundlage setzt den LLM an **wenigen großen Product-/Foundation-/Epic-/Acceptance-Grenzen** ein und hält die Agentenläufe dazwischen kompakt, autonom, risikoadäquat, evidenzstark und kostenbewusst.