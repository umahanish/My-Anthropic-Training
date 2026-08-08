# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project docs (source of truth — read these first for "why")
- `docs/requirements.md` — scope, MVP vs stretch
- `docs/architecture.md` — tech stack, data model, API surface, review checklist
- `docs/product-backlog.md` — epics/stories/acceptance criteria
- `docs/sprint-plan.md` — current sprint, what's in scope right now
- `docs/estimation.md` — effort tracking

Keep these in sync with the companion Claude Project knowledge base.

## Current implementation state
`docs/architecture.md` describes the *target* architecture — treat it as the
destination, not the current state:
- Backend: task CRUD only (E2-1..E2-5), fully tested (16 tests). The data
  store is an **in-memory array** (`backend/src/models/task.js`), not SQLite —
  that migration lands with E1-1 tooling work.
- Auth: signup only (E1-2) — `POST /api/auth/signup` (`backend/src/routes/auth.js`,
  `backend/src/models/user.js`) creates a user with a bcrypt-hashed password
  and rejects duplicate emails, but there's no login and no token yet. Task
  routes still require an `x-user-id` header instead of a JWT (`requireUser`
  in `backend/src/routes/tasks.js`), and both web and mobile clients hardcode
  this stub in their `api/tasks.js`. When wiring login/JWT (E1-3, E1-4),
  update the route middleware and both clients' `headers()` helpers together.
- Groups (Epic 3) and reminders (Epic 4): not started. `isDueSoon()` in
  `task.js` is the only reminder-related logic so far and isn't called by any
  route yet.
- Web/mobile: task-list UI only, calling the same four endpoints below.
- No lint config and no CI workflow exist yet, despite `docs/architecture.md`
  naming GitHub Actions as the target — don't assume either is wired up.

## Stack
- Backend: Node.js + Express + Jest/Supertest, SQLite in dev (planned — see above).
- Web: React + Vite.
- Mobile: React Native (Expo).
- All three share the API contract in `docs/architecture.md` §4 — never
  duplicate business logic in a client; clients call the API.

## Commands
```
# Backend
cd backend && npm install
npm test                          # run all backend tests (jest --runInBand)
npx jest tasks.api.test.js        # run a single test file
npx jest -t "cannot edit"         # run tests matching a name pattern
npm run dev                       # start API on http://localhost:3001

# Web
cd web && npm install
npm run dev                       # http://localhost:5173, proxies /api to :3001
npm run build

# Mobile
cd mobile && npm install
npx expo start                    # scan QR with Expo Go
# on a physical device, edit BASE_URL in mobile/src/api/tasks.js to your LAN IP
```

## Architecture

### Backend request flow
`server.js` → `app.js` (`createApp()`: mounts `express.json()`, `/api/health`,
the `/api/tasks` router, then a catch-all error handler) → `routes/tasks.js`
(`requireUser` middleware reads `x-user-id`, then CRUD handlers) →
`models/task.js` (in-memory array + ownership checks).

- `createApp()` is called fresh per test file, and the model exposes
  `taskModel.reset()` to isolate tests (see `beforeEach` in
  `backend/tests/*.test.js`) — give any new model the same `reset()` pattern.
- Ownership is enforced in the model layer: `update`/`remove` check
  `task.userId === userId` and return `null`/`false` rather than throwing;
  routes turn that into a `404` (not `403`) so a user can't tell whether a
  task exists that they don't own. Follow this pattern for new resources
  (groups, etc.) rather than introducing 403s.

### Client structure (web + mobile)
`web/src/api/tasks.js` and `mobile/src/api/tasks.js` are near-identical thin
fetch wrappers (same function signatures, same `x-user-id` stub) — the only
difference is `BASE_URL`: relative `/api/tasks` for web (proxied by Vite) vs.
absolute `http://localhost:3001/api/tasks` for mobile (Expo/RN has no dev
proxy, and `localhost` on a physical device means the device itself). When
the API contract changes, update both files together.

## Working conventions
1. **One backlog item per change.** Reference the backlog ID (e.g. `E2-1`)
   in commit messages and PR descriptions.
2. **Tests are not optional.** Any new business logic in `backend/src` needs
   a corresponding test in `backend/tests`. Run `npm test` before considering
   a task done.
3. **Small commits.** Prefer several small, reviewable commits over one large one.
4. **Code review pass before merge**, using the checklist in
   `docs/architecture.md` §8. When asked to "review" code, apply that
   checklist explicitly and point out concrete line-level issues.
5. **Don't expand scope.** If a task reveals extra work, add it as a new
   backlog item in `docs/product-backlog.md` rather than doing it inline.
