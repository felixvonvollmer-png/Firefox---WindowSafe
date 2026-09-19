# WindowSafe – autorisierte Vorbereitung der Reviewer-Umgebung

ENVIRONMENT_PREPARATION_ID: WS-REVENV-20260918-01
STATUS: AUTHORIZED_PREPARATION__NOT_YET_QUALIFIED_BY_INDEPENDENT_REVIEWER
EXECUTION_AUTHORIZATION_ID: WS-EA-20260918-01
SOURCE_DRAFT: return/WindowSafe_Reviewer_Environment_WS-REVENV-20260918-01_DRAFT.md
SOURCE_FINDING: WS-PFR-20260918-01-F02 / BLOCKING / OPEN

## 1. Was freigegeben ist

Die Nutzerfreigabe „frei“ nach Vorlage des begrenzten Folgeumfangs autorisiert den
Coding-Agenten, einen tatsächlich verwendbaren, reproduzierbaren Reviewer-
Ausführungskontext vorzubereiten und seine eigenen Umgebungsprüfungen zu belegen.
Sie startet keinen unabhängigen Review und schließt F02 nicht. Dieser neue Record
ändert nicht den erhaltenen Entwurf oder den damaligen BLOCKED-Rücklauf.

Die bestehende autorisierte Codex-Umgebung ist der Ausgangspunkt. Ihre Fähigkeiten
werden tatsächlich geprüft; ein Modellname oder GitHub-Leseconnector genügt nicht.
Der spätere Reviewer muss einen frischen/hinreichend isolierten, nicht
implementierenden Kontext mit eigener Ausführungsmöglichkeit benutzen. Kein neuer
Provider, keine kostenpflichtige Runtime, keine Credentials oder Adminrechte.

## 2. Bereitzustellender Kontext

Benötigt werden echte CPython 3.14.4, Git und eine isolierte vollständige Git-Lesekopie
mit dem alten Bootstrap, dem aktuellen Head 9b6dd621deec1193bfdfbdfa730e8f9349c73fd6,
den Transfer-/Korrekturcommits und dem später tatsächlich entstandenen Kandidaten.
Alte Verträge und alle für Resultatkonsum/History benötigten Trees/Blobs bleiben
verfügbar. Kein loses Verzeichnis mit kopierten Dateien als Ersatz für Gitobjekte.

Bevorzugt die bereits verfügbare gepinnte Runtime verwenden. Fehlt sie, darf sie
nur innerhalb der bestehenden autorisierten isolierten Entwicklungsumgebung aus
belegbarer offizieller Herkunft lokal bereitgestellt werden, ohne System-/Admin-
Eingriff, neue Dienste oder Kostenbindung. Herkunft, tatsächliche Version und
Umgebungsstand dokumentieren. Kein Pin-Monkeypatch und keine Validatoränderung,
um eine andere Runtime als die geforderte auszugeben.

Ein frischer read-only Clone der öffentlichen Quelle ist hier die gebundene
Transportmethode. Benötigt eine Umgebung stattdessen einen anderen Objekttransport,
wird dessen konkrete Herkunft/Integrität zuerst separat vorgelegt und gebunden;
keine pauschale Freigabe manueller Git-Objektrekonstruktion oder fingierter Clones.
Runtime-/Objektzugriff kann nicht hergestellt werden: sichtbarer Umgebungsblocker,
kein behauptetes REVIEW_READY_ENVIRONMENT. Mögliche andere bereits autorisierte
Umgebungen dürfen benannt, aber nicht als ungeprüft verfügbar dargestellt werden.

## 3. Zwei getrennte Nachweise

**Coding-Agent:** Protokolliert tatsächliches Betriebssystem, ausführbare Python-
Datei und Version, Gitversion, Herkunft der Lesekopie, Commit-/Tree-Identitäten,
benutzte Originalkommandos, Exitcodes und Logs. Seine Checks sind
LOCAL_AGENT_REPORTED beziehungsweise selbst gelesene CI-Evidence, keine
unabhängige Reviewer-Ausführung. Nur notwendige synthetische Offline-Tests; keine
Firefox-, Profil-, Restart- oder Produkt-Performanceprobe.

**Späterer unabhängiger Reviewer:** Prüft Runtime und Gitobjekte selbst, lädt den
vollständigen kanonischen Vertrag am neuen Candidate-SHA und führt die dortigen
Originalkommandos request und schema-preflight vor seinem fachlichen Review aus.
Nach dem eigenen Review validiert er sein vollständiges Resultat mit dem passenden
kanonischen validate-result. Scratch-Ausgaben/Fixtures liegen getrennt von den
unveränderten Subjectbytes; Remote und Branch bleiben read-only. Keine CI als
lokale eigene Ausführung und keine Implementiererlogs als Reviewerprovenienz.

Ein fehlgeschlagener verpflichtender Preflight führt zum Halt vor dem fachlichen
Review. F02 bleibt offen, bis der neue unabhängige Ablauf tatsächlich belegt ist.
Die genehmigte Umgebungsvorbereitung allein ist ausdrücklich keine Closure.

## 4. Ende der Vorbereitung

Der Coding-Agent liefert konkrete Wiederholungsbefehle, die tatsächliche Runtime-/
Gitkonfiguration und seinen Umgebungsnachweis zusammen mit dem neuen ungemergten
Candidate-SHA, dem Vertragslocator und der Evidence. Eine künftige Review-ID, ein
neues Reviewresultat oder eine unabhängige Identität werden nicht erfunden.
Die spätere unabhängige Ausführung erhält ihren eigenen exakt gebundenen Auftrag.
