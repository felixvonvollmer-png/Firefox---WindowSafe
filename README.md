# WindowSafe

WindowSafe soll lokale Firefox-Fenster und Sitzungen sichern und nach einer
Nutzeraktion wiederherstellen. Dieses Repository enthält derzeit ausschließlich
die **Project Foundation**, keine installierbare Erweiterung oder Produktfunktion.

Aktuell: Harness-Korrektur **WS-HC-20260917-01** auf ungemergtem Arbeitsbranch,
Ziel `PROJECT_FOUNDATION_READY_FOR_REVIEW`. Der historische Foundation-PASS gilt
nur für den Bootstrap-SHA; der neue Korrekturstand braucht einen unabhängigen
Delta-Review. Kein Merge oder Auto-Merge in diesem Auftrag.

- [Kontext und unveränderte Product Truth](foundation/context.md)
- [Architektur, Entscheidungen und offene Vorab-Gates](foundation/architecture.md)
- [Engineering, Git, Risiko und Entwicklungsbefehle](foundation/engineering.md)
- [Kanonischer Reviewvertrag und Reviewer-Handoff](reviews/README.md)
- [Korrektur-Subject](foundation/subject.json) und [Evidence](foundation/evidence/harness-correction.md)
- [Initiale Epic-Karte und Preparation-Locators](epics/README.md)

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
`python3 tools/foundation.py request --sha HEAD` den exakt gebundenen
Reviewauftrag als JSON auf stdout. Details zum Schema-Preflight stehen im
[Review-Handoff](reviews/README.md).
