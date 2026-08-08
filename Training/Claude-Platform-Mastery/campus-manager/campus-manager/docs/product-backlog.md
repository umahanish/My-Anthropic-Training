# Product Backlog — Campus Task & Study Group Manager

Story points use a simple Fibonacci-ish scale: 1 (trivial), 2, 3, 5, 8 (large — consider splitting).

## Epic 1: Project Setup & Auth
| ID | Story | Acceptance Criteria | Points |
|---|---|---|---|
| E1-1 | As a dev, I can run the backend locally with one command | `npm install && npm run dev` starts API on localhost | 2 |
| E1-2 | As a user, I can sign up with email + password | Account created, password hashed, duplicate email rejected | 3 |
| E1-3 | As a user, I can log in and receive a JWT | Valid creds → 200 + token; invalid → 401 | 3 |
| E1-4 | As a dev, protected routes reject requests without a valid token | 401 returned for missing/invalid token | 2 |

## Epic 2: Personal Tasks (core MVP)
| ID | Story | Acceptance Criteria | Points |
|---|---|---|---|
| E2-1 | As a user, I can create a task with title/subject/due date | Task saved, returned with generated id | 2 |
| E2-2 | As a user, I can view my list of tasks | GET returns only tasks owned by the logged-in user | 2 |
| E2-3 | As a user, I can mark a task complete/incomplete | PATCH toggles status field | 1 |
| E2-4 | As a user, I can edit a task's details | PATCH updates title/date/subject | 2 |
| E2-5 | As a user, I can delete a task | DELETE removes task; 404 if not owner | 2 |

## Epic 3: Study Groups
| ID | Story | Acceptance Criteria | Points |
|---|---|---|---|
| E3-1 | As a user, I can create a study group | Group saved with me as owner | 2 |
| E3-2 | As a group owner, I can invite a member by email | Member added to group, receives access | 3 |
| E3-3 | As a group member, I can see shared group tasks | GET /groups/:id/tasks returns tasks scoped to group | 3 |
| E3-4 | As a group member, I can add a task to the group | Task created with group_id set | 2 |

## Epic 4: Reminders
| ID | Story | Acceptance Criteria | Points |
|---|---|---|---|
| E4-1 | As a user, I see an in-app badge for tasks due within 24h | Frontend computes/display based on due_date | 3 |

## Epic 5: Web Client
| ID | Story | Acceptance Criteria | Points |
|---|---|---|---|
| E5-1 | Login/signup screens | Forms call auth API, store token | 3 |
| E5-2 | Task list + create/edit/delete UI | CRUD reflected instantly in UI | 5 |
| E5-3 | Group view UI | Create group, invite, see group tasks | 5 |

## Epic 6: Mobile Client
| ID | Story | Acceptance Criteria | Points |
|---|---|---|---|
| E6-1 | Login/signup screens (RN) | Same behavior as web, native components | 3 |
| E6-2 | Task list + create/edit/delete UI (RN) | CRUD reflected instantly in UI | 5 |
| E6-3 | Group view UI (RN) | Same as web equivalent | 5 |

## Epic 7: Quality & Deployment
| ID | Story | Acceptance Criteria | Points |
|---|---|---|---|
| E7-1 | CI pipeline runs backend tests on every push | GitHub Actions green/red on PRs | 2 |
| E7-2 | Backend deployed to hosting provider | Public URL responds to health check | 2 |
| E7-3 | Web app deployed | Public URL live | 1 |
| E7-4 | Mobile app buildable/testable (Expo/TestFlight/Play internal) | Installable build shared with a tester | 3 |

**Total estimated points: 66**
