# Architecture — Campus Task & Study Group Manager

## 1. High-level shape

```
            ┌─────────────┐        ┌──────────────┐
            │   Web App   │        │  Mobile App  │
            │  (React)    │        │(React Native)│
            └──────┬──────┘        └──────┬───────┘
                   │  HTTPS / JSON REST    │
                   └───────────┬───────────┘
                               ▼
                     ┌───────────────────┐
                     │   Backend API     │
                     │ Node.js + Express │
                     └────────┬──────────┘
                              ▼
                     ┌───────────────────┐
                     │    Database       │
                     │ SQLite (dev) /    │
                     │ Postgres (prod)   │
                     └───────────────────┘
```

One backend, one data model, two thin clients. This is the single most
important decision: **do not duplicate business logic in the web and mobile
apps** — both call the same API.

## 2. Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend | Node.js + Express | Matches JS on frontend, huge ecosystem, easy to test |
| Auth | JWT (access token) | Stateless, works identically for web + mobile |
| DB (dev) | SQLite | Zero setup, file-based, fast iteration |
| DB (prod) | PostgreSQL | Free tier on Render/Railway/Supabase |
| Web | React + Vite | Fast dev server, simple mental model |
| Mobile | React Native (Expo) | One codebase, easy device testing via Expo Go |
| Testing | Jest + Supertest (backend), Jest + React Testing Library (frontend) | Standard, well documented |
| CI | GitHub Actions | Free, runs tests on every push/PR |
| Hosting | Backend: Render/Railway. Web: Vercel/Netlify. Mobile: Expo/TestFlight/Play internal track |

## 3. Data model (MVP)

**User**
- id, name, email, password_hash, created_at

**Task**
- id, user_id (owner), group_id (nullable — null = personal task), title,
  subject, due_date, status (`todo` / `done`), created_at

**Group**
- id, name, created_by, created_at

**GroupMember**
- id, group_id, user_id, role (`owner` / `member`)

## 4. API surface (MVP)

```
POST   /api/auth/signup
POST   /api/auth/login
GET    /api/tasks                 (personal + group tasks for current user)
POST   /api/tasks
PATCH  /api/tasks/:id
DELETE /api/tasks/:id
POST   /api/groups
POST   /api/groups/:id/invite
GET    /api/groups/:id/tasks
```

## 5. Folder structure (monorepo)

```
campus-manager/
  backend/     -> Express API + tests
  web/         -> React web client
  mobile/      -> React Native client
  docs/        -> requirements, architecture, backlog, sprint plan, estimation
  CLAUDE.md    -> context file for Claude Code
```

## 6. Key architecture decisions & rationale
- **Monorepo** over separate repos: easier for a solo student to keep API
  contract and clients in sync; simplify to separate repos only if the team grows.
- **JWT over sessions**: mobile apps don't handle cookies well; a bearer token
  works identically across web and mobile.
- **SQLite → Postgres migration path**: use an ORM (Prisma or Sequelize) from
  day one so switching databases later is a config change, not a rewrite.
- **No GraphQL for MVP**: REST is simpler to teach, test, and reason about for
  a first full-stack project. Revisit only if over-fetching becomes a real pain.

## 7. Testing strategy
- Unit tests: pure functions and business logic (e.g., "is task overdue?").
- Integration tests: API endpoints via Supertest, hitting a test DB.
- Manual/exploratory testing: web and mobile UI flows before each sprint demo.
- CI runs the full backend test suite on every push; PRs cannot merge if tests fail.

## 8. Code review checklist (used every PR)
- [ ] Does the code do what the ticket describes, nothing more?
- [ ] Are there unit tests for new logic, and do they pass?
- [ ] Any obvious edge cases missed (empty input, unauthorized access, etc.)?
- [ ] Naming and structure consistent with the rest of the codebase?
- [ ] No secrets/credentials committed?
