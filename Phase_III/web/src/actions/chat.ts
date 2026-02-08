'use server';

import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { generateBackendToken } from "@/lib/jwt";
import { Conversation, Message, ChatResponse } from "@/types/chat";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

async function getAuthToken() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session?.user) {
    throw new Error("Unauthorized");
  }

  return generateBackendToken(
    session.user.id,
    session.user.email,
    session.user.name || ""
  );
}

export async function createConversation(title: string): Promise<Conversation> {
  const token = await getAuthToken();

  const res = await fetch(`${API_BASE_URL}/api/chat/conversations`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });

  if (!res.ok) {
    throw new Error(`Failed to create conversation: ${res.statusText}`);
  }

  return res.json();
}

export async function getConversations(limit: number = 20): Promise<any[]> {
  const token = await getAuthToken();

  const res = await fetch(`${API_BASE_URL}/api/chat/conversations?limit=${limit}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch conversations: ${res.statusText}`);
  }

  return res.json();
}

export async function getMessages(conversationId: string, limit: number = 50): Promise<Message[]> {
  const token = await getAuthToken();

  const res = await fetch(`${API_BASE_URL}/api/chat/${conversationId}/messages?limit=${limit}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch messages: ${res.statusText}`);
  }

  return res.json();
}

export async function sendMessage(conversationId: string, message: string, toolsEnabled: boolean = true): Promise<ChatResponse> {
  const token = await getAuthToken();

  const res = await fetch(`${API_BASE_URL}/api/chat/${conversationId}/messages`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      tools_enabled: toolsEnabled
    }),
  });

  if (!res.ok) {
    throw new Error(`Failed to send message: ${res.statusText}`);
  }

  return res.json();
}
