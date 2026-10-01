# Epic-Karte und Preparation-Kanal

## Aktuelles Gate: WS-E01 Epic Preparation Delta

Die nachfolgende READY_FOR_AGENT-Annahme ist historisch und bleibt unverändert.
Der [WS-P05-Foundation-Subject](../foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json)
ist per [Acceptance-Binding](../foundation/deltas/WS-PFDELTA-MAT-20260928-01/binding.json)
mit unabhängigem PASS angenommen. Externer Context-Sync: CONFIRMED_BY_USER
(WS-EXTCTX-SYNC-20260929-01).

**WS-E01-EP-DELTA-20260929-02** (Delta zur historischen WS-E01-EP-20260919-01) liegt unter
`epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-02/`: exakte Project-LLM-Originale
(`preparation.md`, `critical-self-review.md`, Nutzerrichtung, Sync, Beschreibung,
Vorversion), Autorisierung WS-EA-20260929-02, versionierter `subject.json`, Binding
REVIEW_REQUIRED mit `ready_for_agent: false` und `evidence.md`. Der unabhängige
WS-E01-EPR-DELTA-20260929-01 (`reviews/results/WS-E01-EPR-DELTA-20260929-01.json`) ergab
**CORRECTION_REQUIRED** am Head `48d7b0f97eacecd7515f7cbf064955303b0d5767`; dieser Namespace
bleibt unverändert historisch.

**WS-E01-EP-DELTA-20260929-03** unter `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-03/`
korrigiert ausschließlich die drei Reviewfindings (Korrektur, Disposition, Self-Review und
WS-EA-20260929-03 als Originale; neuer Subject, Binding REVIEW_REQUIRED, `evidence.md`).
Fachliche Epic-/Product-/TF-Aussage unverändert. Am Head `dee7ab5c9c5b53accd8602105e87523510582e40`
erhielt -03 WS-E01-EPR-DELTA-20260929-02 **BLOCKED** (Reviewer ohne Checkout) und die
nutzerautorisierte Ersatz-Evidence WS-E01-EPR-DELTA-20260930-04 **CORRECTION_REQUIRED**
(`RECONSTRUCTED_FROM_REVIEW_TRANSCRIPT`): Autorin der übernommenen -02-Preparation fehlte in
der Ausschlussmenge. -03 bleibt historisch unverändert.

**WS-E01-EP-DELTA-20260929-04** unter `epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/`
(WS-EA-20260930-01) schließt diese Fehlerklasse: Der Harness leitet die transitiven Autoren
und Materializer der referenzierten Preparation-/Correction-/Supersession-Linie ab und
lehnt Request/Check ab, wenn eine davon in `review_excluded_identities` fehlt. Fachlich
unverändert; Pending-Binding REVIEW_REQUIRED bleibt erhalten. Unabhängiger Rereview
WS-E01-EPR-DELTA-20260930-05 am `fa109e1b2cea025918d1cff61a2aaee2ee2b2083`: **PASS**.
Exaktes Rebinding **READY_FOR_AGENT** in `rebinding.json` (WS-EA-20260930-02); es ist ab jetzt
das aktuelle WS-E01-Binding, integriert in main `714b440c26167f6411420fbbda4be69deb2e9670`.
Separate breite Ausführungsautorisierung WS-EA-20261001-03:
`epics/WS-E01/evidence/broad-execution-authorization.json`. Feature-Subjects liegen unter
`features/WS-E01-F0<n>/subject.json`; Produktquellen unter `addon/`, Qualifikationsproben unter
`qualification/ws-e01-f0<n>/`.
PR #3 (Head `7d66ca5b025c8f748d7f97b961c496ee450daaa7`) bleibt Draft/ungemergt als historische
F01-Evidence; F01 wird unter WS-EA-20261001-03 auf neuer Basis fortgesetzt.
Nach EPIC_CONVERGED stoppt neue Epic-Arbeit bis Project-LLM-/Nutzer-Richtungsreview;
der Nutzer bestätigt die nächste Epic-Auswahl vor neuer Preparation.

## Historisch angenommene Preparation


**WS-E01 / READY_FOR_AGENT (Preparation angenommen):** Zuverlässige lokale Fenster-/Sitzungssicherung
und manuelle Wiederherstellung (V1). Product-Anker WS-GOAL, WS-CAP-01–04,
WS-RESTORE, WS-BACKUP, WS-QUALITY, WS-AC-01–11; Technical Foundation r6 §11.

Ein zusammenhängender V1-Epic, keine Mikro-Epics. Die bytegetreu materialisierte
[Preparation](WS-E01/preparation.md) beschreibt Feature-Richtungen und Abhängigkeiten.
[Subject](WS-E01/subject.json) und [Binding](WS-E01/binding.json) binden
WS-E01-EP-20260919-01 an main `dc9c1c37a264cc80f79ec08bf166ec42cdd73b95` und den
integrierten Foundation-PASS WS-PFR-20260918-02. External Context Sync NOT_APPLICABLE.
Unabhängiger [Preparation-PASS WS-E01-EPR-20260919-02](../reviews/results/WS-E01-EPR-20260919-02.json)
für den exakten SHA `644b81f63dcc1990bc894a9c2c9bd8dc24a98c04`;
das aktuelle Binding setzt `ready_for_agent: true`. Der ursprüngliche Subject
bleibt mit seinem damaligen Reviewstatus unverändert. Das OPEN/MINOR bleibt im
Original erhalten; sein Routing-Follow-up ist in [reviews/README.md](../reviews/README.md)
dokumentiert. WS-EA-20260919-05 autorisiert diesen Accepted-Binding-/Integrations-
übergang und STOP nach Post-Merge-Prüfung. Kein Featurestart oder Browser-/Profiltest.

Voraussetzungen: PROJECT_FOUNDATION_REVIEW PASS, externer Kontext-Sync oder
begründetes NOT_APPLICABLE, aktueller kanonischer SHA, bekannte Vorgänger und offene
Entscheidungen, keine parallelen ungebundenen Epicstarts. Plattform-/Messgates aus
`foundation/architecture.md` müssen vor betroffener Implementierung erfüllt sein.

## Kanonische Locator

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
