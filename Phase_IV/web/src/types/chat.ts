// web/src/types/chat.ts

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'function';
  content: string;
  function_call?: {
    name: string;
    arguments: Record<string, any>;
  };
  function_response?: {
    name: string;
    result: any;
  };
  created_at: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatResponse {
  message_id: string;
  content: string;
  function_calls?: Array<{
    name: string;
    arguments: Record<string, any>;
  }>;
  function_responses?: Array<{
    name: string;
    result: any;
  }>;
}
