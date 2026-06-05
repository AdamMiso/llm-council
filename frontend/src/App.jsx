import { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import ChatInterface from './components/ChatInterface';
import { api } from './api';
import './App.css';

function App() {
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const loadConversations = useCallback(async () => {
    try {
      const convs = await api.listConversations();
      setConversations(convs);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  }, []);

  const updateLastAssistantMessage = useCallback((updater) => {
    setCurrentConversation((prev) => {
      if (!prev || prev.messages.length === 0) return prev;

      const lastIndex = prev.messages.length - 1;
      const messages = prev.messages.map((message, index) => (
        index === lastIndex ? updater(message) : message
      ));

      return { ...prev, messages };
    });
  }, []);

  // Load conversations on mount
  useEffect(() => {
    let cancelled = false;

    api.listConversations()
      .then((convs) => {
        if (!cancelled) {
          setConversations(convs);
        }
      })
      .catch((error) => {
        console.error('Failed to load conversations:', error);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  // Load conversation details when selected
  useEffect(() => {
    if (!currentConversationId) return undefined;

    let cancelled = false;

    api.getConversation(currentConversationId)
      .then((conv) => {
        if (!cancelled) {
          setCurrentConversation(conv);
        }
      })
      .catch((error) => {
        console.error('Failed to load conversation:', error);
      });

    return () => {
      cancelled = true;
    };
  }, [currentConversationId]);

  const handleNewConversation = async () => {
    try {
      const newConv = await api.createConversation();
      setConversations([
        { id: newConv.id, created_at: newConv.created_at, message_count: 0 },
        ...conversations,
      ]);
      setCurrentConversationId(newConv.id);
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  const handleSelectConversation = (id) => {
    setCurrentConversationId(id);
  };

  const handleSendMessage = async (content) => {
    if (!currentConversationId) return;

    setIsLoading(true);
    try {
      // Optimistically add user message to UI
      const userMessage = { role: 'user', content };
      setCurrentConversation((prev) => ({
        ...prev,
        messages: [...prev.messages, userMessage],
      }));

      // Create a partial assistant message that will be updated progressively
      const assistantMessage = {
        role: 'assistant',
        stage1: null,
        stage2: null,
        stage3: null,
        metadata: null,
        loading: {
          stage1: false,
          stage2: false,
          stage3: false,
        },
      };

      // Add the partial assistant message
      setCurrentConversation((prev) => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
      }));

      // Send message with streaming
      await api.sendMessageStream(currentConversationId, content, (eventType, event) => {
        switch (eventType) {
          case 'stage1_start':
            updateLastAssistantMessage((message) => ({
              ...message,
              loading: { ...message.loading, stage1: true },
            }));
            break;

          case 'stage1_complete':
            updateLastAssistantMessage((message) => ({
              ...message,
              stage1: event.data,
              loading: { ...message.loading, stage1: false },
            }));
            break;

          case 'stage2_start':
            updateLastAssistantMessage((message) => ({
              ...message,
              loading: { ...message.loading, stage2: true },
            }));
            break;

          case 'stage2_complete':
            updateLastAssistantMessage((message) => ({
              ...message,
              stage2: event.data,
              metadata: event.metadata,
              loading: { ...message.loading, stage2: false },
            }));
            break;

          case 'stage3_start':
            updateLastAssistantMessage((message) => ({
              ...message,
              loading: { ...message.loading, stage3: true },
            }));
            break;

          case 'stage3_complete':
            updateLastAssistantMessage((message) => ({
              ...message,
              stage3: event.data,
              loading: { ...message.loading, stage3: false },
            }));
            break;

          case 'title_complete':
            // Reload conversations to get updated title
            loadConversations();
            break;

          case 'complete':
            // Stream complete, reload conversations list
            loadConversations();
            setIsLoading(false);
            break;

          case 'error':
            console.error('Stream error:', event.message);
            setIsLoading(false);
            break;

          default:
            console.log('Unknown event type:', eventType);
        }
      });
    } catch (error) {
      console.error('Failed to send message:', error);
      // Remove optimistic messages on error
      setCurrentConversation((prev) => ({
        ...prev,
        messages: prev.messages.slice(0, -2),
      }));
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
      />
      <ChatInterface
        conversation={currentConversation}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}

export default App;
