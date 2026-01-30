// phase_ii/web/types/task.ts

export type TaskStatus = 'Incomplete' | 'Complete';

export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
}

export interface TaskStatusUpdate {
  status: TaskStatus;
}
