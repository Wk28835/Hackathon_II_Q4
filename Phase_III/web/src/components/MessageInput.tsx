import React, { useState } from 'react';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
}

export default function MessageInput({ onSendMessage }: MessageInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex items-center">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleSend} // Allow sending with Enter key
        placeholder="Type your message..."
        className="flex-1 border border-gray-300 rounded-lg p-2 mr-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        onClick={handleSend}
        className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition duration-200"
      >
        Send
      </button>
    </div>
  );
}
