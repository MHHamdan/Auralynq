import { PathEvidence } from "@/lib/api";

export function EvidencePaths({ paths, seeds }: { paths: PathEvidence[]; seeds: string[] }) {
  if (!paths?.length)
    return (
      <p className="text-sm text-slate-500">
        PathRAG evidence paths appear here for relational / multi-hop questions.
      </p>
    );
  return (
    <div className="space-y-3">
      {seeds?.length > 0 && (
        <div className="flex flex-wrap gap-1">
          <span className="text-xs text-slate-400">seeds:</span>
          {seeds.map((s) => (
            <span key={s} className="tag border-brand2/40 text-brand2">
              {s}
            </span>
          ))}
        </div>
      )}
      {paths.map((p, i) => (
        <div key={i} className="rounded-xl border border-edge bg-ink/40 p-2">
          <div className="flex flex-wrap items-center gap-1 text-sm">
            {p.nodes.map((n, j) => (
              <span key={j} className="flex items-center gap-1">
                <span className="rounded-md bg-edge/60 px-2 py-0.5">{n}</span>
                {j < p.relations.length && (
                  <span className="text-xs text-brand">—{p.relations[j]}→</span>
                )}
              </span>
            ))}
          </div>
          <div className="mt-1 flex items-center gap-2">
            <div className="h-1.5 flex-1 rounded-full bg-edge/50">
              <div
                className="h-1.5 rounded-full bg-brand2"
                style={{ width: `${Math.round(p.reliability * 100)}%` }}
              />
            </div>
            <span className="text-xs text-slate-400">
              reliability {p.reliability.toFixed(2)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
