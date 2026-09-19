# Reviewer-Ausführungskontext WS-REVENV-20260918-01

Vorbereitung gemäß WS-EA-20260918-01 in der bereits autorisierten Codex-Umgebung.
Dies startet keinen unabhängigen Review. Der erhaltene Review bleibt BLOCKED,
F02 bleibt OPEN bis ein späterer unabhängiger Nichtimplementierer beide Pflichtgates
selbst ausführt. Kein Merge oder Produkt-/Browserauftrag.

## Tatsächlich verfügbare Fähigkeiten

Die Originalkonsum-Lesekopie wurde frisch vom öffentlichen GitHub-Repository
geklont: `/tmp/windowsafe-original-consumption-ng46jjy6/repository`.
Isolierte Runtime: `/tmp/windowsafe-original-consumption-ng46jjy6/runtime/bin/python`.
CPython 3.14.4, Basis `/usr/bin/python3.14`, Git 2.53.0, Linux x86_64.
Executable-SHA-256:
`52e0a13e60a981d8c4b6478be2ba5176f69da07948a056bf49cf6f077e30cb41`.
`foundation/evidence/followup-transfer.json` enthält Originalkommandos, Exitcodes,
Runtime und alle 18 Evidencehashes. Keine Installation oder Git-Objektrekonstruktion.
Die lokale Venv nutzt die vorhandene Runtime; sie ist kein portables Runtimearchiv.

Der getestete neue Kandidat wird nach Push mit demselben Verfahren in eine neue
Lesekopie vorbereitet. Sein **exakter SHA, tatsächlicher Verzeichnispfad und
preparation.json-Hash** stehen im abschließenden Agent-/PR-Handoff. Das Record
enthält alle ausgeführten argv/cwd/Umgebungsparameter, Ausgaben und Exitcodes,
Commit/Tree, `git fsck`, Runtime sowie die explizit offene F02-Grenze.
Keine selbstreferenzielle End-SHA-Behauptung in diesem Dokument.

## Reproduzierbare Vorbereitung am exakten Kandidaten

In dieser bestehenden Umgebung und mit dem **vollständigen END_SHA aus dem Handoff**:

```sh
python3 tools/reviewer_environment.py --sha <END_SHA> --destination /tmp/windowsafe-independent-review-<UNIQUE_RUN_ID>
```

Der Zielpfad muss neu sein. Das Werkzeug verlangt bereits vorhandenes tatsächliches
CPython 3.14.4, klont ausschließlich die autorisierte öffentliche HTTPS-Quelle mit
vollständiger History, checkt detached den genauen SHA aus und sperrt den lokalen
Push-URL. Es erstellt eine Venv ohne pip/Dependencies und führt die unveränderten
Originalkommandos des Kandidaten aus. Kein bestehender Kontext wird überschrieben.
Fehler ergeben ENVIRONMENT_BLOCKED mit erhaltenem Record, keine automatische
Installation oder Provider-/Adminaktion. Dieses Werkzeug nur in der autorisierten
Umgebung ausführen; die Testsuite selbst klont ausschließlich lokale synthetische
Git-Fixtures und kontaktiert kein Netz.

## Verpflichtender späterer unabhängiger Ablauf

Ein frischer oder hinreichend isolierter **Nichtimplementierer** muss die
Vorbereitung übernehmen/verifizieren oder mit neuem Ziel selbst reproduzieren.
Setze `REVIEW_ROOT` auf das tatsächlich vorbereitete neue Verzeichnis und
`SUBJECT_SHA` auf den unveränderlichen Handoff-SHA. Die Platzhalter sind vor
Ausführung zu ersetzen; keine bewegliche Branchreferenz für den Review.

```sh
REVIEW_ROOT=/tmp/windowsafe-independent-review-<UNIQUE_RUN_ID>
SUBJECT_SHA=<END_SHA>
REVIEW_PYTHON="$REVIEW_ROOT/runtime/bin/python"
cd "$REVIEW_ROOT/repository"
"$REVIEW_PYTHON" -c 'import sys,platform; assert platform.python_implementation() == "CPython"; assert sys.version_info[:3] == (3,14,4); print(sys.version)'
git cat-file -e "$SUBJECT_SHA^{commit}"
git cat-file -e 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109^{commit}
git cat-file -e 9b6dd621deec1193bfdfbdfa730e8f9349c73fd6^{commit}
"$REVIEW_PYTHON" tools/foundation.py request --sha "$SUBJECT_SHA" > "$REVIEW_ROOT/independent-request.json"
git show "$SUBJECT_SHA:reviews/review-contract.json" > "$REVIEW_ROOT/independent-contract.json"
"$REVIEW_PYTHON" tools/foundation.py schema-preflight --sha "$SUBJECT_SHA" --schema "$REVIEW_ROOT/independent-contract.json"
"$REVIEW_PYTHON" tools/foundation.py check
"$REVIEW_PYTHON" -m unittest discover -s tests -v
"$REVIEW_PYTHON" tools/foundation.py build --verify-repeat
"$REVIEW_PYTHON" tools/foundation.py history --base 4ba2c473fe4d90c85d94ee2b2f5cc5777d115109
```

Erst nach eigenem erfolgreichen Request/Schema-Preflight fachlich reviewen.
Alle verlangten Evidencebytes aus Git lesen/hashprüfen, genauen Head-CI prüfen,
Originalprovenienz und Unabhängigkeit selbst nachweisen. Gezielter Delta-Scope und
kanonischer Vertrag: [Review-Handoff](../reviews/README.md). Nach eigenem Review
vollständiges echtes V3-Resultat außerhalb des checkouts erzeugen, dann zwingend:

```sh
"$REVIEW_PYTHON" tools/foundation.py validate-result --file "$REVIEW_ROOT/<REVIEW_ID>.json"
```

Eigene argv/Exitcodes/Runtime/Git-/Evidencebindung gehören in die tatsächliche
Reviewerprovenienz. Bei Fehler BLOCKED, keine Gateabschwächung. Ohne separates
Schreibrecht nur Originalpayload zurückgeben; kein direkter Kanalschreibvorgang.
Die Implementierervorbereitung und grüne CI schließen F02 **nicht**. Die Fähigkeiten
sind auf diesem Host nachgewiesen; in einem anderen ChatGPT-/Sandbox-Kontext muss
der Reviewer tatsächliche Fähigkeiten erneut nachweisen. Temporärpfade können
verschwinden: in dem Fall mit dem unveränderten Werkzeug frisch reproduzieren.
