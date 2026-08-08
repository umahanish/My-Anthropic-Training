# Campus Task & Study Group Manager

A 6-month learning project for practicing the full SDLC: design → artifacts →
small incremental builds → unit testing → code review → deploy (web + mobile).

## What's in this repo

```
docs/                  Planning docs — put these in your Claude Project knowledge base
  requirements.md
  architecture.md
  product-backlog.md
  sprint-plan.md
  estimation.md
CLAUDE.md              Context file Claude Code reads automatically
backend/                Node.js + Express API (working, tested — Sprint 2 scope)
web/                    React web client (starter — Sprint 6-7 scope)
mobile/                 React Native (Expo) client (starter — Sprint 9-10 scope)
```

## How to set this up

### 1. Claude Project (planning)
1. Create a new Project at claude.ai/projects, e.g. "Campus Manager".
2. Upload everything in `docs/` (and this README) to its knowledge base.
3. Add custom instructions like: *"This project is a 6-month solo learning
   build. Always check requirements.md and architecture.md before proposing
   changes. Track new decisions by updating the relevant doc."*
4. Use this Project for all planning conversations: sprint planning, backlog
   grooming, re-estimating, writing new user stories.

### 2. Claude Code (building)
1. Clone/open this repo locally.
2. `CLAUDE.md` is already in the root — Claude Code will read it automatically
   for context (tech stack, conventions, current docs).
3. Ask Claude Code to implement one backlog item at a time (e.g. "implement
   E1-2 signup endpoint, following the conventions in CLAUDE.md, with tests").
4. Ask it to review your diffs against the checklist in
   `docs/architecture.md` §8 before you merge.

### 3. Run the backend (already working)
```bash
cd backend
npm install
npm test        # 16 tests should pass
npm run dev      # starts API on http://localhost:3001
```

### 4. Run the web client
```bash
cd web
npm install
npm run dev      # starts on http://localhost:5173, proxies /api to :3001
```

### 5. Run the mobile client
```bash
cd mobile
npm install
npx expo start    # scan the QR code with Expo Go on your phone
```
Note: on a physical device, edit `BASE_URL` in `mobile/src/api/tasks.js` to
your machine's LAN IP instead of `localhost`.

## Current state
- ✅ Backend: task CRUD (E2-1 to E2-5) implemented and fully tested (16 tests).
- ✅ Backend: signup (E1-2) implemented and tested (11 tests) — `POST
  /api/auth/signup` creates an account with a bcrypt-hashed password and
  rejects duplicate emails.
- ⬜ Auth (E1-3, E1-4): login + JWT-protected routes not yet implemented —
  clients still use a hardcoded `x-user-id` stub. This is the natural next
  backlog item.
- ⬜ Groups (Epic 3), reminders (Epic 4): not yet started.
- 🟡 Web/mobile clients: task list UI implemented against the stub user;
  wire up to real auth once login (E1-3) exists.

## Suggested first move
Open the Claude Project, review `docs/sprint-plan.md` Sprint 1, then switch
to Claude Code and ask it to implement E1-3/E1-4 (login/JWT middleware) with
tests, following `CLAUDE.md`.
