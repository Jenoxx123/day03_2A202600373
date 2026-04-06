import React, { useState, useMemo } from 'react';
import './ReportApp.css';

const GROUP_SAMPLE = `{
  "title": "Lab 3 - Production-Grade Agentic System",
  "teamName": "Aurora Agents",
  "teamMembers": ["Nina Park", "Ravi Patel", "Kim Lee", "Alex Morgan"],
  "deploymentDate": "2026-03-28",
  "executiveSummary": "Built a robust ReAct agent that significantly outperforms the baseline chatbot on multi-step reasoning tasks by properly leveraging tools.",
  "successRate": "85%",
  "keyOutcome": "Our agent solved 40% more multi-step queries than the chatbot baseline by correctly utilizing the Search tool.",
  "reactLoop": "The agent follows a classic ReAct loop: Thought → Action (tool call) → Observation → Repeat until final answer.",
  "tools": [
    { "name": "calc_tax", "inputFormat": "json", "useCase": "Calculate VAT based on country code" },
    { "name": "search_api", "inputFormat": "string", "useCase": "Retrieve real-time information from Google Search" },
    { "name": "web_browser", "inputFormat": "string", "useCase": "Navigate and extract content from specific URLs" }
  ],
  "llmPrimary": "GPT-4o",
  "llmSecondary": "Gemini 1.5 Flash",
  "telemetry": {
    "avgLatencyP50": "1200ms",
    "maxLatencyP99": "4500ms",
    "avgTokensPerTask": "350",
    "totalCost": "$0.05"
  },
  "rcaCases": [
    {
      "title": "Hallucinated Argument in calc_tax",
      "input": "How much is the tax for 500 in Vietnam?",
      "observation": "Agent called calc_tax(amount=500, region=\\\"Asia\\\")",
      "rootCause": "The system prompt lacked enough Few-Shot examples for the tool's strict 2-letter country code format."
    }
  ],
  "experiments": [
    {
      "title": "Prompt v1 vs Prompt v2",
      "diff": "Added instruction: 'Always double check the tool arguments before calling'",
      "result": "Reduced invalid tool call errors by 30%"
    }
  ],
  "ablationTable": [
    { "case": "Simple Q", "chatbot": "Correct", "agent": "Correct", "winner": "Draw" },
    { "case": "Multi-step", "chatbot": "Hallucinated", "agent": "Correct", "winner": "Agent" }
  ],
  "productionReadiness": {
    "security": "Input sanitization for tool arguments and rate limiting on external APIs.",
    "guardrails": "Max 8 ReAct loops + timeout to prevent infinite loops and excessive billing.",
    "scaling": "Ready to migrate to LangGraph for better state management and complex branching."
  }
}`;

