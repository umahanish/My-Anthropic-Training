const express = require('express');
const userModel = require('../models/user');

const router = express.Router();

function toPublicUser(user) {
  const { passwordHash, ...publicUser } = user; // eslint-disable-line no-unused-vars
  return publicUser;
}

// POST /api/auth/signup — create an account (E1-2)
router.post('/signup', async (req, res) => {
  try {
    const user = await userModel.create(req.body || {});
    res.status(201).json(toPublicUser(user));
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

module.exports = router;
