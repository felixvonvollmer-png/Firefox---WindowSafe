# WindowSafe

WindowSafe soll lokale Firefox-Fenster und Sitzungen sichern und nach einer
Nutzeraktion wiederherstellen. Dieses Repository enthält derzeit ausschließlich
die **Project Foundation**, keine installierbare Erweiterung oder Produktfunktion.

Der Bootstrap WS-PFBOOT-20260917-01 endet bei
`PROJECT_FOUNDATION_READY_FOR_REVIEW`. Ein unabhängiger
`PROJECT_FOUNDATION_REVIEW` steht noch aus. Integration in `main` bedeutet weder
Acceptance noch Release.

- [Kontext und unveränderte Product Truth](foundation/context.md)
- [Architektur, Entscheidungen und offene Vorab-Gates](foundation/architecture.md)
- [Engineering, Git, Risiko und Entwicklungsbefehle](foundation/engineering.md)
- [Kanonischer Reviewvertrag und Reviewer-Handoff](reviews/README.md)
- [Foundation-Subject](foundation/subject.json) und [Evidence](foundation/evidence/internal-review.md)
- [Initiale Epic-Karte und Preparation-Locators](epics/README.md)

## Lokal prüfen

Python **3.14.4** und Git genügen; keine Python-Pakete, Browser oder Profile:

```sh
python3 tools/foundation.py check
python3 -m unittest discover -s tests -v
python3 tools/foundation.py build
```

`build` erzeugt ein deterministisches Foundation-Inventar in `build/`; es baut
kein Firefox-Add-on. Nach einem Commit liefert
`python3 tools/foundation.py request --sha HEAD` den exakt gebundenen
Reviewauftrag als JSON auf stdout. Details zum Schema-Preflight stehen im
[Review-Handoff](reviews/README.md).
