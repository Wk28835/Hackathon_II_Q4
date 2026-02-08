"use server";

import { TaskCreate, TaskStatus, TaskStatusUpdate, TaskUpdate } from "@/types/task";
import { auth } from "@/lib/auth"; // server-side auth
import { headers } from "next/headers"; // Next.js server headers
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { generateBackendToken } from "@/lib/jwt";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

async function getBackendToken() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  if (!session?.user) {
    redirect("/signin");
  }
  // Generate JWT for backend API calls
  return generateBackendToken(session.user.id, session.user.email, session.user.name || "");
}

export async function createTask(data: TaskCreate) {
  const token = await getBackendToken();

  const res = await fetch(`${API_BASE_URL}/api/tasks`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Failed to create task");
  }

  revalidatePath("/tasks");
  return res.json();
}

export async function updateTask(id: number, data: TaskUpdate) {
  const token = await getBackendToken();

  const res = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Failed to update task");
  }

  revalidatePath("/tasks");
  return res.json();
}

export async function deleteTask(id: number) {
  const token = await getBackendToken();

  const res = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Failed to delete task");
  }

  revalidatePath("/tasks");
}

export async function updateTaskStatus(id: number, newStatus: TaskStatus) {
  const token = await getBackendToken();
  const payload: TaskStatusUpdate = { status: newStatus };

  const res = await fetch(`${API_BASE_URL}/api/tasks/${id}/status`, {
    method: "PATCH",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Failed to update task status");
  }

  revalidatePath("/tasks");
  return res.json();
}
