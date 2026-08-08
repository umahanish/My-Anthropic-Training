const { v4: uuidv4 } = require('uuid');
const bcrypt = require('bcryptjs');

const SALT_ROUNDS = 10;

// In-memory store for now (matches models/task.js — see CLAUDE.md "Current
// implementation state"). Swap for a real DB once E1-1 tooling work lands.
let users = [];

function reset() {
  users = [];
}

function findByEmail(email) {
  return users.find((u) => u.email === email.trim().toLowerCase());
}

async function create({ name, email, password }) {
  if (!email || !email.trim()) {
    throw new Error('email is required');
  }
  if (!password || password.length < 8) {
    throw new Error('password must be at least 8 characters');
  }
  if (findByEmail(email)) {
    throw new Error('email is already registered');
  }

  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
  const user = {
    id: uuidv4(),
    name: name ? name.trim() : null,
    email: email.trim().toLowerCase(),
    passwordHash,
    createdAt: new Date().toISOString(),
  };
  users.push(user);
  return user;
}

module.exports = { create, findByEmail, reset };
