"use client";
import { useState } from "react";
import { evalReport } from "@/lib/api";

export function EvalPanel() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);
    try {
      setReport(await evalReport());
    } finally {
      setLoading(false);
    }
  }

  const variants = report?.retrieval
    ? Object.entries(report.retrieval as Record<string, any>)
    : [];

  return (
    <div className="space-y-3">
      <button className="btn-ghost" onClick={load} disabled={loading}>
        {loading ? "Loading…" : "Load eval report"}
      </button>
      {report?.status === "pending" && (
        <p className="text-sm text-slate-400">
          No report yet — run <code className="text-brand">make eval</code>.
        </p>
      )}
      {variants.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-slate-400">
              <tr>
                <th className="text-left">retriever</th>
                <th>recall@k</th>
                <th>nDCG@10</th>
                <th>MRR</th>
                <th>p50 ms</th>
              </tr>
            </thead>
            <tbody>
              {variants.map(([name, m]) => (
                <tr key={name} className="border-t border-edge">
                  <td className="py-1 text-slate-200">{name}</td>
                  <td className="text-center">{m.recall_at_k}</td>
                  <td className="text-center">{m.ndcg_at_10}</td>
                  <td className="text-center">{m.mrr}</td>
                  <td className="text-center">{m.latency_p50_ms}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {report?.agentic?.ragas && (
            <p className="mt-2 text-xs text-slate-400">
              Ragas ({report.agentic.ragas.provider}): faithfulness{" "}
              {report.agentic.ragas.faithfulness} · relevancy{" "}
              {report.agentic.ragas.answer_relevancy} · ctx-precision{" "}
              {report.agentic.ragas.context_precision}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
