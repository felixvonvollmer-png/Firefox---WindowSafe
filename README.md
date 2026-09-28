# WindowSafe

WindowSafe soll lokale Firefox-Fenster und Sitzungen sichern und nach einer
Nutzeraktion wiederherstellen. Dieses Repository enthält derzeit ausschließlich
die integrierte **Project Foundation** und die WS-E01 Epic Preparation, keine
installierbare Erweiterung oder Produktfunktion.

Aktuell: **WS-PFDELTA-MAT-20260928-01** unter **WS-EA-20260928-01**:
minimaler Brownfield-Foundation-Delta für WS-P05 und finale V6-Router.
[Neuer Subject](foundation/deltas/WS-PFDELTA-MAT-20260928-01/subject.json) und [Evidence/Review-Handoff](foundation/deltas/WS-PFDELTA-MAT-20260928-01/evidence.md).
Stop: **PROJECT_FOUNDATION_READY_FOR_REVIEW**, unabhängiger Review noch offen.
Historische WS-E01 Preparation bleibt unverändert angenommen; ihre Annahme ersetzt
kein Delta-Rebinding. F01 bleibt auf PR #3 am Head `7d66ca5b025c8f748d7f97b961c496ee450daaa7`
Draft/ungemergt und wird hier nicht fortgesetzt. Kein Merge oder Produktcode.
Externer Project-Context-Sync: **PENDING_AFTER_PROJECT_FOUNDATION_REVIEW_PASS**.

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
