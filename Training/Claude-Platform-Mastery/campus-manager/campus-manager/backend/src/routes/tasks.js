const express = require('express');
const taskModel = require('../models/task');

const router = express.Router();

// Sprint 2 auth stand-in: real JWT auth lands in E1-2/E1-3. For now the
// caller identifies themselves via x-user-id so task ownership logic can be
// built and tested independently of the auth epic.
function requireUser(req, res, next) {
  const userId = req.header('x-user-id');
  if (!userId) {
    return res.status(401).json({ error: 'x-user-id header required' });
  }
  req.userId = userId;
  next();
}

router.use(requireUser);

// GET /api/tasks — list current user's tasks
router.get('/', (req, res) => {
  res.json(taskModel.listForUser(req.userId));
});

// POST /api/tasks — create a task (E2-1)
router.post('/', (req, res) => {
  try {
    const task = taskModel.create({ userId: req.userId, ...req.body });
    res.status(201).json(task);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// PATCH /api/tasks/:id — edit or toggle status (E2-3, E2-4)
router.patch('/:id', (req, res) => {
  try {
    const task = taskModel.update(req.params.id, req.userId, req.body);
    if (!task) return res.status(404).json({ error: 'task not found' });
    res.json(task);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// DELETE /api/tasks/:id (E2-5)
router.delete('/:id', (req, res) => {
  const deleted = taskModel.remove(req.params.id, req.userId);
  if (!deleted) return res.status(404).json({ error: 'task not found' });
  res.status(204).send();
});

module.exports = router;
