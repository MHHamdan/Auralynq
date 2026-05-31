"use client";
import { useState } from "react";
import { ingestFile } from "@/lib/api";

export function IngestPanel() {
  const [status, setStatus] = useState<string>("");
  const [busy, setBusy] = useState(false);

  async function onUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setBusy(true);
    setStatus(`Uploading ${file.name} …`);
    try {
      const r = await ingestFile(file);
      setStatus(`✓ Indexed ${r.documents} document(s), ${r.chunks} chunk(s).`);
    } catch (err) {
      setStatus(`✗ ${(err as Error).message}`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-400">
        Add PDF, DOCX, HTML, Markdown, TXT or audio (WAV/MP3/M4A). Files are chunked with
        source spans and indexed into the hybrid store + knowledge graph.
      </p>
      <label className="btn-brand cursor-pointer inline-block">
        {busy ? "Working…" : "Upload & index"}
        <input
          type="file"
          className="hidden"
          disabled={busy}
          onChange={onUpload}
          accept=".pdf,.docx,.html,.htm,.md,.txt,.wav,.mp3,.m4a"
        />
      </label>
      {status && <p className="text-sm text-slate-300">{status}</p>}
    </div>
  );
}
