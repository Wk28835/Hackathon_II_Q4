import React from 'react';
import { Message } from '@/types/chat';

interface MessageDisplayProps {
  message: Message;
}

export default function MessageDisplay({ message }: MessageDisplayProps) {
  const isUser = message.role === 'user';
  const isFunction = message.role === 'function';
  const isAssistant = message.role === 'assistant';

  if (isFunction) {
    // Optionally hide raw function outputs or show them in a collapsible detail view
    // For now, we'll hide them to keep the UI clean, unless debugging is needed
    // Or we could show "Task created" etc. if detailed
    return null;
  }

  const messageClasses = isUser
    ? 'ml-auto bg-blue-600 text-white rounded-lg p-3 max-w-[80%] shadow-sm'
    : 'mr-auto bg-white border border-gray-200 text-gray-800 rounded-lg p-3 max-w-[80%] shadow-sm';

  return (
    <div className={`flex flex-col my-3 ${isUser ? 'items-end' : 'items-start'}`}>
      <div className={messageClasses}>
        <div className="whitespace-pre-wrap">{message.content}</div>

        {/* Display function calls if available (assistant intent) */}
        {message.function_call && (
          <div className="mt-2 text-xs bg-black/5 p-2 rounded border border-black/5 font-mono">
            <div className="font-semibold text-gray-500">Executing tool:</div>
            <div>{message.function_call.name}</div>
            <div className="truncate opacity-75">{JSON.stringify(message.function_call.arguments)}</div>
          </div>
        )}
      </div>
      <div className="text-xs text-gray-400 mt-1 px-1">
        {isUser ? 'You' : 'Todo AI'} • {new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  );
}