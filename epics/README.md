# Initiale Epic-Karte und Preparation-Kanal

**WS-E01 / CANDIDATE_NOT_STARTED:** Zuverlässige lokale Fenster-/Sitzungssicherung
und manuelle Wiederherstellung (V1). Product-Anker WS-GOAL, WS-CAP-01–04,
WS-RESTORE, WS-BACKUP, WS-QUALITY, WS-AC-01–11; Technical Foundation r6 §11.

Ein zusammenhängender V1-Epic, keine Mikro-Epics. Denkbare Feature-Richtungen sind
konsistente Erfassung/Recovery-Datenhaltung, benannte Fenster/manuelle kontexttreue
Wiederherstellung und Dateibackup/Import. Schnitt und Reihenfolge werden erst in
der späteren Epic Preparation konkretisiert; keine Dateien, Klassen, Tasks oder
PRs für Produktimplementierung sind vorgeplant.

Voraussetzungen: PROJECT_FOUNDATION_REVIEW PASS, externer Kontext-Sync oder
begründetes NOT_APPLICABLE, aktueller kanonischer SHA, bekannte Vorgänger und offene
Entscheidungen, keine parallelen ungebundenen Epicstarts. Plattform-/Messgates aus
`foundation/architecture.md` müssen vor betroffener Implementierung erfüllt sein.

## Kanonische Locator (noch nicht materialisierte JIT-Artefakte)

- Epic Preparation Subject: `epics/<EPIC_ID>/subject.json` mit Verweisen auf den
  fachlichen Preparation-Text und dessen Evidence.
- Binding: `epics/<EPIC_ID>/binding.json`.
- Gemeinsamer Resultatkanal: `reviews/results/<REVIEW_ID>.json`, typisiert als
  `EPIC_PREPARATION_REVIEW`, Vertrag `reviews/review-contract.json`.
- Feature Subject/Evidence später: `features/<FEATURE_ID>/subject.json`.

Der Preparation-Subject bindet Epic-ID, exakten aktuellen main-SHA, Product-/
Foundationreferenzen, Ziel/Outcome, Scope/Nichtziele, Vorgänger, technische Deltas,
Invarianten, Feature-Richtungen ohne Task-Mikroplan, Risiken/Reviewanforderungen,
Evidence-/Acceptance-Richtung, Research-Reuse/Delta und Quellen/Schlussfolgerungen,
relevante Modell-/Qualitätsgrenzen, offene Nutzerentscheidungen/Agentenfragen und
OPEN_LATER mit Triggern. Research-Status: REUSED_NO_MATERIAL_DELTA oder UPDATED.

Vor unabhängigem Review: Proportionality Pass und kritische Eigenprüfung mit
`COMPLETE__NO_OPEN_CRITICAL_BLOCKING_MAJOR_SELF_FINDINGS`; danach mechanischer
Schema-Preflight. Foundation 1 besitzt Preparationsemantik und Verdict-Autorität,
Foundation 2 den hier definierten technischen Kanal.

READY_FOR_AGENT braucht exakten Subject/Baseline/Review-PASS, valide Product-/
Foundationkompatibilität, keine offenen Critical/Blocking/Major, keine vor Start
offenen materiellen Nutzerentscheidungen und ausreichende Execution Authorization.
Ein kompakter Handoff routet zu diesen Git-Referenzen. Kein erster Featurestart
durch bloße Erstellung dieses Locators.

Nach Features folgt jeweils unabhängige kumulative FEATURE_ACCEPTANCE_REVIEW.
Epic Convergence verlangt angenommene oder explizit disponierte notwendige
Features, keine offenen Epicblocker und synchronisierte kanonische Wahrheit.
Jeder neue Epic braucht erneut extern vorbereitete und geprüfte Epic Preparation.
