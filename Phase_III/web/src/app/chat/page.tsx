// src/app/chat/page.tsx
"use client";

import React, { useState, useEffect, useRef } from 'react';
import MessageDisplay from '@/components/MessageDisplay';
import { Message } from '@/types/chat';
import { createConversation, getConversations, getMessages, sendMessage } from '@/actions/chat';
import { useRouter } from 'next/navigation';

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversations, setConversations] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function loadInitialData() {
    try {
      const convs = await getConversations(10);
      setConversations(convs);
      if (convs.length > 0) {
        setConversationId(convs[0].id);
        loadMessages(convs[0].id);
      }
    } catch (e) {
      console.error("Neural link failed", e);
    }
  }

  async function loadMessages(id: string) {
    setIsLoading(true);
    try {
      const msgs = await getMessages(id);
      setMessages(msgs);
      setConversationId(id);
    } catch (e) {
      console.error("Data retrieval error", e);
    } finally {
      setIsLoading(false);
    }
  }

  const handleSendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const messageText = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      let currentConvId = conversationId;

      if (!currentConvId) {
        const title = messageText.slice(0, 30) || "New Directives";
        const newConv = await createConversation(title);
        currentConvId = newConv.id;
        setConversationId(currentConvId);
      }

      const optimisticMsg: Message = {
        id: Date.now().toString(),
        conversation_id: currentConvId!,
        role: 'user',
        content: messageText,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, optimisticMsg]);

      const response = await sendMessage(currentConvId!, messageText);

      if (response.function_calls && response.function_calls.length > 0) {
        await loadMessages(currentConvId!);
        router.refresh();
      } else {
        const aiMsg: Message = {
          id: response.message_id,
          conversation_id: currentConvId!,
          role: 'assistant',
          content: response.content,
          created_at: new Date().toISOString()
        };
        setMessages(prev => [...prev, aiMsg]);
      }
    } catch (error) {
      console.error('Transmission failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-64px)] bg-[#020617] text-white overflow-hidden font-mono">
      
      {/* SIDEBAR: CONVERSATION HISTORY */}
      <aside className="hidden md:flex w-72 border-r border-emerald-500/10 flex-col bg-black/20 backdrop-blur-xl">
        <div className="p-4 border-b border-emerald-500/10 flex justify-between items-center">
          <span className="text-[10px] uppercase tracking-[0.2em] text-emerald-500/50">Neural_Archives</span>
          <button 
            onClick={() => {setConversationId(null); setMessages([]);}}
            className="p-1 hover:text-emerald-400 transition-colors"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 5v14M5 12h14"/></svg>
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => loadMessages(conv.id)}
              className={`w-full text-left p-3 rounded-lg text-xs transition-all border ${
                conversationId === conv.id 
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
                : 'border-transparent text-slate-500 hover:bg-white/5'
              }`}
            >
              <div className="truncate font-bold"># {conv.title || 'Untitled_Link'}</div>
              <div className="text-[9px] opacity-50 mt-1">{new Date(conv.created_at).toLocaleDateString()}</div>
            </button>
          ))}
        </div>
      </aside>

      {/* MAIN CHAT AREA */}
      <main className="flex-1 flex flex-col relative">
        {/* Decorative Grid Background */}
        <div className="absolute inset-0 z-0 opacity-[0.03] pointer-events-none" 
             style={{ backgroundImage: `radial-gradient(#10b981 1px, transparent 1px)`, backgroundSize: '30px 30px' }} />

        {/* Message Feed */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 relative z-10">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center space-y-6 text-center">
              <div className="w-20 h-20 rounded-full border border-emerald-500/20 bg-emerald-500/5 flex items-center justify-center animate-pulse">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="1"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
              </div>
              <div className="space-y-2">
                <h2 className="text-xl font-black uppercase tracking-tighter italic">Neural Link Established</h2>
                <p className="text-slate-500 text-xs uppercase tracking-widest max-w-xs leading-loose">
                  Input task directives or query existing data parameters. Gemini-1.5 is standing by.
                </p>
              </div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div key={msg.id || index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] md:max-w-[70%] ${msg.role === 'user' ? 'order-1' : 'order-2'}`}>
                   <MessageDisplay message={msg} />
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex items-center gap-3 text-emerald-500/50 text-[10px] uppercase tracking-[.2em]">
              <div className="flex gap-1">
                <div className="w-1 h-1 bg-emerald-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
                <div className="w-1 h-1 bg-emerald-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
                <div className="w-1 h-1 bg-emerald-500 rounded-full animate-bounce" />
              </div>
              Analyzing_Request...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Console Input */}
        <div className="p-4 md:p-8 from-[#020617] via-[#020617] to-transparent relative z-10">
          <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto relative group">
            <div className="absolute -inset-0.5 bg-emerald-500/20 rounded-2xl blur opacity-0 group-focus-within:opacity-100 transition duration-500"></div>
            <div className="relative flex gap-2 bg-black/40 border border-emerald-500/20 rounded-2xl p-2 backdrop-blur-xl">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Execute command (e.g., 'List my incomplete tasks')..."
                className="flex-1 bg-transparent border-none px-4 py-3 text-sm text-white focus:ring-0 placeholder:text-emerald-900/50"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="bg-emerald-600 text-black px-6 rounded-xl font-black uppercase text-[10px] tracking-widest hover:bg-emerald-400 disabled:opacity-20 transition-all"
              >
                Send
              </button>
            </div>
          </form>
          <p className="text-center mt-4 text-[9px] text-slate-700 uppercase tracking-widest">
            Gemini Core // Model Context Protocol v1.2
          </p>
        </div>
      </main>
    </div>
  );
}