function ReportApp() {
  const [activeTab, setActiveTab] = useState('overview');

  const data = useMemo(() => {
    try {
      return JSON.parse(GROUP_SAMPLE);
    } catch (error) {
      console.error("Failed to parse GROUP_SAMPLE:", error);
      return null;
    }
  }, []);

  const handleTabChange = (tab) => {
    console.log(`Tab clicked: ${tab}`);   // ← You should see this in console now
    setActiveTab(tab);
  };

  if (!data) {
    return <div className="error-state">Error loading report data.</div>;
  }

  return (
    <div className="report-app">
      <div className="report-bg" />

      <header className="hero">
        <div>
          <p className="eyebrow">Group Lab Report</p>
          <h1>{data.title}</h1>
          <p className="subtitle">Production-Grade Agentic System</p>
        </div>
      </header>

      <main className="report-container">
        <section className="report-meta">
          <div className="meta-grid">
            <p><strong>Team:</strong> {data.teamName}</p>
            <p><strong>Members:</strong> {data.teamMembers?.join(', ')}</p>
            <p><strong>Deployment Date:</strong> {data.deploymentDate}</p>
          </div>
        </section>

        <div className="tabs">
          <button 
            className={activeTab === 'overview' ? 'active' : ''}
            onClick={() => handleTabChange('overview')}
          >
            Overview
          </button>
          <button 
            className={activeTab === 'architecture' ? 'active' : ''}
            onClick={() => handleTabChange('architecture')}
          >
            Architecture & Tooling
          </button>
          <button 
            className={activeTab === 'analysis' ? 'active' : ''}
            onClick={() => handleTabChange('analysis')}
          >
            Analysis & Experiments
          </button>
          <button 
            className={activeTab === 'readiness' ? 'active' : ''}
            onClick={() => handleTabChange('readiness')}
          >
            Production Readiness
          </button>
        </div>

        <div className="report-body">
          {activeTab === 'overview' && (
            <>
              <div className="summary-card">
                <h4>1. Executive Summary</h4>
                <p>{data.executiveSummary}</p>
              </div>
              <div className="stat-grid">
                <div className="stat-card">
                  <p className="stat-label">Success Rate</p>
                  <p className="stat-value big">{data.successRate}</p>
                </div>
                <div className="stat-card">
                  <p className="stat-label">Key Outcome</p>
                  <p className="stat-value outcome">{data.keyOutcome}</p>
                </div>
              </div>
            </>
          )}

          {activeTab === 'architecture' && (
            <>
              <div className="list-card">
                <h4>2.1 ReAct Loop Implementation</h4>
                <p>{data.reactLoop}</p>
              </div>

              <div className="list-card">
                <h4>2.2 Tool Definitions (Inventory)</h4>
                <table className="tool-table">
                  <thead>
                    <tr>
                      <th>Tool Name</th>
                      <th>Input Format</th>
                      <th>Use Case</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(data.tools || []).map((tool, i) => (
                      <tr key={i}>
                        <td><code>{tool.name}</code></td>
                        <td>{tool.inputFormat}</td>
                        <td>{tool.useCase}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="list-card">
                <h4>2.3 LLM Providers Used</h4>
                <p><strong>Primary:</strong> {data.llmPrimary}</p>
                {data.llmSecondary && <p><strong>Secondary:</strong> {data.llmSecondary}</p>}
              </div>

              <div className="list-card">
                <h4>3. Telemetry & Performance Dashboard</h4>
                <div className="stat-grid">
                  <div className="stat-card"><p className="stat-label">Avg Latency (P50)</p><p className="stat-value">{data.telemetry?.avgLatencyP50}</p></div>
                  <div className="stat-card"><p className="stat-label">Max Latency (P99)</p><p className="stat-value">{data.telemetry?.maxLatencyP99}</p></div>
                  <div className="stat-card"><p className="stat-label">Avg Tokens per Task</p><p className="stat-value">{data.telemetry?.avgTokensPerTask}</p></div>
                  <div className="stat-card"><p className="stat-label">Total Cost</p><p className="stat-value">{data.telemetry?.totalCost}</p></div>
                </div>
              </div>
            </>
          )}

          {activeTab === 'analysis' && (
            <>
              <div className="list-card">
                <h4>4. Root Cause Analysis (RCA)</h4>
                {(data.rcaCases || []).map((rca, i) => (
                  <div key={i} className="rca-card">
                    <h5>Case Study: {rca.title}</h5>
                    <p><strong>Input:</strong> "{rca.input}"</p>
                    <p><strong>Observation:</strong> {rca.observation}</p>
                    <p><strong>Root Cause:</strong> {rca.rootCause}</p>
                  </div>
                ))}
              </div>

              <div className="list-card">
                <h4>5. Ablation Studies & Experiments</h4>
                {(data.experiments || []).map((exp, i) => (
                  <div key={i} className="experiment-card">
                    <h5>{exp.title}</h5>
                    <p><strong>Change:</strong> {exp.diff}</p>
                    <p><strong>Result:</strong> {exp.result}</p>
                  </div>
                ))}

                {data.ablationTable && (
                  <div className="list-card">
                    <h5>Chatbot vs Agent Comparison</h5>
                    <table className="tool-table">
                      <thead>
                        <tr>
                          <th>Case</th>
                          <th>Chatbot</th>
                          <th>Agent</th>
                          <th>Winner</th>
                        </tr>
                      </thead>
                      <tbody>
                        {data.ablationTable.map((row, i) => (
                          <tr key={i}>
                            <td>{row.case}</td>
                            <td>{row.chatbot}</td>
                            <td>{row.agent}</td>
                            <td><strong>{row.winner}</strong></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </>
          )}

          {activeTab === 'readiness' && (
            <div className="list-card">
              <h4>6. Production Readiness Review</h4>
              <div className="readiness-grid">
                <div className="readiness-item">
                  <strong>Security</strong>
                  <p>{data.productionReadiness?.security}</p>
                </div>
                <div className="readiness-item">
                  <strong>Guardrails</strong>
                  <p>{data.productionReadiness?.guardrails}</p>
                </div>
                <div className="readiness-item">
                  <strong>Scaling</strong>
                  <p>{data.productionReadiness?.scaling}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default ReportApp;