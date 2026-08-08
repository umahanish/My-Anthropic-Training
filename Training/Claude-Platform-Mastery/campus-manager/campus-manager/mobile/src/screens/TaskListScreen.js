import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import { listTasks, createTask, updateTask, deleteTask } from '../api/tasks';

// TEMP: hardcoded until login (E6-1) wires up a real logged-in user.
const CURRENT_USER_ID = 'demo-user';

export default function TaskListScreen() {
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

  async function handleAdd() {
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
    <View style={styles.container}>
      <Text style={styles.heading}>My Tasks</Text>
      {error && <Text style={styles.error}>{error}</Text>}

      <View style={styles.addRow}>
        <TextInput
          style={styles.input}
          value={title}
          onChangeText={setTitle}
          placeholder="New task title"
        />
        <Button title="Add" onPress={handleAdd} />
      </View>

      <FlatList
        data={tasks}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.row}>
            <TouchableOpacity onPress={() => handleToggle(item)} style={styles.taskText}>
              <Text
                style={item.status === 'done' ? styles.doneText : styles.todoText}
              >
                {item.title}
              </Text>
            </TouchableOpacity>
            <Button title="Delete" onPress={() => handleDelete(item)} />
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, paddingTop: 48 },
  heading: { fontSize: 22, fontWeight: 'bold', marginBottom: 12 },
  error: { color: 'red', marginBottom: 8 },
  addRow: { flexDirection: 'row', gap: 8, marginBottom: 16 },
  input: { flex: 1, borderWidth: 1, borderColor: '#ccc', borderRadius: 6, padding: 8 },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  taskText: { flex: 1 },
  todoText: { fontSize: 16 },
  doneText: { fontSize: 16, textDecorationLine: 'line-through', color: '#888' },
});
