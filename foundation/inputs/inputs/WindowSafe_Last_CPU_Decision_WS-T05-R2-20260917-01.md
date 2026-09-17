# WindowSafe – T05-R2 Last-CPU-Vertrag

```text
DOCUMENT_TYPE: MATERIAL_TECHNICAL_DECISION_SUBJECT
DECISION_ID: T05-R2
DECISION_SUBJECT_ID: WS-T05-R2-20260917-01
STATUS: APPROVED_BY_USER_CONTEXT
DATE: 2026-09-17
PROJECT: WindowSafe
PARENT_PREPARATION: WS-TFP-20260917-01
PREVIOUS_UNAPPROVED_PROPOSAL: WS-T05-20260917-01
PREVIOUS_REVIEW_FINDING: WS-TFPR-20260917-01-F01
```

## 1. Zweck

Dieser Vertrag ergänzt die bereits freigegebenen T02-Ressourcen- und Verzögerungsziele um ein reproduzierbares Last-CPU-Kriterium. Er ersetzt weder T02 noch Sicherheits-, Datenverlust- oder Persistenzgrenzen.

Die frühere, nicht freigegebene T05-Fassung mit harten Dauerlastgrenzen von 1 % (R500) und 2 % (R2000) wird **nicht** übernommen. Der Nutzer hat ausdrücklich angemerkt, dass ein zu aggressives Vorabziel unnötige Architekturumbauten provozieren könnte. T05-R2 setzt daher robuste harte Grenzen und getrennte Soft-Optimierungsziele.

## 2. Lastprofil L10

- **R500:** 500 Tabs / 10 Fenster gemäß T02.
- **R2000:** 2.000 Tabs / 20 Fenster gemäß T02.
- **Dauer:** 10 Minuten (600 s).
- **Änderungsrate:** 10 tatsächlich verarbeitete, relevante WindowSafe-Zustandsänderungen pro Sekunde.
- Der definierte Mix umfasst mindestens Navigation auf synthetischen lokalen Testseiten, mute/unmute, pin/unpin, Tab-Reihenfolge sowie Tab-Transfers zwischen Fenstern. Der Mix darf nicht nur triviale No-op-Ereignisse enthalten.
- Die vorhandenen T02-Sicherungsverzögerungen, Datenverlustschutz- und Schreibinvarianten müssen gleichzeitig eingehalten werden.

## 3. Harte Bestehensgrenzen

Bezugsgröße ist **ein CPU-Kern**. Gemessen wird zusätzlicher WindowSafe-bedingter CPU-Verbrauch durch gepaarte Vergleichsläufe der gleichen synthetischen Testlast mit und ohne WindowSafe über den gesamten relevanten Firefox-Prozessbaum.

| Lastprofil | Harte Dauerlastgrenze | Zusätzliche Einzellaufgrenze |
|---|---:|---:|
| R500 | Median der gültigen Messpaare **≤ 10 % eines CPU-Kerns** | kein gültiger Lauf **> 15 %** |
| R2000 | Median der gültigen Messpaare **≤ 20 % eines CPU-Kerns** | kein gültiger Lauf **> 30 %** |

Die Medianregel verhindert, dass ein einzelner kleiner Messausreißer automatisch einen Architekturumbau erzwingt; die Einzellaufgrenze verhindert zugleich, dass stark schwankendes oder sporadisch exzessives Verhalten durch einen guten Median verdeckt wird.

## 4. Soft-Optimierungsziele

| Lastprofil | Soft-Ziel |
|---|---:|
| R500 | möglichst **≤ 5 % eines CPU-Kerns** |
| R2000 | möglichst **≤ 10 % eines CPU-Kerns** |

Das Nichterreichen eines Soft-Ziels **allein**:

```text
IS_NOT_ACCEPTANCE_FAILURE
DOES_NOT_REQUIRE_ARCHITECTURE_REWORK
DOES_NOT_CREATE_A_BLOCKING_FINDING
```

Eine triviale lokale Optimierung darf vorgenommen werden, wenn sie keine Recovery-, Safety-, Latenz- oder Wartbarkeitsgrenze verschlechtert. Ein Redesign nur zur Erreichung des Soft-Ziels ist nicht gefordert.

## 5. Mess- und Bestehensregeln

- Mindestens **5 gültige gepaarte Messläufe je Lastprofil und unterstütztem Betriebssystem** (Windows und Ubuntu gemäß T01).
- A/B-Paar: identische synthetische Last und Testumgebung; A ohne WindowSafe-Lastverarbeitung, B mit WindowSafe.
- Messwerkzeug, Firefox-Build, OS-Build, Hardware, Profilzustand, Hintergrundlast, Warm-up, Messintervall und bekannte Messunsicherheit werden **vor Beginn der betroffenen Produktimplementierung** als Testvertrag gebunden.
- Die Differenz B−A wird als WindowSafe-Zusatzverbrauch berichtet. Nicht sauber zurechenbare native Effekte werden separat ausgewiesen und nicht als null behandelt.
- Ein Lauf ist ungültig, wenn die definierte Last nicht tatsächlich ausgeliefert/verarbeitet wurde oder T02-Sicherungs-/Safety-Regeln durch verlorene beziehungsweise absichtlich verzögerte Änderungen umgangen wurden.
- Die tatsächlichen Last-CPU-Ergebnisse entstehen später und sind spätestens vor Feature-Acceptance nachzuweisen.

## 6. Burstprüfung

Der vorhandene T02-Burst von 300 relevanten Ereignissen über 3 Sekunden bleibt bestehen. Für CPU wird zusätzlich ein festes 10-Sekunden-Fenster einschließlich Nachlauf gemessen:

- R500: **≤ 20 % eines CPU-Kerns im Mittel über dieses 10-Sekunden-Fenster**.
- R2000: **≤ 40 % eines CPU-Kerns im Mittel über dieses 10-Sekunden-Fenster**.

Diese Burstgrenzen sind harte Schutzgrenzen gegen kurzzeitige exzessive Verarbeitung, aber bewusst weniger restriktiv als ein dauerhaftes Lastbudget.

## 7. Unveränderte Grenzen

Unverändert gelten insbesondere:

- Idle-CPU-Ziel aus T02: durchschnittlich höchstens 0,1 % eines CPU-Kerns im ruhigen 10-Minuten-Intervall.
- Keine periodischen Vollscans oder Dauer-Polling im normalen Leerlauf.
- Keine vollständigen unbetroffenen Sitzungs-/Historien-Rewrites wegen einzelner Tabänderungen.
- Keine Verbesserung von CPU-Zahlen durch stilles Weglassen, falsches Zusammenführen oder verspätetes Persistieren von Recovery-Daten.
- Überschreitung einer **harten** T05-R2-Grenze verlangt Optimierung oder eine sichtbare neue materielle Entscheidung; keine heimliche Abschwächung des Tests.

## 8. Autorisierung

Diese Entscheidung definiert Qualitätsgrenzen. Sie autorisiert **keinen Coding-Agentenstart, keine Produktimplementierung, keine GitHub-Mutation, keine Firefox-Profiländerung und keinen Release**. Die korrigierte Technical Foundation Preparation benötigt weiterhin den unabhängigen Rereview.
