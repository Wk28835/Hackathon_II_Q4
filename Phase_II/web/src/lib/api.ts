// phase_ii/web/lib/api.ts
import { Task, TaskStatus } from "@/types/task";
import { auth } from "@/lib/auth"; // server-side auth
import { headers } from "next/headers"; // Next.js server headers
import { generateBackendToken } from "@/lib/jwt";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

// Server-side API Client (for use in Server Components)
export async function getTasks(status?: TaskStatus): Promise<Task[]> {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session?.user) {
    throw new Error("Unauthorized");
  }

  // Generate JWT for backend API
  const token = await generateBackendToken(
    session.user.id,
    session.user.email,
    session.user.name || ""
  );
  
  // Determine URL with query params
  let url = `${API_BASE_URL}/api/tasks`;

  if (status) {
    url += `?status=${status}`;
  }
  const res = await fetch(url, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    cache: "no-store" // Dynamic data
  });

  if (!res.ok) {
    if (res.status === 401) throw new Error("Unauthorized");
    throw new Error(`Failed to fetch tasks: ${res.statusText} ${API_BASE_URL} ${token}`);
  }

  return res.json();
}
