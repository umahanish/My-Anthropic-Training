# Requirements — Campus Task & Study Group Manager

## 1. Purpose
A cross-platform (Web + Mobile) app that helps students track assignments/tasks
and coordinate study groups. Built as a 6-month learning project covering the
full SDLC: design → artifacts → incremental build → testing → review → deploy.

## 2. Target users
- **Student (primary)**: creates tasks, joins/creates study groups, gets reminders.
- **Group organizer**: same as student, plus can manage group membership.

## 3. MVP scope (must-have)
1. User can sign up / log in (email + password).
2. User can create, view, edit, delete personal tasks (title, due date, subject, status).
3. User can mark a task complete/incomplete.
4. User can create a study group and invite others by email/username.
5. Group members can see a shared list of group tasks/events.
6. User gets a reminder (in-app notification) for tasks due within 24 hours.

## 4. Stretch scope (nice-to-have, only after MVP is stable)
7. Push notifications on mobile.
8. File/note sharing inside a study group.
9. Calendar view (week/month) of tasks.
10. Basic analytics: tasks completed per week.

## 5. Non-functional requirements
- Web and mobile clients share a single REST API and data model.
- API response time < 500ms for CRUD operations under normal load.
- Passwords stored hashed (bcrypt or equivalent), never plaintext.
- All new backend code ships with unit tests (target: >80% coverage on business logic).
- Every PR is reviewed (self-review checklist minimum) before merge.

## 6. Out of scope for this project
- Payment/billing.
- Real-time chat (use simple polling or leave as a stretch item, not MVP).
- Multi-language i18n.

## 7. Success criteria
- MVP deployed and usable on web (browser) and mobile (installable/testable build)
  by end of Month 6.
- Backend test suite passes in CI before every deploy.
- Backlog, architecture, and sprint history are all traceable in the Claude
  Project knowledge base.
