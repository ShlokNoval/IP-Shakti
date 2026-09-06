"use client";

import { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../store/chatStore';
import { Send, Bot, User, ShieldCheck, ShieldAlert, BookOpen } from 'lucide-react';

export default function Home() {
  const [input, setInput] = useState('');
  const { messages, isLoading, addMessage, setLoading } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    addMessage({ id: Date.now().toString(), role: 'user', content: userMessage });
    setLoading(true);

    try {
      // Call our FastAPI backend
      const res = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userMessage,
          jurisdiction: 'india',
          language: 'en'
        }),
      });

      if (!res.ok) throw new Error('Backend responded with an error');
      const data = await res.json();

      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.guidance_text,
        classification: data.classification,
        alerts: data.compliance_alerts,
        sources: data.sources
      });
    } catch (error) {
      console.error(error);
      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I couldn't reach the IP-SHAKTI backend. Make sure the FastAPI server is running!"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>IP-SHAKTI</h1>
        <p>Advanced Ayurvedic Regulatory & IP Advisor</p>
      </header>

      <div className="messages-area">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '4rem' }}>
            <Bot size={48} style={{ opacity: 0.5, marginBottom: '1rem' }} />
            <h2>Welcome to IP-SHAKTI</h2>
            <p>Describe your Ayurvedic formulation or ask a regulatory question.</p>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-avatar">
              {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
            </div>
            
            <div className="message-content">
              {/* If it's the AI, show the rich structured data */}
              {msg.role === 'assistant' && msg.classification && (
                <div className="badge">{msg.classification.replace(/_/g, ' ')}</div>
              )}
              
              <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
                {msg.content}
              </div>

              {msg.role === 'assistant' && msg.alerts && msg.alerts.length > 0 && (
                <div className="alerts-container">
                  {msg.alerts.map((alert, idx) => (
                    <div key={idx} className={`alert ${alert.status.toLowerCase()}`}>
                      {alert.status === 'CLEAR' ? <ShieldCheck size={16} /> : <ShieldAlert size={16} />}
                      <div>
                        <strong>{alert.check_name}:</strong> {alert.reason}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                <div className="sources-container">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <BookOpen size={14} /> <strong>Citations:</strong>
                  </div>
                  <ul style={{ paddingLeft: '1.5rem' }}>
                    {msg.sources.map((src, idx) => (
                      <li key={idx}>
                        {src.name} - {src.section}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
             <div className="message-avatar"><Bot size={20} /></div>
             <div className="message-content" style={{ opacity: 0.7 }}>Analyzing query...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="input-area" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="e.g. Can I patent a new cream containing Turmeric and Neem?"
          disabled={isLoading}
        />
        <button type="submit" disabled={!input.trim() || isLoading}>
          <Send size={18} /> Send
        </button>
      </form>
    </div>
  );
}
