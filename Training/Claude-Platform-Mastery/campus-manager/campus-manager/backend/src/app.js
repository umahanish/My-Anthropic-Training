const express = require('express');
const authRouter = require('./routes/auth');
const tasksRouter = require('./routes/tasks');

function createApp() {
  const app = express();
  app.use(express.json());

  app.get('/api/health', (req, res) => res.json({ status: 'ok' }));
  app.use('/api/auth', authRouter);
  app.use('/api/tasks', tasksRouter);

  // Fallback error handler
  app.use((err, req, res, next) => {
    console.error(err); // eslint-disable-line no-console
    res.status(500).json({ error: 'internal server error' });
  });

  return app;
}

module.exports = createApp;
