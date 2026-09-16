"use client";

import { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../store/chatStore';
import { 
  BookOpen, 
  ShieldCheck, 
  ShieldAlert, 
  Menu, 
  FolderOpen, 
  Shield, 
  Search, 
  Clock, 
  Leaf, 
  Activity, 
  ChevronRight,
  Sparkles,
  MessageSquare
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import IntakeWizard from '../components/IntakeWizard';

export default function Home() {
  const [input, setInput] = useState('');
  const [viewMode, setViewMode] = useState<'wizard' | 'chat'>('wizard');
  const [jurisdiction, setJurisdiction] = useState<'india' | 'international'>('india');
  const { messages, isLoading, addMessage, setLoading, clearMessages } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [activeSession, setActiveSession] = useState('new');

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const executeUserQuery = async (userQuery: string, customJurisdiction?: 'india' | 'international') => {
    if (!userQuery.trim() || isLoading) return;

    const activeJurisdiction = customJurisdiction || jurisdiction;
    const queryText = userQuery.trim();
    setInput('');
    setViewMode('chat');
    addMessage({ id: Date.now().toString(), role: 'user', content: queryText });
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/v1/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: queryText,
          jurisdiction: activeJurisdiction,
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

  const handleWizardSubmit = (compiledProfile: string, _category: string, targetJurisdiction: 'india' | 'international') => {
    setActiveSession('wizard-profile');
    setJurisdiction(targetJurisdiction);
    executeUserQuery(compiledProfile, targetJurisdiction);
  };

  const handleQuickAction = (actionText: string) => {
    executeUserQuery(actionText);
  };

  const loadConsultation = (query: string, label: string, targetJurisdiction: 'india' | 'international' = 'india') => {
    setActiveSession(label);
    setJurisdiction(targetJurisdiction);
    executeUserQuery(query, targetJurisdiction);
  };

  const startNewSession = () => {
    setActiveSession('new');
    clearMessages();
    setViewMode('wizard');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    executeUserQuery(input);
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
              <span>New Guided Intake</span>
            </div>
          </div>

          <div>
            <h3 className="sidebar-section-title">Recent Consultations</h3>
            <div 
              className={`sidebar-item ${activeSession === 'ashwagandha' ? 'active' : ''}`}
              onClick={() => loadConsultation('Check patentability and Section 3(p) criteria of Ashwagandha extract in India.', 'ashwagandha', 'india')}
            >
              <Clock size={16} />
              <span style={{ fontSize: '0.9rem' }}>Ashwagandha (India IPO)</span>
            </div>
            <div 
              className={`sidebar-item ${activeSession === 'triphala' ? 'active' : ''}`}
              onClick={() => loadConsultation('Verify Ayush Ministry safety guidelines for long term daily use of Triphala formulation.', 'triphala', 'india')}
            >
              <Search size={16} />
              <span style={{ fontSize: '0.9rem' }}>Triphala Safety Check</span>
            </div>
            <div 
              className={`sidebar-item ${activeSession === 'wipo-pct' ? 'active' : ''}`}
              onClick={() => loadConsultation('Evaluate international patentability and WIPO PCT prior art search for standardized botanical extract with Nagoya Protocol ABS compliance.', 'wipo-pct', 'international')}
            >
              <BookOpen size={16} />
              <span style={{ fontSize: '0.9rem' }}>Global PCT Filing</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Chat & Wizard Area */}
      <main className="chat-main">
        {/* Top Navigation Bar */}
        <header className="top-nav">
          <div className="nav-title">
            <Menu className="mobile-menu-icon" size={20} style={{ display: 'none' }} />
            <Shield size={22} color="var(--tertiary-mint)" />
            <span>Ayurvedic Intellectual Property & Patent Advisor</span>
          </div>

          {/* Navigation Controls: Mode Toggle + Jurisdiction Toggle */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
            {/* Jurisdiction Switcher */}
            <div className="jurisdiction-toggle-group">
              <button 
                type="button"
                className={`jurisdiction-btn ${jurisdiction === 'india' ? 'active' : ''}`}
                onClick={() => setJurisdiction('india')}
                title="Indian Legal Scope: Patents Act 1970, Section 3(p), AYUSH Rules, Biological Diversity Act 2002"
              >
                <span>🇮🇳 India (IPO / AYUSH)</span>
              </button>
              <button 
                type="button"
                className={`jurisdiction-btn ${jurisdiction === 'international' ? 'active' : ''}`}
                onClick={() => setJurisdiction('international')}
                title="International Legal Scope: WIPO PCT, EPO, USPTO, Nagoya Protocol, CBD"
              >
                <span>🌐 Global (PCT / WIPO)</span>
              </button>
            </div>

            {/* Mode Switcher */}
            <div className="mode-toggle-group">
              <button 
                type="button"
                className={`mode-toggle-btn ${viewMode === 'wizard' ? 'active' : ''}`}
                onClick={() => setViewMode('wizard')}
              >
                <Sparkles size={15} />
                <span>Guided Wizard</span>
              </button>
              <button 
                type="button"
                className={`mode-toggle-btn ${viewMode === 'chat' ? 'active' : ''}`}
                onClick={() => setViewMode('chat')}
              >
                <MessageSquare size={15} />
                <span>Expert Chat</span>
              </button>
            </div>

            <div className="status-pill">
              <div className="status-indicator"></div>
              {jurisdiction === 'india' ? '27k India Corpus' : '9k Global Corpus'}
            </div>
          </div>
        </header>

        {/* View Mode: Interactive Wizard */}
        {viewMode === 'wizard' && (
          <div className="messages-area" style={{ paddingBottom: '3rem' }}>
            <IntakeWizard 
              onSubmit={handleWizardSubmit} 
              jurisdiction={jurisdiction}
              onJurisdictionChange={setJurisdiction}
              isLoading={isLoading} 
            />
          </div>
        )}

        {/* View Mode: Expert Chat Feed */}
        {viewMode === 'chat' && (
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
                    <Search size={14} className="animate-spin" style={{ animation: 'spin 2s linear infinite' }} /> Querying {jurisdiction === 'india' ? '27,000+ Indian' : '8,800+ Global'} Legal Records...
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} style={{ height: '40px' }} />
          </div>
        )}

        {/* Fixed Floating Input Bar (Active in Direct Chat mode) */}
        {viewMode === 'chat' && (
          <form id="chat-form" className="input-container" onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={`Inquire on ${jurisdiction === 'india' ? 'Indian (AYUSH/IPO)' : 'International (WIPO/PCT)'} formulations & claims...`}
              disabled={isLoading}
            />
            <button type="submit" className="send-btn" disabled={!input.trim() || isLoading}>
              <ChevronRight size={24} />
            </button>
          </form>
        )}
      </main>
    </div>
  );
}
