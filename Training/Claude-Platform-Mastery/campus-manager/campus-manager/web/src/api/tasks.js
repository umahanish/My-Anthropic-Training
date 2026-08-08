// Thin wrapper around the tasks API. Swap the x-user-id stub for a real
// Authorization: Bearer <jwt> header once E1-3 (login) lands on the client.
const BASE_URL = '/api/tasks';

function headers(userId) {
  return {
    'Content-Type': 'application/json',
    'x-user-id': userId,
  };
}

export async function listTasks(userId) {
  const res = await fetch(BASE_URL, { headers: headers(userId) });
  if (!res.ok) throw new Error('Failed to load tasks');
  return res.json();
}

export async function createTask(userId, task) {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: headers(userId),
    body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error('Failed to create task');
  return res.json();
}

export async function updateTask(userId, taskId, changes) {
  const res = await fetch(`${BASE_URL}/${taskId}`, {
    method: 'PATCH',
    headers: headers(userId),
    body: JSON.stringify(changes),
  });
  if (!res.ok) throw new Error('Failed to update task');
  return res.json();
}

export async function deleteTask(userId, taskId) {
  const res = await fetch(`${BASE_URL}/${taskId}`, {
    method: 'DELETE',
    headers: headers(userId),
  });
  if (!res.ok) throw new Error('Failed to delete task');
}
