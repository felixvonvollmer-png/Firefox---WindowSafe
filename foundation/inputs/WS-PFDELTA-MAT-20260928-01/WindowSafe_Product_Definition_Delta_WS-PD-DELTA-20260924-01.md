# WindowSafe – Product Definition Delta

```text
DOCUMENT_TYPE: PRODUCT_DEFINITION_DELTA_SUBJECT
PRODUCT_DEFINITION_DELTA_ID: WS-PD-DELTA-20260924-01
PROJECT: WindowSafe
DATE: 2026-09-24
STATUS: USER_REVIEW_REQUIRED
BASE_PRODUCT_DEFINITION_ID: WS-PD-20260917-01
BASE_PRODUCT_DEFINITION_REVISION: 1
BASE_PRODUCT_DEFINITION_SHA256: fff235b7591f483b9b31c945911a6b5950d29fac931b9136438ae5586c756900
BASE_PRODUCT_APPROVAL_ID: WS-PD-APPROVAL-20260917-01
BASE_PRODUCT_APPROVAL_SHA256: a655d1fb0a594997e1f6da00c7e8a36bb6c5807ac844ce9fbf04ccb7d1afd4a5
SOURCE_ORIGIN: Explicit material user decision in the WindowSafe project chat on 2026-09-24
V6_MODE: MATERIAL_PRODUCT_TRUTH_DELTA__APPEND_ONLY
PROPORTIONALITY_PASS: COMPLETE
OPEN_MATERIAL_USER_DECISIONS: NONE
IMPLEMENTATION_AUTHORIZED: NO
REPOSITORY_MUTATION_AUTHORIZED: NO
```

## 1. Zweck und Verbindlichkeit

Dieser Subject ändert ausschließlich die Produktgrenze für öffentlich nicht zuverlässig
unterscheidbare Sonderfenster, insbesondere native WebApp-/Taskbar-Tab-Fenster, die Firefox
156 über die öffentliche WebExtension-API als gewöhnliche `normal`-Fenster exponiert.

Die bestehende freigegebene Product Definition `WS-PD-20260917-01` bleibt unverändert
historische Product Truth. Nach ausdrücklicher Approval-Bindung bildet sie zusammen mit diesem
Delta die neue wirksame Product Truth.

Keine andere Produktfähigkeit, Plattformgrenze, Datenschutzgrenze oder Ressourcenanforderung
wird durch diesen Subject geändert.

## 2. Materielle Nutzerentscheidung [WS-UD-08]

Der Nutzer hat ausdrücklich freigegeben:

> WindowSafe V1 unterscheidet über die öffentliche Firefox-WebExtension-API nicht zuverlässig
> zwischen normalen Fenstern und bestimmten als `normal` exponierten Sonderfenstern wie nativen
> WebApp-/Taskbar-Tab-Fenstern. Solche öffentlich nicht unterscheidbaren Fenster dürfen hinsichtlich
> ihrer erfassbaren Tabs und Sitzungsdaten gesichert werden. Bei einer Wiederherstellung wird jedoch
> ausschließlich ein gewöhnliches Firefox-Fenster bzw. gewöhnliche Tabs wiederhergestellt.
> Native WebApp-/Taskbar-Identität, App-Shell, Pinning, OS-Integration oder andere
> Sonderfenster-Eigenschaften werden nicht als erhalten oder wiederhergestellt zugesagt.
> Diese Einschränkung muss für den Nutzer sichtbar dokumentiert werden.

Zusätzlich ausdrücklich bestätigt:

- keine internen Firefox-Tricks als Produktmechanismus;
- keine Behauptung, WebApps zuverlässig erkennen zu können;
- keine Behauptung nativer WebApp-Wiederherstellung.

## 3. Neue Produktregel [WS-P05]

### WS-P05 – Daten-/Tab-Fallback bei öffentlich nicht unterscheidbaren Sonderfenstern

Kann WindowSafe ein Fenster mit der freigegebenen öffentlichen Firefox-WebExtension-API nicht
zuverlässig von einem normalen Fenster unterscheiden, darf es die über diese API regulär
sichtbaren, nichtprivaten Tabs und wiederherstellungsrelevanten Sitzungsdaten nach den sonst
geltenden WindowSafe-Regeln sichern.

Für eine spätere WindowSafe-Wiederherstellung gilt dann ausschließlich der **gewöhnliche
Fenster-/Tab-Pfad**:

- es wird ein gewöhnliches Firefox-Fenster beziehungsweise gewöhnliche Tabs erzeugt;
- die erfassten Tab-Daten bleiben erhalten, soweit sie ohnehin zum V1-Wiederherstellungsumfang gehören;
- native WebApp-/Taskbar-Identität wird nicht rekonstruiert;
- App-Shell, native Pinning-/Taskbar-Semantik, OS-Integration und sonstige nicht öffentlich
  rekonstruierbare Sonderfenster-Eigenschaften werden nicht als erhalten zugesagt;
- die Einschränkung wird für den Nutzer sichtbar und verständlich ausgewiesen.

