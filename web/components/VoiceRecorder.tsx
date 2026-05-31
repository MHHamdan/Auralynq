"use client";
import { useRef, useState } from "react";
import { audioUrl, sendVoice } from "@/lib/api";

export function VoiceRecorder({ onResult }: { onResult: (r: any) => void }) {
  const [recording, setRecording] = useState(false);
  const [busy, setBusy] = useState(false);
  const [partial, setPartial] = useState("");
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  async function start() {
    setPartial("");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(stream);
    chunksRef.current = [];
    rec.ondataavailable = (e) => e.data.size > 0 && chunksRef.current.push(e.data);
    rec.onstop = async () => {
      stream.getTracks().forEach((t) => t.stop());
      setBusy(true);
      try {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const r = await sendVoice(blob);
        setPartial(r.transcript || "");
        onResult(r);
        const a = new Audio(audioUrl());
        a.play().catch(() => {});
      } catch (err) {
        onResult({ answer: `Voice error: ${(err as Error).message}`, citations: [] });
      } finally {
        setBusy(false);
      }
    };
    rec.start();
    recorderRef.current = rec;
    setRecording(true);
  }

  function stop() {
    recorderRef.current?.stop();
    setRecording(false);
  }

  return (
    <div className="flex items-center gap-3">
      <button
        className={recording ? "btn bg-rose-500 text-white" : "btn-brand"}
        onMouseDown={start}
        onMouseUp={stop}
        onTouchStart={start}
        onTouchEnd={stop}
        disabled={busy}
      >
        {busy ? "Thinking…" : recording ? "● Recording — release to send" : "🎙 Push to talk"}
      </button>
      {recording && (
        <span className="flex items-center gap-1">
          {[0, 1, 2, 3].map((i) => (
            <span
              key={i}
              className="inline-block w-1.5 rounded-full bg-brand animate-pulse"
              style={{ height: `${8 + ((i * 7) % 18)}px`, animationDelay: `${i * 120}ms` }}
            />
          ))}
        </span>
      )}
      {partial && <span className="text-sm text-slate-400">“{partial}”</span>}
    </div>
  );
}
