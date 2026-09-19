# WindowSafe – Reviewer-Ausführungskontext nach WS-PFR-20260918-01-F02

Status: DRAFT / Umgebungs-Rebind vor neuem unabhängigen Review erforderlich.
Kein neuer Reviewauftrag für den alten fehlerhaften Head, kein Agentenstart.

## Zweck

Der eingegangene Rücklauf nennt fehlende eigene kanonische Originalausführungen
von request, schema-preflight und validate-result. Dies wird nicht rückwirkend
behoben, indem der vorbereitende Projekt-LLM oder der Implementierer die Befehle
später selbst ausführt. Das Original bleibt BLOCKED und unverändert.

Für den neuen korrigierten Head wird ein frischer oder hinreichend isolierter,
nicht implementierender Reviewer an einen tatsächlich geeigneten Ausführungskontext
gebunden. Ein GitHub-Leseconnector allein beweist keinen lokalen Git-Objektzugriff.
Modellname oder höhere Reasoningstufe ersetzt keine dieser Fähigkeiten.

## Voraussetzungen vor Beginn des fachlichen Reviews

* Gepinnte CPython-Runtime 3.14.4 real vorhanden; kein Umbenennen einer anderen Version,
  kein monkeypatch des Pins und keine modifizierte Validator-Kopie.
* Isolierte Git-Lesekopie mit den exakten alten und neuen Commit-, Tree- und Blobobjekten,
  einschließlich historischer Verträge und Resultate. Subject/Evidence vollständig
  vorhanden; die Git-Objektidentitäten werden tatsächlich verifiziert.
* Reviewautorität und unabhängiger Kontext gebunden; kein gemeinsamer schreibender
  Implementierungslauf. Repository und Remote read-only. Eigene Scratch-Ausgaben
  und synthetische Testfixtures sind getrennt von den kanonischen Subjectbytes.
* Keine neuen Provider, bezahlten Runtime-Dienste, privilegierten Secrets oder
  Produkt-/Browserprofile. Erforderliche Ausführungsrechte separat binden.

Ein sauberer Clone in einer bereits autorisierten ausführbaren Umgebung ist eine
mögliche Transportmethode. Eine andere Methode benötigt eine explizite Bindung und
darf nicht als bereits ausgeführter Original-Clone dargestellt werden. Der aktuelle
Auftrag erteilt keine pauschale Freigabe manueller Rekonstruktion als Ersatz.

## Verifikationsfolge für den später exakt gebundenen neuen Head

Zuerst Runtime-/Git-Objekt- und Vertragszugriff prüfen. Dann den Request und den
vollständigen Vertrag direkt aus dem unveränderten Kandidaten erzeugen und den
kanonischen schema-preflight tatsächlich ausführen. Bei Fehlschlag: vor dem
fachlichen Review stoppen und Umgebungsblockade zurückgeben.

Nach erfolgreichem Preflight den begrenzten gesamten Korrekturdelta prüfen,
inklusive der beiden MAJORs, Writerregressionen, Versions-/Historienkompatibilität
und tatsächlicher neuer CI-/Test-Evidence. Zuletzt das vom unabhängigen Reviewer
verfasste neue Resultat mit dem passenden kanonischen validate-result gegen seinen
exakten Subject prüfen. Dateien und Reviewerprovenienz bleiben unverändert; keine
Kommandos simulieren, keine CI als lokale eigene Ausführung umdeuten.

Die konkrete neue Review-ID, der neue Candidate-SHA, Vertragsblob, vollständige
Evidence-Liste, Reviewerumgebung und Resultatlocator werden erst aus dem dann
wirklich vorhandenen Korrekturstand gebunden. Es wird jetzt kein SHA erfunden.

## Disposition des alten Rücklaufs

Der alte Text dokumentiert fachliche Feststellungen trotz nicht abgeschlossenen
mechanischen Reviewgates. Sie bleiben als solche erhalten und können eng gerichtete
Korrekturarbeit begründen, aber keine vollständige unabhängige Annahme ersetzen.
F02 bleibt bis zum neu belegten unabhängigen Ablauf offen; bloßes Vorbereiten dieser
Checkliste oder ein Implementierer-Umgebungstest schließt den Befund nicht.
