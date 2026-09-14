"use client";

import { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../store/chatStore';
import { Send, BookOpen, ShieldCheck, ShieldAlert, Menu, FolderOpen, Shield, Search, Clock, Leaf, Activity, ChevronRight } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function Home() {
  const [input, setInput] = useState('');
  const { messages, isLoading, addMessage, setLoading, clearMessages, setMessages } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [activeSession, setActiveSession] = useState('new');

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleQuickAction = (actionText: string) => {
    setInput(actionText);
    // Automatically submit after a short delay for better UX
    setTimeout(() => {
      const form = document.getElementById('chat-form') as HTMLFormElement;
      if (form) form.requestSubmit();
    }, 100);
  };

  const loadMockHistory = (type: 'ashwagandha' | 'triphala') => {
    setActiveSession(type);
    if (type === 'ashwagandha') {
      setMessages([
        { id: '1', role: 'user', content: 'Check patentability of Ashwagandha extract for sleep aid in India.' },
        { 
          id: '2', 
          role: 'assistant', 
          content: 'Based on the Traditional Knowledge Digital Library (TKDL) and Indian Patent Act Section 3(p), the use of Ashwagandha (*Withania somnifera*) for sleep regulation is well-documented in classical Ayurvedic texts.\n\n### Novelty Assessment\nExtracting it for a known traditional use does not constitute patentable subject matter under Section 3(p) unless a synergistic effect with other ingredients is proven.\n\n### Recommendations\n1. Focus on unique extraction processes or novel synergistic formulations.\n2. Consider protecting the formulation under trade secrets if patentability criteria are not met.',
          classification: 'Patentability Assessment',
          alerts: [
            { check_name: 'Section 3(p) Compliance', status: 'FAIL', reason: 'Traditional knowledge is not patentable.' },
            { check_name: 'Novelty', status: 'REVIEW', reason: 'Requires proof of synergistic effect.' }
          ],
          sources: [
            { name: 'TKDL', section: 'Formulation TK-1234' },
            { name: 'Charaka Samhita', section: 'Sutra Sthana, Ch. 4' }
          ]
        }
      ]);
    } else {
      setMessages([
        { id: '1', role: 'user', content: 'Is Triphala safe for long-term daily use according to Ayush guidelines?' },
        { 
          id: '2', 
          role: 'assistant', 
          content: 'Triphala (a combination of Amalaki, Bibhitaki, and Haritaki) is classified as a *Rasayana* (rejuvenative) in Ayurveda.\n\nAccording to Ayush Ministry guidelines and classical texts, it is generally safe for long-term daily use in appropriate dosages. However, as it has mild laxative properties, continuous use without breaks may cause dependency in some individuals.',
          classification: 'Safety & Regulatory Check',
          alerts: [
            { check_name: 'Ayush Safety Guidelines', status: 'CLEAR', reason: 'Approved for general use as Rasayana.' }
          ],
          sources: [
            { name: 'Ayush Pharmacopoeia', section: 'Part 1, Vol 1' }
          ]
        }
      ]);
    }
  };

  const startNewSession = () => {
    setActiveSession('new');
    clearMessages();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    addMessage({ id: Date.now().toString(), role: 'user', content: userMessage });
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/v1/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userMessage,
          jurisdiction: 'india',
          language: 'en'
        }),
      });

      if (!res.ok) {
        const detail = await res.text();
        throw new Error(`Backend error (${res.status}): ${detail || 'No detail returned'}`);
      }
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
        content: `**Request Error:** ${error instanceof Error ? error.message : 'Unable to contact the IP-SHAKTI backend.'}`
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-layout">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <Leaf size={24} color="var(--primary-brand)" />
          <h2>IP-SHAKTI</h2>
        </div>
        <div className="sidebar-content">
          <div style={{ marginBottom: '2rem' }}>
            <h3 className="sidebar-section-title">Active Session</h3>
            <div 
              className={`sidebar-item ${activeSession === 'new' ? 'active' : ''}`}
              onClick={startNewSession}
            >
              <FolderOpen size={18} />
              <span>New Formulation</span>
            </div>
          </div>

          <div>
            <h3 className="sidebar-section-title">Recent Consultations</h3>
            <div 
              className={`sidebar-item ${activeSession === 'ashwagandha' ? 'active' : ''}`}
              onClick={() => loadMockHistory('ashwagandha')}
            >
              <Clock size={16} />
              <span style={{ fontSize: '0.9rem' }}>Ashwagandha Extract</span>
            </div>
            <div 
              className={`sidebar-item ${activeSession === 'triphala' ? 'active' : ''}`}
              onClick={() => loadMockHistory('triphala')}
            >
              <Search size={16} />
              <span style={{ fontSize: '0.9rem' }}>Triphala Safety Check</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-main">
        {/* Top Navigation Bar */}
        <header className="top-nav">
          <div className="nav-title">
            <Menu className="mobile-menu-icon" size={20} style={{ display: 'none' }} />
            <Shield size={22} color="var(--tertiary-mint)" />
            <span>Ayurvedic Intellectual Property & Patent Advisor</span>
          </div>
          <div className="status-pill">
            <div className="status-indicator"></div>
            AYUSH Compliant Core
          </div>
        </header>

        {/* Messages Feed */}
        <div className="messages-area">
          {messages.length === 0 && (
            <div className="empty-state-container">
              <div className="hero-icon-wrapper">
                <Leaf size={56} color="var(--primary-brand)" />
              </div>
              <h2 className="empty-state-title">IP-SHAKTI Regulatory Intelligence</h2>
              <p className="empty-state-subtitle">
                Cross-reference TKDL, WIPO, and classical Ayurvedic texts to ensure regulatory compliance and evaluate patentability of traditional formulations.
              </p>
              
              <div className="quick-actions-grid">
                <div className="quick-action-card" onClick={() => handleQuickAction("Evaluate patentability of Ashwagandha and Turmeric extract.")}>
                  <div className="quick-action-icon"><Search size={20} /></div>
                  <div>
                    <h3>Novelty Search</h3>
                    <p>Evaluate formulation novelty against TKDL.</p>
                  </div>
                </div>
                <div className="quick-action-card" onClick={() => handleQuickAction("What are the patent criteria for Chyawanprash formulation under Section 3(p)?")}>
                  <div className="quick-action-icon"><BookOpen size={20} /></div>
                  <div>
                    <h3>Patent Criteria</h3>
                    <p>Review Section 3(p) requirements.</p>
                  </div>
                </div>
                <div className="quick-action-card" onClick={() => handleQuickAction("Verify safety guidelines for long term usage of Triphala.")}>
                  <div className="quick-action-icon"><Activity size={20} /></div>
                  <div>
                    <h3>Safety Check</h3>
                    <p>Verify Ayush Ministry safety guidelines.</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id} className={`message-wrapper ${msg.role}`}>
              <div className={`avatar ${msg.role === 'user' ? 'user' : 'ai'}`}>
                {msg.role === 'user' ? <div style={{fontWeight: 'bold', fontSize: '1.2rem'}}>U</div> : <Leaf size={24} />}
              </div>
              
              <div style={{ width: '100%' }}>
                {msg.role === 'assistant' && msg.classification && (
                  <div className="classification-badge">
                    <ShieldCheck size={14} /> {msg.classification.replace(/_/g, ' ').toUpperCase()}
                  </div>
                )}
                
                <div className="message-card">
                  {/* Markdown Renderer for Rich Responses */}
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>

                  {/* Compliance Alerts Grid */}
                  {msg.role === 'assistant' && msg.alerts && msg.alerts.length > 0 && (
                    <div className="alerts-grid">
                      {msg.alerts.map((alert, idx) => {
                        const statusClass = alert.status ? alert.status.toLowerCase() : 'review';
                        return (
                          <div key={idx} className={`alert-card ${statusClass}`}>
                            <div className="alert-icon">
                              {alert.status === 'CLEAR' ? <ShieldCheck size={20} /> : <ShieldAlert size={20} />}
                            </div>
                            <div className="alert-content">
                              <h4>{alert.check_name || 'Regulatory Check'}</h4>
                              <p>{alert.reason}</p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Citation Chips */}
                  {msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                    <div className="citations-section">
                      <div className="citations-title">
                        <BookOpen size={18} /> Verified Citations
                      </div>
                      <div>
                        {msg.sources.map((src, idx) => (
                          <span key={idx} className="citation-chip">
                            {src.name} • {src.section}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message-wrapper ai">
              <div className="avatar ai">
                <Leaf size={24} />
              </div>
              <div className="message-card" style={{ width: '100%', maxWidth: '400px' }}>
                <div className="loading-skeleton">
                  <div className="skeleton-line w-3-4"></div>
                  <div className="skeleton-line w-1-2"></div>
                  <div className="skeleton-line"></div>
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 500 }}>
                  <Search size={14} className="animate-spin" style={{ animation: 'spin 2s linear infinite' }} /> Querying TKDL & WIPO Databases...
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} style={{ height: '40px' }} />
        </div>

        {/* Fixed Floating Input Bar */}
        <form id="chat-form" className="input-container" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Inquire on Ayurvedic formulations, novelty, or patent claims..."
            disabled={isLoading}
          />
          <button type="submit" className="send-btn" disabled={!input.trim() || isLoading}>
            <ChevronRight size={24} />
          </button>
        </form>
      </main>
    </div>
  );
}
