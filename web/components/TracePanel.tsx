import { TraceSpan } from "@/lib/api";

export function TracePanel({ trace }: { trace: TraceSpan[] }) {
  if (!trace?.length)
    return <p className="text-sm text-slate-500">Run a query to see the agent trajectory.</p>;
  const max = Math.max(...trace.map((s) => s.duration_ms), 1);
  return (
    <div className="space-y-2">
      {trace.map((s, i) => (
        <div key={i} className="text-sm">
          <div className="flex items-center justify-between">
            <span className="font-mono text-slate-200">{s.name}</span>
            <span className="text-slate-400">{s.duration_ms.toFixed(1)}ms</span>
          </div>
          <div className="mt-1 h-1.5 w-full rounded-full bg-edge/50">
            <div
              className="h-1.5 rounded-full bg-brand"
              style={{ width: `${Math.max((s.duration_ms / max) * 100, 3)}%` }}
            />
          </div>
          {s.attributes && Object.keys(s.attributes).length > 0 && (
            <div className="mt-1 flex flex-wrap gap-1">
              {Object.entries(s.attributes)
                .slice(0, 4)
                .map(([k, v]) => (
                  <span key={k} className="tag">
                    {k}: {String(v).slice(0, 24)}
                  </span>
                ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
