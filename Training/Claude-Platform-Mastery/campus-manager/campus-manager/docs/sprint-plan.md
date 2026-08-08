# Sprint Plan — 6 Months (12 sprints × 2 weeks)

Assumes a solo student, part-time (~10-15 hrs/week), learning as they go —
so velocity is intentionally light and includes buffer for review/rework.

| Sprint | Weeks | Focus | Backlog items | Deliverable |
|---|---|---|---|---|
| 0 | 1-2 | Setup | E1-1 | Repo scaffolded, Claude Project + CLAUDE.md configured, docs in knowledge base |
| 1 | 3-4 | Auth | E1-2, E1-3, E1-4 | Signup/login API working, tested |
| 2 | 5-6 | Tasks API | E2-1, E2-2, E2-3 | Core task CRUD (create/list/toggle) with unit tests |
| 3 | 7-8 | Tasks API (cont.) | E2-4, E2-5, E7-1 | Task edit/delete done, CI pipeline running tests |
| 4 | 9-10 | Groups API | E3-1, E3-2 | Group creation + invite working, tested |
| 5 | 11-12 | Groups API (cont.) | E3-3, E3-4 | Shared group tasks working, tested |
| 6 | 13-14 | Web client I | E5-1, E5-2 (start) | Login/signup screens + basic task list on web |
| 7 | 15-16 | Web client II | E5-2 (finish), E5-3 | Full task CRUD + group UI on web |
| 8 | 17-18 | Reminders + review pass | E4-1, code review cleanup on backend + web | In-app reminder badge; backlog of bugs from review closed |
| 9 | 19-20 | Mobile client I | E6-1, E6-2 (start) | Login/signup + task list on mobile (Expo) |
| 10 | 21-22 | Mobile client II | E6-2 (finish), E6-3 | Full task CRUD + group UI on mobile |
| 11 | 23-24 | Deployment | E7-2, E7-3, E7-4 | Backend + web live; mobile build shared with a tester |

## Sprint ritual (repeat every 2 weeks)
1. **Sprint planning** (30 min): pull next items from backlog into `sprint-tasks.md`.
2. **Daily-ish check-in** (5 min, self): what did I finish, what's blocked.
3. **Code review pass**: run the checklist in `architecture.md` §8 against the sprint's PRs.
4. **Sprint demo**: manually click through the new feature end-to-end.
5. **Retro** (10 min): one thing that went well, one thing to change next sprint.

## Notes
- If a sprint's items slip, don't add new scope — carry them to the next sprint
  and re-plan. This is the single most common real-world lesson to learn here.
- Sprint 8 is intentionally lighter on new features and heavier on review/bugfixing —
  treat this as a mandatory "pay down technical debt" sprint, not optional.
