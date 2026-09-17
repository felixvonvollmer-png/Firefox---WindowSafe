# Architektur, Entscheidungen und Vorab-Gates

## Übernommene Grenzen

Die normative technische Beschreibung ist die unveränderte r6 in
`foundation/inputs/inputs/WindowSafe_Technical_Foundation_WS-TFP-20260917-01_r6.md`.
Ihre §§2–10 und I01–I10 bleiben verbindlich. Dieses Dokument ist Routing und
Engineeringentscheidung, keine alternative Product Truth.

T01: Firefox Desktop 156 als gewählte Mindest-/Referenzversion, Windows und Ubuntu.
Das ist eine gebundene Zielentscheidung, keine hier geprüfte Kompatibilität.
T02: R500/R2000/H mit allen Ressourcen-, Latenz- und Safety-Zielen aus r6 §9.1.
T03: regulär 14 Sitzungscheckpoints und 50 geschlossene Fensterstände; geschützte
Recovery-Inhalte bleiben zusätzlich erhalten. T04: native IndexedDB,
unlimitedStorage/contextualIdentities innerhalb der vereinbarten Zweckgrenzen.
G01: Repository bleibt öffentlich, reale Browserdaten bleiben ausgeschlossen.
T05-R2: harte Mediane 10/20 %, inklusive Einzellaufcaps 15/30 %, Burst 20/40 %;
5/10 % sind allein nicht blockierende Soft-Ziele. Keine Safety-/Latenzabschwächung.

## Reversible Engineeringentscheidungen dieses Laufs

**WS-ADR-001 / ACCEPTED_ENGINEERING:** Die Foundation nutzt Python 3.14.4 und
Standardbibliothek für Inputintegrität, Reviewvertrag, Historienprüfung und
synthetische Harness-Tests. Keine Drittanbieter-Python-Pakete, keine Produktlaufzeit.
Das vermeidet ein unbenutztes Add-on-Gerüst vor den harten Implementierungsgates.

Die bevorzugte Produktrichtung bleibt Firefox-only MV3 Event Page, striktes
TypeScript und native kleine HTML/CSS-Oberfläche, kein UI-/DB-Framework, Server,
Native-Messaging-Helper oder Content-Script. Erfassung/Identitätsabgleich →
Recovery-Regeln → ein kontrollierter IndexedDB-Schreibpfad; UI, Backup und Import
verwenden denselben Konsistenzvertrag. Details werden erst innerhalb eines
autorisierten und qualifizierten Epics implementiert.

**WS-ADR-002 / DEFERRED_WITH_TRIGGER:** Produkt-Build, TypeScript-Compiler,
Node-/web-ext-Versionen und Manifest werden vor dem ersten autorisierten
Produkt-/Packaging-Inkrement gemeinsam kompatibel festgeschrieben und geprüft.
Sie sind für diesen reinen Foundation-Subject NOT_APPLICABLE; keine Dummy-
Erweiterung und kein web-ext-Erfolg werden behauptet. Das ist eine reversible
JIT-Toolingentscheidung; die bevorzugte Produkttechnologie wird nicht ersetzt.

**WS-ADR-003 / ACCEPTED_ENGINEERING:** Ein typisierter JSON-Reviewkanal für
Foundation, Epic Preparation und Feature Acceptance, mit einem vollständigen
kanonischen Vertragsdokument und einer kleinen expliziten Validatorimplementierung.
Es wird kein universeller JSON-Schema-Validator behauptet. Schema-Preflight verlangt
exakte strukturelle Gleichheit mit diesem Vertrag am Subject-SHA; Ergebnisprüfung
bindet SHA, Evidence, Rolle und Resultatpfad. Provenienz muss zusätzlich unabhängig
kontrolliert werden; Strukturprüfung authentifiziert keine Person.

**WS-ADR-004 / ACCEPTED_ENGINEERING:** Initiale Integration in Development-main
nach internem Review und lokalen Gates, anschließend CI am veröffentlichten SHA.
Kein Deploymentpfad, kein Add-on-Artefakt, keine Releaseaktion. Branchschutz wird
nicht administrativ verändert; CI plus Agentenpolicy und externes Reviewgate sind
der funktionale Fallback. Spätere Inkremente bevorzugen kurze Branches/kleine PRs.

## Offene Gates mit Triggern

| Gate | Status und notwendiger späterer Nachweis |
|---|---|
| WS-GATE-PLATFORM / r6 §7.1 | REQUIRED_BEFORE_AFFECTED_PRODUCT_IMPLEMENTATION: exakter Zielbuild, API-/Erkennungsqualifikation für Sonderfenster, Restoregrenzen, verborgene Tabs, Gruppen/Split/Containerkombinationen. Keine produktive Erfassung vor sicherer Erkennung. |
| WS-GATE-MEASUREMENT / r6 §§9.1/9.3 | REQUIRED_BEFORE_AFFECTED_PRODUCT_IMPLEMENTATION: konkrete Tools/Trace, OS-/Firefox-Build, Hardware, Warm-up, Profilzustand, Hintergrundlast, Unsicherheit und gepaarte A/B-Methode binden; mindestens fünf Paare je Profil/OS. |
| WS-GATE-NATIVE | REQUIRED_BEFORE_FEATURE_ACCEPTANCE: echte Integrations-/Abbruch-/Restart-/Performance-Nachweise der späteren Implementation; kein Ersatz durch Modelltests oder temporär geladenes Add-on. |
| WS-GATE-TEST-ENVELOPE | BEFORE_ANY_BROWSER_PROBE: separat autorisierte künstliche Profile und geeigneter Installationsweg. Dieser Lauf startet keinerlei Browserprobe. |
| WS-GATE-DELIVERY | BEFORE_DISTRIBUTION: Lizenz, Installations-/Signierungs-/Verteilungsweg und Production Readiness separat entscheiden. Keine AMO-Aktion. |

Diese Punkte blockieren die betroffene spätere Arbeit, nicht diesen reinen
Foundation-Bootstrap. Qualifikationen erhalten später ein Git-gebundenes
Evidence-Dokument plus Autorisierungsreferenz; keine Platzhalter zählen als PASS.
Die Epic Preparation muss deren exakte Locator aufnehmen. Unklare Fakten bleiben
offen; materielle Funktionsabstriche verlangen Nutzerentscheidung und Rebinding.

## Sicherheits- und Risikogrenze

Das spätere Produkt hat mindestens Elevated Risk wegen sensibler Metadaten,
Concurrency, Recovery und destruktiver Bereinigung; spezialisierte Reviews werden
risikobezogen fällig. Das aktuelle Inkrement ist LOW_RISK: ausschließlich
Dokumente und offline arbeitender Repository-Harness, kein Browserzugriff, keine
Datenspeicherung/-löschung im Produkt und keine externe Runtimewirkung.
Policy und Inputintegrität werden mechanisch geprüft, Verdict-Autorität bleibt
außerhalb des implementierenden Agenten. Diese Einstufung gilt nicht für spätere
Produktfeatures und senkt deren Risikofloor nicht.
