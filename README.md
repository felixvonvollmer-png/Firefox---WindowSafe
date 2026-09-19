# WindowSafe

WindowSafe soll lokale Firefox-Fenster und Sitzungen sichern und nach einer
Nutzeraktion wiederherstellen. Dieses Repository enthält derzeit ausschließlich
die integrierte **Project Foundation** und die WS-E01 Epic Preparation, keine
installierbare Erweiterung oder Produktfunktion.

Aktuell: **WS-E01-INT-20260919-02**, autorisiert durch **WS-EA-20260919-05**.
Der unveränderte unabhängige [Epic Preparation PASS](reviews/results/WS-E01-EPR-20260919-02.json)
bindet den reviewed Subject `644b81f63dcc1990bc894a9c2c9bd8dc24a98c04` und dessen
Foundationbasis `dc9c1c37a264cc80f79ec08bf166ec42cdd73b95`.
Das [WS-E01 Binding](epics/WS-E01/binding.json) ist **READY_FOR_AGENT**;
External Context Sync: NOT_APPLICABLE. Die Annahme öffnet ausschließlich das
Preparation-Gate. Dieser Auftrag endet nach geprüfter Normal-Merge-Integration
von PR #2. WS-E01-F01 benötigt eine spätere ausdrückliche Ausführungsautorisierung;
Produkt-/Browser-/Profilarbeit bleibt in diesem Lauf ausgeschlossen.

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

## F01-Qualifikation

Der ungemergte F01-Lauf liefert Partial-Evidence und ist am finalen Auditgate BLOCKED; Einstieg über
[Qualifikationsbericht](features/WS-E01-F01/evidence/qualification-followup.md) und
[Fortsetzungspaket](qualification/ws-e01-f01/README.md). Kein Produktstart, F02 oder Merge.
