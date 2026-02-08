// phase_ii/web/components/ChatWidget.tsx
'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Message } from '@/types/chat';
import { createConversation, getMessages, sendMessage, getConversations } from '@/actions/chat';
import MessageDisplay from './MessageDisplay';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversations, setConversations] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    if (isOpen) loadConversations();
  }, [isOpen]);

  useEffect(() => {
    if (conversationId && isOpen) loadMessages(conversationId);
  }, [conversationId, isOpen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function loadConversations() {
    try {
      const convs = await getConversations(5);
      setConversations(convs);
      if (!conversationId && convs.length > 0) setConversationId(convs[0].id);
    } catch (e) {
      console.error("Failed to load conversations", e);
    }
  }

  async function loadMessages(id: string) {
    setIsLoading(true);
    try {
      const msgs = await getMessages(id);
      setMessages(msgs);
    } catch (e) {
      console.error("Failed to load messages", e);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSend(e?: React.FormEvent) {
    e?.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMsgContent = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      let currentConvId = conversationId;
      if (!currentConvId) {
        const title = userMsgContent.slice(0, 30) || "New Neural Link";
        const newConv = await createConversation(title);
        currentConvId = newConv.id;
        setConversationId(currentConvId);
        setConversations([newConv, ...conversations]);
      }

      const optimisticMsg: Message = {
        id: Date.now().toString(),
        conversation_id: currentConvId,
        role: 'user',
        content: userMsgContent,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, optimisticMsg]);

      const response = await sendMessage(currentConvId, userMsgContent);

      if (response.function_calls && response.function_calls.length > 0) {
        await loadMessages(currentConvId);
        router.refresh();
      } else {
        const aiMsg: Message = {
          id: response.message_id,
          conversation_id: currentConvId,
          role: 'assistant',
          content: response.content,
          created_at: new Date().toISOString()
        };
        setMessages(prev => [...prev, aiMsg]);
      }
    } catch (e) {
      console.error("Failed to send message", e);
    } finally {
      setIsLoading(false);
    }
  }

  function handleNewChat() {
    setConversationId(null);
    setMessages([]);
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end font-mono">
      {/* --- CHAT INTERFACE --- */}
      {isOpen && (
        <div className="mb-4 w-[90vw] sm:w-100 h-150 bg-[#050505]/95 backdrop-blur-2xl rounded-2xl shadow-[0_0_50px_-12px_rgba(16,185,129,0.4)] border border-emerald-500/20 flex flex-col overflow-hidden animate-in slide-in-from-bottom-10 fade-in duration-500">
          
          {/* AI Header */}
          <div className="bg-emerald-950/40 p-4 border-b border-emerald-500/20 flex justify-between items-center shrink-0">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-ping absolute" />
                <div className="w-2 h-2 bg-emerald-500 rounded-full relative" />
              </div>
              <div className="flex flex-col">
                <span className="text-white text-xs font-black uppercase tracking-widest">Neural_Assistant</span>
                <span className="text-[9px] text-emerald-500/60 uppercase">Link-Status: Secure</span>
              </div>
            </div>
            <div className="flex gap-3">
              <button onClick={handleNewChat} className="p-1.5 hover:bg-emerald-500/10 rounded-md transition-colors text-emerald-500" title="Clear Buffer">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 5v14M5 12h14"/></svg>
              </button>
              <button onClick={() => setIsOpen(false)} className="p-1.5 hover:bg-emerald-500/10 rounded-md transition-colors text-emerald-500">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
              </button>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[radial-gradient(circle_at_top,#064e3b10_0%,transparent_100%)]">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 space-y-4">
                <div className="w-16 h-16 border border-emerald-500/20 rounded-full flex items-center justify-center bg-emerald-500/5">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#10b981" strokeWidth="1"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                </div>
                <div className="space-y-2">
                  <p className="text-emerald-500 text-xs font-bold uppercase tracking-widest">Awaiting Directives</p>
                  <p className="text-slate-500 text-[10px] leading-relaxed italic">"Initialize task: Buy neural-link components at 0900 hours"</p>
                </div>
              </div>
            ) : (
              messages.map((msg) => (
                <MessageDisplay key={msg.id} message={msg} />
              ))
            )}

            {isLoading && (
              <div className="flex items-center gap-3 text-emerald-500/50 text-[10px] uppercase tracking-[0.2em] ml-2">
                <span className="flex gap-1">
                  <span className="w-1 h-1 bg-emerald-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
                  <span className="w-1 h-1 bg-emerald-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
                  <span className="w-1 h-1 bg-emerald-500 rounded-full animate-bounce" />
                </span>
                Processing_Query...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <form onSubmit={handleSend} className="p-4 border-t border-emerald-500/10 bg-black/60 backdrop-blur-md">
            <div className="relative group">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Enter command..."
                className="w-full bg-emerald-950/10 border border-emerald-500/20 rounded-xl pl-4 pr-12 py-3 text-sm text-white placeholder:text-emerald-900 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-emerald-500 hover:text-emerald-400 disabled:opacity-20 transition-colors"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
              </button>
            </div>
          </form>
        </div>
      )}

      {/* --- FLOATING AI CORE (TOGGLE) --- */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="group relative h-16 w-16 flex items-center justify-center transition-all duration-300 active:scale-90"
      >
        {/* Orbiting Ring */}
        <div className={`absolute inset-0 rounded-full border-2 border-dashed border-emerald-500/30 animate-[spin_10s_linear_infinite] ${!isOpen && 'group-hover:border-emerald-500'}`} />
        
        {/* Core Button */}
        <div className={`relative h-12 w-12 rounded-full flex items-center justify-center shadow-2xl transition-all duration-500 ${isOpen ? 'bg-red-500/20 border border-red-500/40 rotate-90' : 'bg-emerald-500 shadow-[0_0_20px_#10b981] group-hover:shadow-[0_0_30px_#10b981]'}`}>
          {isOpen ? (
             <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="3"><path d="M18 6L6 18M6 6l12 12"/></svg>
          ) : (
             <div className="flex flex-col items-center gap-0.5">
               <div className="w-5 h-0.5 bg-black rounded-full" />
               <div className="w-3 h-0.5 bg-black rounded-full" />
               <div className="w-5 h-0.5 bg-black rounded-full" />
             </div>
          )}
        </div>
      </button>
    </div>
  );
}