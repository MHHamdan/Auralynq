# Recording the Auralynq demo

`README.md` references `docs/demo.gif` as a placeholder. To produce it:

1. Start the stack: `make stack-up` (or run `make serve` + `cd web && npm run dev`).
2. Open http://localhost:3000.
3. Record a short clip showing:
   - a typed question streaming a grounded answer with citations,
   - a relational question routing to **PathRAG** (watch the evidence-path panel),
   - a **push-to-talk** voice question with a spoken answer.
4. Export to `docs/demo.gif` (e.g. `peek`, `asciinema`+`agg`, or `ffmpeg`):

   ```bash
   ffmpeg -i demo.mov -vf "fps=12,scale=900:-1:flags=lanczos" docs/demo.gif
   ```

For a terminal-only demo, `make demo` runs the full pipeline (index → typed →
relational → voice) and prints cited answers + evidence paths.
