const { v4: uuidv4 } = require('uuid');

// In-memory store for now (Sprint 2 scope). Swap for a real DB (SQLite via
// an ORM) once E1-1 tooling work lands — see docs/architecture.md.
let tasks = [];

function reset() {
  tasks = [];
}

function create({ userId, title, subject, dueDate }) {
  if (!title || !title.trim()) {
    throw new Error('title is required');
  }
  const task = {
    id: uuidv4(),
    userId,
    title: title.trim(),
    subject: subject || null,
    dueDate: dueDate || null,
    status: 'todo',
    createdAt: new Date().toISOString(),
  };
  tasks.push(task);
  return task;
}

function listForUser(userId) {
  return tasks.filter((t) => t.userId === userId);
}

function findById(id) {
  return tasks.find((t) => t.id === id);
}

function update(id, userId, changes) {
  const task = findById(id);
  if (!task || task.userId !== userId) return null;

  if (changes.title !== undefined) task.title = changes.title;
  if (changes.subject !== undefined) task.subject = changes.subject;
  if (changes.dueDate !== undefined) task.dueDate = changes.dueDate;
  if (changes.status !== undefined) {
    if (!['todo', 'done'].includes(changes.status)) {
      throw new Error('status must be "todo" or "done"');
    }
    task.status = changes.status;
  }
  return task;
}

function remove(id, userId) {
  const task = findById(id);
  if (!task || task.userId !== userId) return false;
  tasks = tasks.filter((t) => t.id !== id);
  return true;
}

// Used by E4-1: is this task due within the next 24 hours?
function isDueSoon(task, now = new Date()) {
  if (!task.dueDate || task.status === 'done') return false;
  const due = new Date(task.dueDate);
  const diffMs = due.getTime() - now.getTime();
  const oneDayMs = 24 * 60 * 60 * 1000;
  return diffMs >= 0 && diffMs <= oneDayMs;
}

module.exports = { create, listForUser, findById, update, remove, isDueSoon, reset };
