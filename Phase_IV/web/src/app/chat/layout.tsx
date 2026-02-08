import React from 'react';

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col h-screen  bg-gray-900">
      {/* The main content of the chat page will be rendered here */}
      {children}
    </div>
  );
}
