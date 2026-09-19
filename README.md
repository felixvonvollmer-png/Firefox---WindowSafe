# WindowSafe

WindowSafe soll lokale Firefox-Fenster und Sitzungen sichern und nach einer
Nutzeraktion wiederherstellen. Dieses Repository enthält derzeit ausschließlich
die integrierte **Project Foundation** und die WS-E01 Epic Preparation, keine
installierbare Erweiterung oder Produktfunktion.

Aktuell: **WS-E01-MAT-20260919-01**, autorisiert durch WS-EA-20260919-04 ab main
`dc9c1c37a264cc80f79ec08bf166ec42cdd73b95`. Der unveränderte unabhängige
[Foundation-PASS](reviews/results/WS-PFR-20260918-02.json) wurde integriert;
External Context Sync: NOT_APPLICABLE. Die [WS-E01 Preparation](epics/WS-E01/preparation.md)
ist materialisiert: `EPIC_PREPARATION_READY_FOR_REVIEW`, unabhängiger Review PENDING.
Kein Epic ist READY_FOR_AGENT. STOP am getesteten ungemergten Draft-PR;
kein Merge/Auto-Merge, Featurestart oder Browser-/Profiltest in diesem Auftrag.

- [Kontext und unveränderte Product Truth](foundation/context.md)
- [Architektur, Entscheidungen und offene Vorab-Gates](foundation/architecture.md)
- [Engineering, Git, Risiko und Entwicklungsbefehle](foundation/engineering.md)
- [Kanonischer Reviewvertrag und Reviewer-Handoff](reviews/README.md)
- [Korrektur-Subject](foundation/subject.json) und [Evidence](foundation/evidence/followup-correction.md)
- [Vorbereitete Reviewer-Umgebung](foundation/reviewer-environment.md)
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
`python3 tools/foundation.py request --sha HEAD --subject epics/WS-E01/subject.json` den exakt gebundenen
Reviewauftrag als JSON auf stdout. Details zum Schema-Preflight stehen im
[Review-Handoff](reviews/README.md).
