const taskModel = require('../src/models/task');

beforeEach(() => {
  taskModel.reset();
});

describe('task model', () => {
  test('create() saves a task with default status "todo"', () => {
    const task = taskModel.create({ userId: 'u1', title: 'Read chapter 3' });
    expect(task.id).toBeDefined();
    expect(task.status).toBe('todo');
    expect(task.title).toBe('Read chapter 3');
  });

  test('create() rejects an empty title', () => {
    expect(() => taskModel.create({ userId: 'u1', title: '  ' })).toThrow(
      'title is required'
    );
  });

  test('listForUser() only returns tasks owned by that user', () => {
    taskModel.create({ userId: 'u1', title: 'Task A' });
    taskModel.create({ userId: 'u2', title: 'Task B' });
    const result = taskModel.listForUser('u1');
    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Task A');
  });

  test('update() toggles status', () => {
    const task = taskModel.create({ userId: 'u1', title: 'Task A' });
    const updated = taskModel.update(task.id, 'u1', { status: 'done' });
    expect(updated.status).toBe('done');
  });

  test('update() rejects an invalid status', () => {
    const task = taskModel.create({ userId: 'u1', title: 'Task A' });
    expect(() => taskModel.update(task.id, 'u1', { status: 'archived' })).toThrow(
      'status must be'
    );
  });

  test('update() returns null when task belongs to another user', () => {
    const task = taskModel.create({ userId: 'u1', title: 'Task A' });
    const result = taskModel.update(task.id, 'u2', { status: 'done' });
    expect(result).toBeNull();
  });

  test('remove() deletes only the owner\'s task', () => {
    const task = taskModel.create({ userId: 'u1', title: 'Task A' });
    expect(taskModel.remove(task.id, 'u2')).toBe(false);
    expect(taskModel.remove(task.id, 'u1')).toBe(true);
    expect(taskModel.findById(task.id)).toBeUndefined();
  });

  describe('isDueSoon()', () => {
    test('true when due within 24 hours and not done', () => {
      const now = new Date('2026-07-25T12:00:00Z');
      const task = {
        status: 'todo',
        dueDate: new Date('2026-07-26T06:00:00Z').toISOString(),
      };
      expect(taskModel.isDueSoon(task, now)).toBe(true);
    });

    test('false when task is already done', () => {
      const now = new Date('2026-07-25T12:00:00Z');
      const task = {
        status: 'done',
        dueDate: new Date('2026-07-26T06:00:00Z').toISOString(),
      };
      expect(taskModel.isDueSoon(task, now)).toBe(false);
    });

    test('false when due date is more than 24 hours away', () => {
      const now = new Date('2026-07-25T12:00:00Z');
      const task = {
        status: 'todo',
        dueDate: new Date('2026-07-30T12:00:00Z').toISOString(),
      };
      expect(taskModel.isDueSoon(task, now)).toBe(false);
    });

    test('false when the due date has already passed', () => {
      const now = new Date('2026-07-25T12:00:00Z');
      const task = {
        status: 'todo',
        dueDate: new Date('2026-07-20T12:00:00Z').toISOString(),
      };
      expect(taskModel.isDueSoon(task, now)).toBe(false);
    });
  });
});
