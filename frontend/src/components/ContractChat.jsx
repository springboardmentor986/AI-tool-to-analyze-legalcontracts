import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FiSend, FiMessageCircle, FiX, FiHelpCircle } from 'react-icons/fi';
import { useTranslation } from '../hooks/useTranslation';
import './ContractChat.css';

const ContractChat = ({ contractId, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);
  const { t, language } = useTranslation();

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load suggested questions on mount
  useEffect(() => {
    if (contractId) {
      loadSuggestions();
      // Add welcome message
      setMessages([{
        type: 'bot',
        content: t('chat.welcome', 'Hi! I\'m your contract assistant. Ask me anything about the analyzed contract.'),
        timestamp: new Date()
      }]);
    }
  }, [contractId]);

  const loadSuggestions = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/chat/suggestions/${contractId}`);
      setSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('Error loading suggestions:', error);
    }
  };

  const sendMessage = async (messageText = null) => {
    const question = messageText || inputMessage.trim();
    
    if (!question) return;

    // Add user message to chat
    const userMessage = {
      type: 'user',
      content: question,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      // Send question to backend
      const response = await axios.post('http://localhost:8000/chat', {
        contract_id: contractId,
        question: question,
        language: language
      });

      // Add bot response
      const botMessage = {
        type: 'bot',
        content: response.data.answer,
        sources: response.data.sources,
        confidence: response.data.confidence,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        type: 'bot',
        content: t('chat.error', 'Sorry, I encountered an error. Please try again.'),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const getConfidenceBadge = (confidence) => {
    const badges = {
      'high': { text: t('chat.confidence.high', 'High'), class: 'confidence-high' },
      'medium': { text: t('chat.confidence.medium', 'Medium'), class: 'confidence-medium' },
      'low': { text: t('chat.confidence.low', 'Low'), class: 'confidence-low' }
    };
    return badges[confidence] || badges.medium;
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-header-content">
          <FiMessageCircle className="chat-icon" />
          <div>
            <h3>{t('chat.title', 'Contract Assistant')}</h3>
            <p>{t('chat.subtitle', 'Ask questions about your contract')}</p>
          </div>
        </div>
        <button className="chat-close-btn" onClick={onClose}>
          <FiX />
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.type}`}>
            <div className="message-content">
              <p>{msg.content}</p>
              {msg.sources && msg.sources.length > 0 && (
                <div className="message-sources">
                  <small>📚 {t('chat.sources', 'Sources')}: {msg.sources.join(', ')}</small>
                </div>
              )}
              {msg.confidence && (
                <div className={`message-confidence ${getConfidenceBadge(msg.confidence).class}`}>
                  <small>✓ {getConfidenceBadge(msg.confidence).text} {t('chat.confidence.label', 'Confidence')}</small>
                </div>
              )}
            </div>
            <div className="message-timestamp">
              {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message bot">
            <div className="message-content typing">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {suggestions.length > 0 && messages.length <= 1 && (
        <div className="chat-suggestions">
          <div className="suggestions-header">
            <FiHelpCircle />
            <span>{t('chat.suggestedQuestions', 'Suggested Questions')}</span>
          </div>
          <div className="suggestions-list">
            {suggestions.map((suggestion, idx) => (
              <button
                key={idx}
                className="suggestion-btn"
                onClick={() => handleSuggestionClick(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="chat-input-container">
        <textarea
          className="chat-input"
          placeholder={t('chat.placeholder', 'Ask a question about the contract...')}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          rows="2"
          disabled={loading}
        />
        <button
          className="chat-send-btn"
          onClick={() => sendMessage()}
          disabled={loading || !inputMessage.trim()}
        >
          <FiSend />
        </button>
      </div>
    </div>
  );
};

export default ContractChat;
