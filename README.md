# KnowBall

**The AI assistant for basketball coaches.**

KnowBall helps a basketball coach plan practices, prepare for opponents and teach plays, while the coach stays in charge of every decision. It answers in Hebrew or English, follows the coach's own philosophy, and only gives an opinion when asked for one.

> Status: prototype. The interface is currently in Hebrew; a full English version is planned.

---

## What it does

| Area | What the coach gets |
|---|---|
| **Practice plan** | A full practice built from the drill library, with timings, coaching points and a source for every drill. |
| **Weekly planning** | A week of practices, games, rest and S&C days. The coach's fixed days always win. Planned load is compared with recent weeks. |
| **Opponent scouting** | Upload short clips of the opponent. Each clip is watched frame by frame, matched to a play in the library (or given its common coaching name), and drawn as an X&O diagram. The report feeds the game plan, a prep week and scout-team cards. |
| **Game plan** | A plan built from the scout report and the coach's notes. |
| **X&O board** | Draw plays from scratch or edit any diagram: add players and defenders, cuts, dribbles, passes, screens, handoffs and shots, step by step, with undo. Every diagram can be played as an animation. |
| **Drill & play library** | About 270 drills and plays (PnR coverages, Pistol, Drag, Delay, shooter actions, ghost screens, zone defenses and offenses, presses and more). Each one has a source link, a diagram and an animation. |
| **Drill bank** | The coach's own saved drills, with a playbook export for players (animations plus an optional quiz). |
| **Roster** | Players, positions, availability and a 4-week development plan for each player. |
| **Practice journal** | Minutes, RPE, attendance and reflections. Training load is calculated from what the coach enters. |
| **Ask the assistant** | Questions about basketball, always with a real source or a YouTube search link. A separate mode recommends load and rest from the coach's own data. It never prescribes strength, conditioning or nutrition work; that stays with the S&C coach. |

## Principles

- **Answer what was asked.** The assistant does the request and does not add its own ideas unless asked "what do you think?".
- **Real sources only.** Every drill comes from the library with a checked source. The assistant cannot invent a link: unknown references are removed and shown as "no source".
- **The coach decides.** Days, drills and plans the coach sets are never overridden.
- **Privacy.** Each coach's bank, roster, journal and scouts are stored separately. Only the drill library is shared.

## How it runs

KnowBall is a single HTML file (`KnowBall.html`) that runs as a Claude artifact. It uses Claude for the AI features and for storing data, so **opening the file directly in a browser will not work**. Use the shared artifact link instead.

- The drill library and each coach's data live in the artifact's database, not in this file.
- The zone-defense pack is included in the file and is added to the library and to the coach's bank the first time the app opens.
- The player playbook export is a standalone HTML file that works anywhere.

## Sources

Library items link to their original pages, mainly Coach's Clipboard, FastModel Sports, Breakthrough Basketball, Coaching Toolbox, The Basketball Action Dictionary, Hoop Student and others. Where a diagram's exact positions were drawn from the source's rules rather than copied, the item says so in a note next to the source.

## Roadmap

- Full English interface (language switch, left-to-right layout, English library text)
- Testing with real coaches and real game footage
- Shared staff access (assistant coaches and S&C coach on the same roster)
- Data backup / export

---

## בעברית

**KnowBall** הוא עוזר AI למאמני כדורסל: מערכי אימון, תכנון שבועי, סקאוט יריב מקטעי וידאו, תוכנית משחק, לוח X&O עם אנימציות, ספרייה של כ-270 תרגילים ומהלכים עם מקורות, בנק תרגילים, סגל ויומן אימונים.

העוזר עונה רק על מה שביקשו ממנו, משתמש רק במקורות אמיתיים, ולא נותן המלצות כושר או תזונה. ההחלטות תמיד של המאמן.

המערכת רצה כ-artifact של Claude דרך הקישור המשותף. פתיחה ישירה של הקובץ בדפדפן לא תעבוד.

## Running as a website (Firebase)

The live site is `index.html`, served by GitHub Pages. It uses Firebase for sign-in (email and password) and Firestore for each coach's data.

- `src/app.html` – the app source (also runs as a Claude artifact).
- `build/` – the Firebase layer (login screen, data adapter). Run `python3 build/build.py` to rebuild `index.html` after changing the source.
- `library.json` – the shared drill and play library (read-only).
- `firestore.rules` – security rules: every coach can read and write only their own data.
- AI features (practice plans, scout, chat) are not connected on the website yet; that is the next stage (Cloud Functions, so no API key is ever in the browser).
