import React, { useState, useRef, useEffect } from 'react';
import { ChatIcon } from './ChatIcon';
import './styles.css';

const API_URL = 'http://localhost:8000/chat';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    const handleMouseUp = () => {
      const selection = window.getSelection().toString().trim();
      if (selection) {
        setSelectedText(selection);
        setIsOpen(true);
      }
    };
    document.addEventListener('mouseup', handleMouseUp);
    return () => document.removeEventListener('mouseup', handleMouseUp);
  }, []);

  const handleSendMessage = async () => {
    if (input.trim() === '' || isLoading) return;

    const userMessage = { type: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, selected_text: selectedText }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      const botMessage = { type: 'bot', text: data.answer, sources: data.sources };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { type: 'bot', text: 'Sorry, something went wrong. Please try again.' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText(null); // Clear selection after sending
    }
  };

  return (
    <div className="chat-widget-container">
      <div className={`chat-window ${!isOpen ? 'hidden' : ''}`}>
        <div className="chat-header">Ask me about the book!</div>
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              <p>{msg.text}</p>
              {msg.type === 'bot' && msg.sources && msg.sources.length > 0 && (
                <div className="message-sources">
                  <strong>Sources:</strong> {msg.sources.join(', ')}
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        {selectedText && (
          <div className="selected-text-context">
            <p><strong>Answering about:</strong> "{selectedText}"</p>
            <button onClick={() => setSelectedText(null)}>X</button>
          </div>
        )}
        <div className="chat-input-area">
          <input
            type="text"
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your question..."
            disabled={isLoading}
          />
          <button onClick={handleSendMessage} className="send-button" disabled={isLoading}>
            {isLoading ? '...' : 'Send'}
          </button>
        </div>
      </div>
      <button className="chat-toggle-button" onClick={() => setIsOpen(!isOpen)}>
        <ChatIcon />
      </button>
    </div>
  );
}
