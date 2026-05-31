"use client";
import { useEffect, useRef, useState } from "react";
import {
  AnswerResult,
  Citation,
  PathEvidence,
  StreamEvent,
  TraceSpan,
  askStream,
  health,
} from "@/lib/api";
import { Citations } from "@/components/Citations";
import { TracePanel } from "@/components/TracePanel";
import { EvidencePaths } from "@/components/EvidencePaths";
import { IngestPanel } from "@/components/IngestPanel";
import { EvalPanel } from "@/components/EvalPanel";
import { VoiceRecorder } from "@/components/VoiceRecorder";

interface Turn {
  role: "user" | "assistant";
  text: string;
  citations?: Citation[];
  route?: string;
  rationale?: string;
}

const SUGGESTIONS = [
  "What is the capital of France?",
  "How does PathRAG prune relational paths?",
  "How are Paris, France and Europe related?",
];

export default function Home() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [trace, setTrace] = useState<TraceSpan[]>([]);
  const [paths, setPaths] = useState<PathEvidence[]>([]);
  const [seeds, setSeeds] = useState<string[]>([]);
  const [tab, setTab] = useState<"trace" | "evidence" | "ingest" | "eval">("trace");
  const [providers, setProviders] = useState<{ subsystem: string; provider: string }[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    health()
      .then((h) => setProviders(h.providers || []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [turns]);

  async function send(q: string) {
    if (!q.trim() || streaming) return;
    setInput("");
    setTurns((t) => [...t, { role: "user", text: q }, { role: "assistant", text: "" }]);
    setStreaming(true);
    setTrace([]);
    setPaths([]);
    setSeeds([]);
    try {
      await askStream(q, (e: StreamEvent) => {
        if (e.type === "meta") {
          setPaths(e.path_evidence || []);
          setSeeds(e.seeds || []);
          setTab(e.route === "fast" ? "trace" : "evidence");
          setTurns((t) => {
            const c = [...t];
            c[c.length - 1] = { ...c[c.length - 1], route: e.route, rationale: e.rationale };
            return c;
          });
        } else if (e.type === "token") {
          setTurns((t) => {
            const c = [...t];
            c[c.length - 1] = { ...c[c.length - 1], text: c[c.length - 1].text + e.text };
            return c;
          });
        } else if (e.type === "final") {
          setTrace(e.trace || []);
          setTurns((t) => {
            const c = [...t];
            c[c.length - 1] = { ...c[c.length - 1], text: e.answer, citations: e.citations };
            return c;
          });
        }
      });
    } catch (err) {
      setTurns((t) => {
        const c = [...t];
        c[c.length - 1] = { ...c[c.length - 1], text: `Error: ${(err as Error).message}` };
        return c;
      });
    } finally {
      setStreaming(false);
    }
  }

  function onVoice(r: AnswerResult & { transcript?: string }) {
    const q = r.transcript || "voice query";
    setTurns((t) => [
      ...t,
      { role: "user", text: `🎙 ${q}` },
      { role: "assistant", text: r.answer, citations: r.citations, route: r.route },
    ]);
    setPaths(r.path_evidence || []);
    if (r.trace) setTrace(r.trace);
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-4 p-4 md:p-6">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">
            🎙️ <span className="text-brand">Aura</span>
            <span className="text-brand2">lynq</span>
          </h1>
          <p className="text-sm text-slate-400">Talk to Your Data — agentic voice RAG · PathRAG</p>
        </div>
        <div className="flex flex-wrap gap-1">
          {providers.map((p) => (
            <span key={p.subsystem} className="tag">
              {p.subsystem}: <span className="text-brand">{p.provider}</span>
            </span>
          ))}
        </div>
      </header>

      <div className="grid flex-1 gap-4 lg:grid-cols-[1.4fr_1fr]">
        {/* Chat column */}
        <section className="card flex min-h-[60vh] flex-col">
          <div ref={scrollRef} className="scroll-thin flex-1 space-y-3 overflow-y-auto pr-1">
            {turns.length === 0 && (
              <div className="flex h-full flex-col items-center justify-center gap-3 text-center">
                <p className="text-slate-400">Ask a question — by text or voice.</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {SUGGESTIONS.map((s) => (
                    <button key={s} className="btn-ghost text-sm" onClick={() => send(s)}>
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}
            {turns.map((t, i) => (
              <div
                key={i}
                className={t.role === "user" ? "flex justify-end" : "flex justify-start"}
              >
                <div
                  className={
                    t.role === "user"
                      ? "max-w-[85%] rounded-2xl bg-brand2/20 px-4 py-2"
                      : "max-w-[90%] rounded-2xl border border-edge bg-ink/50 px-4 py-3"
                  }
                >
                  {t.role === "assistant" && t.route && (
                    <div className="mb-1 flex items-center gap-2 text-xs">
                      <span className="tag border-brand/40 text-brand">route: {t.route}</span>
                      {t.rationale && <span className="text-slate-500">{t.rationale}</span>}
                    </div>
                  )}
                  <p className="whitespace-pre-wrap leading-relaxed">
                    {t.text || (streaming && i === turns.length - 1 ? "▍" : "")}
                  </p>
                  {t.citations && <Citations citations={t.citations} />}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-3 space-y-2 border-t border-edge pt-3">
            <VoiceRecorder onResult={onVoice} />
            <form
              className="flex gap-2"
              onSubmit={(e) => {
                e.preventDefault();
                send(input);
              }}
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask Auralynq…"
                className="flex-1 rounded-xl border border-edge bg-ink/60 px-4 py-2 outline-none focus:border-brand"
              />
              <button className="btn-brand" disabled={streaming}>
                {streaming ? "…" : "Ask"}
              </button>
            </form>
          </div>
        </section>

        {/* Side panel */}
        <section className="card flex flex-col">
          <div className="mb-3 flex gap-1 text-sm">
            {(["trace", "evidence", "ingest", "eval"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`rounded-lg px-3 py-1 capitalize ${
                  tab === t ? "bg-brand text-ink" : "border border-edge"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
          <div className="scroll-thin flex-1 overflow-y-auto">
            {tab === "trace" && <TracePanel trace={trace} />}
            {tab === "evidence" && <EvidencePaths paths={paths} seeds={seeds} />}
            {tab === "ingest" && <IngestPanel />}
            {tab === "eval" && <EvalPanel />}
          </div>
        </section>
      </div>

      <footer className="text-center text-xs text-slate-500">
        Auralynq · local-first · $0 default · grounded answers with citations, spans &amp;
        timestamps
      </footer>
    </main>
  );
}
