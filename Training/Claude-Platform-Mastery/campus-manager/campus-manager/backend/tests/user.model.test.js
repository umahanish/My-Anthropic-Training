const userModel = require('../src/models/user');

beforeEach(() => {
  userModel.reset();
});

describe('user model', () => {
  test('create() saves a user with a hashed password', async () => {
    const user = await userModel.create({
      email: 'ada@example.com',
      password: 'password123',
    });
    expect(user.id).toBeDefined();
    expect(user.email).toBe('ada@example.com');
    expect(user.passwordHash).toBeDefined();
    expect(user.passwordHash).not.toBe('password123');
  });

  test('create() normalizes email to lowercase', async () => {
    const user = await userModel.create({
      email: 'Ada@Example.com',
      password: 'password123',
    });
    expect(user.email).toBe('ada@example.com');
  });

  test('create() rejects a missing email', async () => {
    await expect(
      userModel.create({ password: 'password123' })
    ).rejects.toThrow('email is required');
  });

  test('create() rejects a password shorter than 8 characters', async () => {
    await expect(
      userModel.create({ email: 'ada@example.com', password: 'short' })
    ).rejects.toThrow('password must be at least 8 characters');
  });

  test('create() rejects a duplicate email', async () => {
    await userModel.create({ email: 'ada@example.com', password: 'password123' });
    await expect(
      userModel.create({ email: 'ada@example.com', password: 'password456' })
    ).rejects.toThrow('already registered');
  });

  test('create() rejects a duplicate email regardless of case', async () => {
    await userModel.create({ email: 'ada@example.com', password: 'password123' });
    await expect(
      userModel.create({ email: 'ADA@EXAMPLE.COM', password: 'password456' })
    ).rejects.toThrow('already registered');
  });

  test('findByEmail() looks up a user case-insensitively', async () => {
    await userModel.create({ email: 'ada@example.com', password: 'password123' });
    expect(userModel.findByEmail('ADA@example.com')).toBeDefined();
    expect(userModel.findByEmail('nobody@example.com')).toBeUndefined();
  });
});
