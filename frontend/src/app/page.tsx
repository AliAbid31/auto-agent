"use client";

import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { Send, Car, Sparkles, RefreshCw, User } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  toolsUsed?: string[];
}

export default function AutoChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll vers le dernier message
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;
    const userQuery = input.trim();
    setInput("");

    setMessages((prev) => [...prev, { role: "user", content: userQuery }]);
    setLoading(true);

    try {
      const backUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      const response = await fetch(`${backUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message: userQuery,
          history: messages.slice(-4) }),
        });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      };
      const data = await response.json();

      setMessages((prev) => [...prev, { role: "assistant", content: data.response, toolsUsed: data.tools_used }]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, an error occurred while sending the message." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-neutral-950 text-neutral-100 flex-col items-center">
      <header className="w-full max-w-4xl p-4 border-b border-neutral-800 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-red-600 flex items-center justify-center font-bold shadow-lg shadow-red-900/30">
            <Car className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-semibold text-base tracking-wide">AutoExpert RAG</h1>
            <p className="text-xs text-neutral-400">Histoire Automobile & Veille Web Tavily</p>
          </div>
        </div>
        <button
          onClick={() => setMessages([])}
          className="flex items-center gap-1.5 text-xs text-neutral-400 hover:text-neutral-200 border border-neutral-800 px-3 py-1.5 rounded-lg transition"
        >
          <RefreshCw className="w-3.5 h-3.5" /> Réinitialiser
        </button>
      </header>

      <div className="flex-1 w-full max-w-4xl overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="text-center py-16 space-y-4">
            <div className="w-16 h-16 bg-neutral-900 border border-neutral-800 rounded-2xl flex items-center justify-center mx-auto text-red-500">
              <Sparkles className="w-8 h-8" />
            </div>
            <h2 className="text-lg font-medium">Posez votre question sur l&apos;automobile</h2>
            <p className="text-sm text-neutral-400 max-w-md mx-auto">
              Je réponds à partir de mes <strong className="text-neutral-200">archives locales</strong> ou je cherche sur le <strong className="text-neutral-200">Web en direct</strong> si nécessaire.
            </p>

            <div className="flex flex-wrap gap-2 justify-center pt-2 max-w-xl mx-auto">
              {[
                "D'où vient le cheval cabré de Ferrari ?",
                "Qui a inventé la ceinture à 3 points ?",
                "Quel est le prix actuel d'une Tesla Model 3 ?",
                "Pourquoi la Porsche 911 s'appelait-elle 901 au départ ?",
              ].map((q, i) => (
                <button
                  key={i}
                  onClick={() => setInput(q)}
                  className="text-xs bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 px-3 py-2 rounded-full transition text-neutral-300 text-left"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-3 max-w-[85%] ${
              m.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            }`}
          >
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                m.role === "user" ? "bg-red-600" : "bg-neutral-800"
              }`}
            >
              {m.role === "user" ? <User className="w-4 h-4" /> : <Car className="w-4 h-4" />}
            </div>

            <div className="space-y-2">
              <div
                className={`p-4 rounded-2xl text-sm leading-relaxed ${
                  m.role === "user"
                    ? "bg-red-600 text-white"
                    : "bg-neutral-900 border border-neutral-800 text-neutral-200"
                }`}
              >
                <div className="prose prose-invert text-sm max-w-none">
                  <ReactMarkdown>{m.content}</ReactMarkdown>
                </div>
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 max-w-[80%]">
            <div className="w-8 h-8 rounded-lg bg-neutral-800 flex items-center justify-center">
              <Car className="w-4 h-4 text-neutral-400 animate-pulse" />
            </div>
            <div className="p-3.5 rounded-2xl bg-neutral-900 border border-neutral-800 flex items-center gap-2 text-xs text-neutral-400">
              <div className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
              Réflexion de l `&apos;` Agent et consultation des outils...
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      {/* Saisie */}
      <footer className="w-full max-w-4xl p-4 border-t border-neutral-800">
        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question sur l'automobile..."
            className="flex-1 bg-neutral-900 border border-neutral-800 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-red-500 transition text-neutral-100 placeholder-neutral-500"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-red-600 hover:bg-red-500 disabled:opacity-40 text-white px-5 rounded-xl flex items-center justify-center transition"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </footer>
    </div>
  );
}