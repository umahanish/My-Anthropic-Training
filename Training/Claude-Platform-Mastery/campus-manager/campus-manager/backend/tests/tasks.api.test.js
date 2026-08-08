const request = require('supertest');
const createApp = require('../src/app');
const taskModel = require('../src/models/task');

const app = createApp();

beforeEach(() => {
  taskModel.reset();
});

describe('GET /api/health', () => {
  test('returns ok', async () => {
    const res = await request(app).get('/api/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});

describe('tasks API', () => {
  test('rejects requests with no x-user-id header', async () => {
    const res = await request(app).get('/api/tasks');
    expect(res.status).toBe(401);
  });

  test('full CRUD lifecycle for a task', async () => {
    // create
    const createRes = await request(app)
      .post('/api/tasks')
      .set('x-user-id', 'u1')
      .send({ title: 'Finish lab report', subject: 'Chemistry' });
    expect(createRes.status).toBe(201);
    const taskId = createRes.body.id;

    // list
    const listRes = await request(app).get('/api/tasks').set('x-user-id', 'u1');
    expect(listRes.status).toBe(200);
    expect(listRes.body).toHaveLength(1);

    // update (mark done)
    const patchRes = await request(app)
      .patch(`/api/tasks/${taskId}`)
      .set('x-user-id', 'u1')
      .send({ status: 'done' });
    expect(patchRes.status).toBe(200);
    expect(patchRes.body.status).toBe('done');

    // delete
    const deleteRes = await request(app)
      .delete(`/api/tasks/${taskId}`)
      .set('x-user-id', 'u1');
    expect(deleteRes.status).toBe(204);

    // confirm gone
    const listAfter = await request(app).get('/api/tasks').set('x-user-id', 'u1');
    expect(listAfter.body).toHaveLength(0);
  });

  test('a user cannot edit or delete another user\'s task', async () => {
    const createRes = await request(app)
      .post('/api/tasks')
      .set('x-user-id', 'u1')
      .send({ title: 'Private task' });
    const taskId = createRes.body.id;

    const patchRes = await request(app)
      .patch(`/api/tasks/${taskId}`)
      .set('x-user-id', 'u2')
      .send({ status: 'done' });
    expect(patchRes.status).toBe(404);

    const deleteRes = await request(app)
      .delete(`/api/tasks/${taskId}`)
      .set('x-user-id', 'u2');
    expect(deleteRes.status).toBe(404);
  });

  test('rejects creating a task with an empty title', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .set('x-user-id', 'u1')
      .send({ title: '' });
    expect(res.status).toBe(400);
  });
});
