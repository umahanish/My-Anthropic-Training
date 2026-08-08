import TaskList from './components/TaskList';

export default function App() {
  return (
    <main style={{ maxWidth: 480, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>Campus Task Manager</h1>
      <TaskList />
    </main>
  );
}
