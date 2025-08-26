import Image from "next/image";
import ChatBot from "../components/ChatBot/ChatBot";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4 sm:p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm">
        <h1 className="text-3xl font-bold text-center mb-8">Video Generation Chatbot</h1>
        <ChatBot />
      </div>
    </main>
  );
}
