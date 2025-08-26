'use client';

import { getVideoUrl } from '@/services/videoService';
import Image from 'next/image';

interface MessageProps {
  message: {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    videoTaskId?: string;
    videoStatus?: 'processing' | 'completed' | 'failed';
    videoUrl?: string;
    error?: string;
  };
}

const ChatMessage = ({ message }: MessageProps) => {
  const isBot = message.sender === 'bot';
  
  return (
    <div
      className={`flex mb-4 ${
        isBot ? 'justify-start' : 'justify-end'
      } items-start`}
    >
      {isBot && (
        <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center mr-2 flex-shrink-0">
          <span className="text-white text-sm">🤖</span>
        </div>
      )}
      
      <div
        className={`max-w-[70%] rounded-lg p-3 ${
          isBot
            ? 'bg-white border border-gray-200'
            : 'bg-blue-500 text-white'
        }`}
      >
        <p className="text-sm">{message.text}</p>
        
        {message.videoStatus === 'processing' && (
          <div className="mt-2 flex items-center space-x-2">
            <div className="animate-spin h-4 w-4 border-2 border-blue-500 rounded-full border-t-transparent"></div>
            <span className="text-xs text-gray-500">Generating video...</span>
          </div>
        )}
        
        {message.videoStatus === 'completed' && message.videoUrl && (
          <div className="mt-2">
            <video
              src={getVideoUrl(message.videoTaskId!)}
              controls
              className="w-full h-auto rounded mt-2 shadow-sm"
            >
              Your browser does not support the video tag.
            </video>
          </div>
        )}
        
        {message.videoStatus === 'failed' && (
          <div className="mt-2 text-xs text-red-500">
            {message.error || 'Failed to generate video. Please try again.'}
          </div>
        )}
      </div>
      
      {!isBot && (
        <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center ml-2 flex-shrink-0">
          <span className="text-white text-sm">👤</span>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