WindowSafe darf zur Unterscheidung solcher Fälle **keine** nichtöffentlichen Chrome-Attribute,
privilegierten Firefox-Interna oder erratenen Heuristiken aus URL, Titel, Geometrie oder
ähnlichen Merkmalen als verlässliche Produktidentität verwenden.

Wird eine zukünftige Firefox-Version mit einer dokumentierten öffentlichen und ausreichend
belastbaren Unterscheidungsmöglichkeit unterstützt, darf eine native Sonderfensterbehandlung
erst nach neuer versionsgebundener Qualifikation und gegebenenfalls neuem Product-/Foundation-
Delta zugesagt werden.

## 4. Delta zu [WS-RESTORE]

Der bisherige allgemeine Satz

> Nicht zuverlässig abgrenzbare Fälle dürfen nicht stillschweigend als vollständig unterstützt gelten.

bleibt gültig und wird für öffentlich als `normal` exponierte, nicht zuverlässig
unterscheidbare Sonderfenster durch WS-P05 konkretisiert:

- **Datenerhalt:** ja, soweit die Tabs/Daten über die akzeptierte öffentliche API regulär sichtbar sind.
- **Native Sonderfenster-Wiederherstellung:** nein.
- **Fallback:** gewöhnliches Fenster / gewöhnliche Tabs.
- **Nutzerhinweis:** verpflichtend sichtbar.
- **Privilegierte Erkennung oder Rekonstruktion:** nein.

Andere bestehende Sonderfenstergrenzen für Popup, DevTools und Picture-in-Picture werden durch
diesen Delta-Subject nicht pauschal erweitert oder abgeschwächt.

## 5. Delta zu [WS-CAP-04]

Ein Fallback nach WS-P05 ist ein **sichtbares Teilergebnis**. Die Oberfläche darf nicht
„vollständig wiederhergestellt“ oder eine gleichwertige Aussage anzeigen, wenn native
Sonderfenster-Eigenschaften nicht erhalten werden.

## 6. Delta zu [WS-AC-08]

Zusätzlich ist nachzuweisen:

- ein öffentlich nicht unterscheidbares WebApp-/Taskbar-Tab-Fenster kann innerhalb der
  akzeptierten öffentlichen API-Grenze datenerhaltend erfasst werden;
- die WindowSafe-Wiederherstellung verwendet ausschließlich gewöhnliche Fenster/Tabs;
- es wird kein interner Firefox-Discriminator und keine Heuristik als Produktidentität benutzt;
- der Verlust nativer Sonderfenster-Eigenschaften wird sichtbar kommuniziert;
- das Ergebnis wird nicht als native WebApp-Wiederherstellung ausgegeben.

## 7. Delta zu [WS-OL-03]

Die technische Vorabklärung für Sonderfenster ist für öffentlich nicht zuverlässig
unterscheidbare WebApp-/Taskbar-Tab-Fälle nicht mehr auf einen zwingenden
WebApp-Discriminator beschränkt.

Vor betroffener Produktimplementierung muss stattdessen exakt gebunden sein:

1. welche Sonderfenster öffentlich zuverlässig unterscheidbar sind;
2. für welche Fälle WS-P05 gilt;
3. dass die Datenerfassung innerhalb der normalen öffentlichen API-Grenze sicher ist;
4. dass die Wiederherstellung ausschließlich als gewöhnliches Fenster/gewöhnliche Tabs erfolgt;
5. wie die sichtbare Einschränkung dargestellt und getestet wird.

Ungeklärte Fälle außerhalb dieser gebundenen Grenze bleiben weiterhin blockierend.

## 8. Unverändert

Unverändert bleiben insbesondere:

- Firefox Desktop V1, Windows + Ubuntu und die gebundene Referenz-/Mindestversion;
- keine automatische Recovery beim Browserstart;
- Firefox Session Restore als autoritative Quelle für bereits nativ wiederhergestellte Fenster;
- Private-Fenster-Ausschluss;
- Container-/Identitäts-/Recovery-Sicherheitsregeln;
- Gruppen-, Split-, Reader-, pinned-, muted- und discarded-Grenzen;
- Backup-, Import- und Datenschutzregeln;
- Ressourcen-/Qualitätsziele;
- keine Cloud, kein Server, keine Telemetrie;
- kein Chrome/Chromium-Scope;
- keine neuen Berechtigungen allein für die WebApp-Abgrenzung;
- alle bisherigen Product-/Foundation-/Epic-/F01-/Review-Evidenceoriginale.

## 9. Approval-Gate

Dieser Subject ist **noch nicht APPROVED**.

V6-konform ist der nächste Schritt eine separate ausdrückliche Nutzerfreigabe, gebunden an
die exakten Bytes und SHA-256 dieses Subjects. Erst danach darf
`TECHNICAL_FOUNDATION_DELTA_PREPARATION` verbindlich fortgesetzt werden.

Kein Coding-Agent, keine Repositorymaterialisierung, keine F01-Restqualifikation und kein
Epic-Rebinding werden durch diesen Subject autorisiert.
