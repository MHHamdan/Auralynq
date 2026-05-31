import { Citation } from "@/lib/api";

export function Citations({ citations }: { citations: Citation[] }) {
  if (!citations?.length) return null;
  return (
    <div className="mt-3 space-y-1">
      <div className="text-xs uppercase tracking-wide text-slate-400">Citations</div>
      <ol className="space-y-1">
        {citations.map((c) => (
          <li key={c.marker} className="flex items-start gap-2 text-sm">
            <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-brand2/20 text-xs text-brand2">
              {c.marker}
            </span>
            <span>
              <span className="text-slate-200">{c.source}</span>{" "}
              <span className="text-slate-400">
                {c.speaker ? `· ${c.speaker} ` : ""}
                {c.locator}
              </span>
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}
