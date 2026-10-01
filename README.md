# WindowSafe

WindowSafe soll lokale Firefox-Fenster und Sitzungen sichern und nach einer
Nutzeraktion wiederherstellen. Dieses Repository enthält derzeit ausschließlich
die integrierte **Project Foundation** und die WS-E01 Epic Preparation, keine
installierbare Erweiterung oder Produktfunktion.

Aktuell: Project Foundation Delta **WS-PFDELTA-MAT-20260928-01** (WS-P05, finale V6-Router)
ist mit dem unabhängigen [WS-PFR-DELTA-20260928-01 PASS](reviews/results/WS-PFR-DELTA-20260928-01.json)
angenommen und durch **WS-PFDELTA-INT-20260929-01** / **WS-EA-20260929-01** integriert.
[Acceptance-Binding](foundation/deltas/WS-PFDELTA-MAT-20260928-01/binding.json),
[reviewed Subject](foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json) und [Evidence](foundation/deltas/WS-PFDELTA-MAT-20260928-01/evidence.md).
Externer Project-Context-Sync: **CONFIRMED_BY_USER** (WS-EXTCTX-SYNC-20260929-01).
Aktuell: WS-E01 Epic Preparation Delta **WS-E01-EP-DELTA-20260929-04** ist unabhängig mit
WS-E01-EPR-DELTA-20260930-05 **PASS** angenommen und exakt rebound (READY_FOR_AGENT,
`epics/WS-E01/deltas/WS-E01-EP-DELTA-20260929-04/rebinding.json`), integriert in main
`714b440c26167f6411420fbbda4be69deb2e9670`. Breite WS-E01-Ausführung unter WS-EA-20261001-03
(`epics/WS-E01/evidence/broad-execution-authorization.json`).
Die Vorversionen -02 (CORRECTION_REQUIRED) und -03 (BLOCKED, danach CORRECTION_REQUIRED als
nutzerautorisierte rekonstruierte Ersatz-Evidence) bleiben historisch unter `reviews/results/`.
Historische WS-E01 Preparation bleibt unverändert angenommen; ihre Annahme ersetzt
kein Delta-Rebinding. F01 bleibt auf PR #3 am Head `7d66ca5b025c8f748d7f97b961c496ee450daaa7`
Draft/ungemergt, gestoppt und wird nicht fortgesetzt. Kein Produktcode oder Feature Acceptance.

- [Kontext und unveränderte Product Truth](foundation/context.md)
- [Architektur, Entscheidungen und offene Vorab-Gates](foundation/architecture.md)
- [Engineering, Git, Risiko und Entwicklungsbefehle](foundation/engineering.md)
- [Kanonischer Reviewvertrag und Reviewer-Handoff](reviews/README.md)
- [Historischer Korrektur-Subject](foundation/subject.json) und [Evidence](foundation/evidence/followup-correction.md)
- [Reviewer-Umgebung und historische Qualifikation](foundation/reviewer-environment.md)
- [Epic-Karte und Preparation-Locators](epics/README.md)

## Lokal prüfen

Python **3.14.4** und Git genügen; keine Python-Pakete, Browser oder Profile:

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build
```

`build` benötigt die qualifizierten POSIX-No-follow-/dir_fd-Fähigkeiten und
erzeugt ein deterministisches Foundation-Inventar in `build/`; es baut
kein Firefox-Add-on. Nach einem Commit liefert
`python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json` nach Prüfung des Accepted-Bindings den ursprünglichen
Reviewauftrag am reviewed Subject (unverändert 23 Evidence-Bindungen) als JSON auf stdout. Details zum Schema-Preflight stehen im
[Review-Handoff](reviews/README.md).
