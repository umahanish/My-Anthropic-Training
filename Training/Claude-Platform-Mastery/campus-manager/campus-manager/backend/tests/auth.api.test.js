const request = require('supertest');
const createApp = require('../src/app');
const userModel = require('../src/models/user');

const app = createApp();

beforeEach(() => {
  userModel.reset();
});

describe('POST /api/auth/signup', () => {
  test('creates an account and never returns the password hash', async () => {
    const res = await request(app).post('/api/auth/signup').send({
      name: 'Ada Lovelace',
      email: 'ada@example.com',
      password: 'password123',
    });

    expect(res.status).toBe(201);
    expect(res.body.id).toBeDefined();
    expect(res.body.email).toBe('ada@example.com');
    expect(res.body.name).toBe('Ada Lovelace');
    expect(res.body.passwordHash).toBeUndefined();
    expect(res.body.password).toBeUndefined();
  });

  test('rejects a signup with no password', async () => {
    const res = await request(app)
      .post('/api/auth/signup')
      .send({ email: 'ada@example.com' });
    expect(res.status).toBe(400);
  });

  test('rejects a signup with no email', async () => {
    const res = await request(app)
      .post('/api/auth/signup')
      .send({ password: 'password123' });
    expect(res.status).toBe(400);
  });

  test('rejects a duplicate email', async () => {
    await request(app)
      .post('/api/auth/signup')
      .send({ email: 'ada@example.com', password: 'password123' });

    const res = await request(app)
      .post('/api/auth/signup')
      .send({ email: 'ada@example.com', password: 'password456' });

    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/already registered/);
  });
});
