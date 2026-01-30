// phase_ii/web/src/app/tasks/page.tsx
import { getTasks } from '@/lib/api';
import TaskList from '@/components/TaskList';
import SignOutButton from '@/components/SignOutButton';
import { Task } from '@/types/task';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';

export const dynamic = 'force-dynamic';

export default async function TasksPage() {
  const session = await auth.api.getSession({
     headers: await headers()
  });

  if (!session?.user) {
    redirect('/signin');
  }

  // Fetch tasks server-side
  let tasks: Task[] = [];
  try {
     tasks = await getTasks();
  } catch(e) {
     console.error("Failed to fetch tasks", e);
  }

  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <nav className="max-w-4xl mx-auto px-4 mb-8 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Task Manager</h1>
        <div className="flex items-center gap-4">
           {session.user.name && <span className="text-gray-600">Hello, {session.user.name}</span>}
           <SignOutButton />
        </div>
      </nav>
      <TaskList initialTasks={tasks} />
    </div>
  );
}
