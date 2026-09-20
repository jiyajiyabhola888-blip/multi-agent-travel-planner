import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, 
  Sparkles, 
  Send, 
  X, 
  Minimize2, 
  Maximize2, 
  Trash2, 
  MapPin, 
  Hotel, 
  Utensils, 
  CloudRain, 
  ArrowRight,
  ShieldCheck,
  MessageSquare
} from 'lucide-react';
import { askWanderAI } from '../../services/api';
import { ChatMessage } from '../../types';

interface WanderAIChatboxProps {
  currentDestination?: string;
  activeDestination?: string;
  onNavigateAction?: (action: string, payload?: any) => void;
  onTriggerAction?: (action: string, payload?: any) => void;
  isOpen: boolean;
  onClose: () => void;
}

const DEFAULT_PROMPTS = [
  "What should I do in Jaipur?",
  "Find me a boutique stay under ₹5,000",
  "Top vegetarian food & cafes nearby",
  "Make a 4-day realistic itinerary",
  "What if heavy rain disrupts my trip?",
  "Why did you choose this hotel route?"
];

export const WanderAIChatbox: React.FC<WanderAIChatboxProps> = ({
  currentDestination,
  activeDestination,
  onNavigateAction,
  onTriggerAction,
  isOpen,
  onClose
}) => {
  const dest = activeDestination || currentDestination || 'Jaipur';
  const handleActionTrigger = onTriggerAction || onNavigateAction || (() => {});
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'm-welcome',
      sender: 'assistant',
      text: `Hello! I'm **WanderAI**, your personal travel companion for **World Travelholic** 🌍.\n\nAsk me anything about destination sights, luxury stays, local food trails, or live trip recovery!`,
      timestamp: 'Just now',
      actions: [
        { label: 'Plan Trip with AI', action: 'PLAN_TRIP', payload: {} },
        { label: 'Explore Destinations', action: 'DISCOVER', payload: {} }
      ]
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputText).trim();
    if (!query) return;

    const userMsg: ChatMessage = {
      id: `u-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: 'Just now'
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await askWanderAI(query, currentDestination);
      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        sender: 'assistant',
        text: response.reply,
        city: response.city,
        actions: response.actions,
        timestamp: 'Just now'
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: 'assistant',
        text: "I'm experiencing a brief connection delay. Please try again or tap one of our suggested trip planning actions below!",
        timestamp: 'Just now',
        actions: [{ label: 'Plan with 15 Agents', action: 'PLAN_TRIP', payload: {} }]
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 'm-cleared',
        sender: 'assistant',
        text: `Conversation reset. How can I help you explore the world today?`,
        timestamp: 'Just now',
        actions: [
          { label: 'Plan a New Trip', action: 'PLAN_TRIP', payload: {} },
          { label: 'Discover Places', action: 'DISCOVER', payload: {} }
        ]
      }
    ]);
  };

  if (!isOpen) return null;

  return (
    <div 
      className={`fixed z-50 transition-all duration-300 ${
        isExpanded 
          ? 'inset-2 sm:inset-6 md:inset-12 bg-white rounded-3xl shadow-2xl flex flex-col border border-brand-200' 
          : 'bottom-4 right-4 sm:bottom-6 sm:right-6 w-[calc(100vw-2rem)] sm:w-[420px] h-[580px] max-h-[85vh] bg-white rounded-3xl shadow-soft-xl border border-brand-100 flex flex-col overflow-hidden'
      }`}
    >
      {/* Chat Header */}
      <div className="p-4 sm:p-5 bg-gradient-to-r from-brand-500 via-rose-600 to-blush-600 text-white flex items-center justify-between shadow-soft">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white border border-white/30 shadow-inner">
            <Sparkles className="w-5 h-5 text-rose-100" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h3 className="font-extrabold text-base tracking-tight">WanderAI</h3>
              <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            </div>
            <p className="text-xs text-rose-100 font-medium">Your personal travel assistant</p>
          </div>
        </div>

        <div className="flex items-center gap-1 text-white/80">
          <button 
            onClick={handleClearChat} 
            title="Clear conversation"
            className="p-1.5 hover:text-white hover:bg-white/15 rounded-xl transition-colors"
          >
            <Trash2 className="w-4 h-4" />
          </button>
          <button 
            onClick={() => setIsExpanded(!isExpanded)} 
            title={isExpanded ? "Collapse" : "Expand"}
            className="p-1.5 hover:text-white hover:bg-white/15 rounded-xl transition-colors hidden sm:inline-flex"
          >
            {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
          <button 
            onClick={onClose} 
            title="Close"
            className="p-1.5 hover:text-white hover:bg-white/15 rounded-xl transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Current Destination Context Pill */}
      {currentDestination && (
        <div className="bg-rose-50 px-4 py-2 border-b border-rose-100 flex items-center justify-between text-xs text-brand-800">
          <div className="flex items-center gap-1.5 font-semibold">
            <MapPin className="w-3.5 h-3.5 text-brand-600" />
            <span>Active Destination: {currentDestination}</span>
          </div>
          <span className="text-[10px] font-bold uppercase bg-white px-2 py-0.5 rounded-full border border-rose-200">Context Active</span>
        </div>
      )}

      {/* Chat Messages Body */}
      <div className="flex-1 p-4 sm:p-5 overflow-y-auto space-y-4 bg-gradient-to-b from-[#FFFDFD] to-rose-50/20">
        {messages.map((msg) => (
          <div 
            key={msg.id} 
            className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div 
              className={`max-w-[85%] sm:max-w-[80%] p-3.5 sm:p-4 rounded-2xl text-xs sm:text-sm leading-relaxed shadow-xs ${
                msg.sender === 'user'
                  ? 'bg-gradient-to-r from-brand-500 to-rose-600 text-white rounded-br-xs'
                  : 'bg-white border border-rose-100/80 text-charcoal-900 rounded-bl-xs shadow-soft'
              }`}
            >
              <div className="whitespace-pre-wrap">
                {msg.text.split('\n').map((line, lIdx) => {
                  if (line.startsWith('• ')) {
                    return <p key={lIdx} className="ml-2 font-medium my-0.5">{line}</p>;
                  }
                  return <p key={lIdx} className="my-1">{line}</p>;
                })}
              </div>
            </div>

            {/* Actionable buttons inside AI message */}
            {msg.actions && msg.actions.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mt-2 ml-1">
                {msg.actions.map((act, actIdx) => (
                  <button
                    key={actIdx}
                    onClick={() => {
                      handleActionTrigger(act.action, act.payload);
                      onClose();
                    }}
                    className="px-3 py-1.5 rounded-xl bg-white border border-brand-200 hover:border-brand-500 hover:bg-brand-50 text-brand-700 text-xs font-bold shadow-xs flex items-center gap-1 transition-all"
                  >
                    <span>{act.label}</span>
                    <ArrowRight className="w-3 h-3 text-brand-500" />
                  </button>
                ))}
              </div>
            )}

            <span className="text-[10px] text-slate-400 mt-1 px-1">{msg.timestamp}</span>
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 p-3 bg-white rounded-2xl border border-rose-100 shadow-soft w-fit">
            <div className="w-2 h-2 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 rounded-full bg-rose-500 animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 rounded-full bg-blush-500 animate-bounce" style={{ animationDelay: '300ms' }} />
            <span className="text-xs font-semibold text-brand-700 ml-1">WanderAI is researching...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompt Chips */}
      <div className="px-3 py-2 bg-white border-t border-rose-100 flex gap-1.5 overflow-x-auto no-scrollbar">
        {DEFAULT_PROMPTS.map((prompt, pIdx) => (
          <button
            key={pIdx}
            onClick={() => handleSendMessage(prompt)}
            className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full bg-rose-50 hover:bg-rose-100 text-brand-800 font-semibold border border-rose-200 transition-colors"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Input Bar */}
      <div className="p-3 sm:p-4 bg-white border-t border-rose-100 flex items-center gap-2">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Ask WanderAI anything..."
          className="flex-1 px-4 py-3 rounded-xl border border-rose-200 text-xs sm:text-sm font-medium text-charcoal-900 focus:outline-none focus:ring-2 focus:ring-brand-500 bg-rose-50/20"
        />
        <button
          onClick={() => handleSendMessage()}
          disabled={!inputText.trim() || isLoading}
          className="w-11 h-11 rounded-xl bg-gradient-to-r from-brand-500 to-rose-600 text-white flex items-center justify-center hover:shadow-glow-pink disabled:opacity-40 disabled:cursor-not-allowed transition-all shrink-0"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
