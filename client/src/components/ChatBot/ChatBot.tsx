'use client';

import { useState, useEffect, useRef } from 'react';
import { generateVideo, getVideoStatus } from '@/services/videoService';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  videoTaskId?: string;
  videoStatus?: 'processing' | 'completed' | 'failed';
  videoUrl?: string;
  error?: string;
}

const ChatBot = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Hello! I can generate videos based on your prompts. What would you like to see?',
      sender: 'bot',
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Poll for video generation status updates
  useEffect(() => {
    const pendingMessages = messages.filter(
      (msg) => msg.videoTaskId && msg.videoStatus === 'processing'
    );

    if (pendingMessages.length === 0) return;

    const intervalIds: NodeJS.Timeout[] = [];

    pendingMessages.forEach((message) => {
      const intervalId = setInterval(async () => {
        try {
          const status = await getVideoStatus(message.videoTaskId!);
          
          if (status.status !== 'processing') {
            clearInterval(intervalId);
            
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === message.id
                  ? {
                      ...msg,
                      videoStatus: status.status,
                      videoUrl: status.video_url,
                      error: status.error,
                    }
                  : msg
              )
            );
          }
        } catch (error) {
          console.error('Error checking video status:', error);
        }
      }, 2000);

      intervalIds.push(intervalId);
    });

    return () => {
      intervalIds.forEach((id) => clearInterval(id));
    };
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Add bot response with loading state
      const botMessageId = (Date.now() + 1).toString();
      const botMessage: Message = {
        id: botMessageId,
        text: "I'll generate a video for you based on your prompt...",
        sender: 'bot',
      };

      setMessages((prev) => [...prev, botMessage]);

      // Start video generation
      const response = await generateVideo(text);
      
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === botMessageId
            ? {
                ...msg,
                text: `I'm generating your video. This might take a moment...`,
                videoTaskId: response.task_id,
                videoStatus: 'processing',
              }
            : msg
        )
      );
    } catch (error) {
      console.error('Error generating video:', error);
      
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          text: 'Sorry, there was an error generating your video. Please try again.',
          sender: 'bot',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[70vh] bg-gray-50 rounded-lg shadow-lg overflow-hidden">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatBot;
