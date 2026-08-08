import React from 'react';
import { SafeAreaView } from 'react-native';
import TaskListScreen from './src/screens/TaskListScreen';

export default function App() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <TaskListScreen />
    </SafeAreaView>
  );
}
