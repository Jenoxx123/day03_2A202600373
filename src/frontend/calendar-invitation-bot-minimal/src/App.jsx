import React, { useState } from 'react';
import ChatbotInterface from './components/ChatbotInterface';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "👋 Xin chào! Tôi là trợ lý đặt lịch họp của bạn. Hãy cho tôi biết bạn muốn đặt lịch với ai, vào thời gian nào nhé!",
    }
  ]);

  const [awaitingResponse, setAwaitingResponse] = useState(false);

  const handleSendMessage = async (userMessage) => {
    // Add user message
    const newUserMessage = {
      id: Date.now(),
      type: 'user',
      text: userMessage,
    };

    setMessages(prev => [...prev, newUserMessage]);
    setAwaitingResponse(true);

    try {
      const history = messages.map((msg) => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.text,
      }));

      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          history,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Backend request failed');
      }

      const data = await response.json();
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        text: data.reply || 'I did not get a response. Please try again.',
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        text: `Xin lỗi, tôi gặp sự cố khi xử lý yêu cầu của bạn. ${error?.message || 'Vui lòng thử lại sau.'}`.trim(),
      };
      setMessages(prev => [...prev, botResponse]);
    } finally {
      setAwaitingResponse(false);
    }
  };

  return (
    <div className="app-container">
      <div className="app-content">
        <ChatbotInterface
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={awaitingResponse}
        />
      </div>
    </div>
  );
}

export default App;
