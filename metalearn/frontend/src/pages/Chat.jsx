import { useState, useRef, useEffect } from 'react'
import { chat } from '../services/api'

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Halo! 👋 Aku MetaLearn AI, asisten belajarmu. Tanyakan apa pun tentang pelajaran, tugas, atau topik yang ingin kamu pelajari!' },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setLoading(true)
    try {
      const { data } = await chat.send({ message: text, session_id: sessionId })
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }])
      if (data.session_id) setSessionId(data.session_id)
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Maaf, terjadi kesalahan. Coba lagi ya!' }])
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    if (!sessionId) {
      setMessages([
        { role: 'assistant', content: 'Halo! 👋 Aku MetaLearn AI, asisten belajarmu. Tanyakan apa pun tentang pelajaran, tugas, atau topik yang ingin kamu pelajari!' },
      ])
      return
    }
    try {
      await chat.reset({ session_id: sessionId })
    } catch {
      // ignore
    }
    setSessionId(null)
    setMessages([
      { role: 'assistant', content: 'Percakapan direset! 🆕 Ada yang ingin kamu tanyakan?' },
    ])
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="max-w-3xl mx-auto flex flex-col h-[calc(100vh-12rem)]">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Chat AI</h1>
          <p className="text-sm text-gray-400">Tanya apa saja tentang belajar</p>
        </div>
        <button onClick={handleReset} className="px-3 py-1.5 text-xs rounded-lg glass text-gray-400 hover:text-white hover:bg-white/10 transition flex items-center gap-1.5">
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          Reset
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              msg.role === 'user'
                ? 'bg-indigo-500/20 border border-indigo-500/30 text-white rounded-br-md'
                : 'glass text-gray-200 rounded-bl-md'
            }`}>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="glass rounded-2xl rounded-bl-md px-4 py-3">
              <div className="flex gap-1.5">
                <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="mt-4 glass-strong rounded-2xl p-2 flex items-end gap-2 border border-white/10">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ketik pesan..."
          rows={1}
          className="flex-1 bg-transparent text-white placeholder-gray-500 px-3 py-2 outline-none resize-none text-sm max-h-32"
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || loading}
          className="p-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-400 disabled:opacity-40 disabled:cursor-not-allowed transition text-white flex-shrink-0"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19V5m0 0l-7 7m7-7l7 7" /></svg>
        </button>
      </div>
    </div>
  )
}
