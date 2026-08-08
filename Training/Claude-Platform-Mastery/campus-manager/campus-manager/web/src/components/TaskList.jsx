import { useEffect, useState } from 'react';
import { listTasks, createTask, updateTask, deleteTask } from '../api/tasks';

// TEMP: hardcoded until E1-3 (login) wires up a real logged-in user.
const CURRENT_USER_ID = 'demo-user';

export default function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    try {
      setTasks(await listTasks(CURRENT_USER_ID));
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleAdd(e) {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await createTask(CURRENT_USER_ID, { title });
      setTitle('');
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleToggle(task) {
    const nextStatus = task.status === 'done' ? 'todo' : 'done';
    await updateTask(CURRENT_USER_ID, task.id, { status: nextStatus });
    await refresh();
  }

  async function handleDelete(task) {
    await deleteTask(CURRENT_USER_ID, task.id);
    await refresh();
  }

  return (
    <div>
      <h2>My Tasks</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleAdd}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task title"
        />
        <button type="submit">Add</button>
      </form>

      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <label>
              <input
                type="checkbox"
                checked={task.status === 'done'}
                onChange={() => handleToggle(task)}
              />
              <span
                style={{
                  textDecoration: task.status === 'done' ? 'line-through' : 'none',
                }}
              >
                {task.title}
              </span>
            </label>
            <button onClick={() => handleDelete(task)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
