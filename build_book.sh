#!/usr/bin/env bash
# build_book.sh — Build the Acceleralpho book as a browseable HTML site and a PDF.
#
# Usage:
#   ./build_book.sh          # HTML site only  (output: book/)
#   ./build_book.sh --pdf    # HTML site + PDF (output: book/  +  book.pdf)
#   ./build_book.sh --pdf-only  # PDF via pandoc only (no HTML site)
#
# Requirements:
#   pip install -r requirements-book.txt   (for HTML and mkdocs-with-pdf)
#   pandoc                                  (for the standalone PDF fallback)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$REPO_ROOT/docs"
BOOK_DIR="$REPO_ROOT/book"
PDF_OUT="$REPO_ROOT/book.pdf"

BUILD_HTML=true
BUILD_PDF=false

for arg in "$@"; do
  case "$arg" in
    --pdf)      BUILD_PDF=true ;;
    --pdf-only) BUILD_HTML=false; BUILD_PDF=true ;;
    --help|-h)
      echo "Usage: $0 [--pdf] [--pdf-only]"
      echo "  --pdf       Build HTML site AND PDF"
      echo "  --pdf-only  Build PDF only via pandoc (faster, no HTML site)"
      exit 0 ;;
  esac
done

# ─── HTML site via MkDocs ────────────────────────────────────────────────────
if $BUILD_HTML; then
  echo "==> Building HTML book site → $BOOK_DIR/"

  if $BUILD_PDF; then
    # mkdocs-with-pdf is triggered by the ENABLE_PDF_EXPORT env var
    ENABLE_PDF_EXPORT=1 mkdocs build --config-file "$REPO_ROOT/mkdocs.yml"
    echo "==> PDF written → $PDF_OUT"
  else
    mkdocs build --config-file "$REPO_ROOT/mkdocs.yml"
  fi

  echo ""
  echo "✅  HTML site ready at:  $BOOK_DIR/index.html"
  echo "    Open with:  open $BOOK_DIR/index.html  (macOS)"
  echo "             or xdg-open $BOOK_DIR/index.html  (Linux)"
  echo ""
fi

# ─── PDF via pandoc (standalone, no HTML build needed) ───────────────────────
if $BUILD_PDF && ! $BUILD_HTML; then
  if ! command -v pandoc &>/dev/null; then
    echo "ERROR: pandoc not found. Install it from https://pandoc.org/installing.html"
    exit 1
  fi

  echo "==> Building PDF via pandoc → $PDF_OUT"

  # Ordered list of all chapter markdown files
  CHAPTERS=(
    "$DOCS_DIR/index.md"
    "$DOCS_DIR/part1/1.1 The Great IDE Exodus.md"
    "$DOCS_DIR/part1/1.2 Claude Code The Boris Persona.md"
    "$DOCS_DIR/part1/1.3 The UX of Autonomy.md"
    "$DOCS_DIR/part1/2.1 I'm in Danger Feedback Loops.md"
    "$DOCS_DIR/part1/2.2 Recursive Failure.md"
    "$DOCS_DIR/part1/2.3 The Proverbial Glue.md"
    "$DOCS_DIR/part2/3.1 Steve Yegge High-Throughput Agentic Environments.md"
    "$DOCS_DIR/part2/3.2 Beyond RAG The Infinite Window.md"
    "$DOCS_DIR/part2/3.3 Cody and the Context Power Plant.md"
    "$DOCS_DIR/part2/4.1 LLMs as First-Class OS Citizens.md"
    "$DOCS_DIR/part2/4.2 Orchestration vs Execution The Loom Framework.md"
    "$DOCS_DIR/part2/4.3 Refactoring the Past Legacy C++ via Agentic Threads.md"
    "$DOCS_DIR/part3/5.1 Leashing the Beast Tool-Calling and Sandboxed Execution.md"
    "$DOCS_DIR/part3/5.2 OpenRouter The Switzerland of the Model Wars.md"
    "$DOCS_DIR/part3/5.3 OpenCode and the Democratization of Agentic Access.md"
    "$DOCS_DIR/part3/6.1 AWS Bedrock and Azure AI Foundry The Enterprise Response.md"
    "$DOCS_DIR/part3/6.2 The Copilot Workspace Agentifying the Pull Request.md"
    "$DOCS_DIR/part3/6.3 Security and Governance in the Age of Shadow Agents.md"
    "$DOCS_DIR/part4/7.1 DeepSeek and Qwen Shattering the Western Moat.md"
    "$DOCS_DIR/part4/7.2 The Efficiency Gap High-Performance Coding on a Budget.md"
    "$DOCS_DIR/part4/7.3 The Geopolitics of Code Generation.md"
    "$DOCS_DIR/part4/8.1 Aider OpenDevin and the Bazaar of Agents.md"
    "$DOCS_DIR/part4/8.2 Local-First Running Boris on a Mac Studio.md"
    "$DOCS_DIR/part4/8.3 The Rise of the Personal Agent Stack.md"
    "$DOCS_DIR/part5/9.1 Self-Healing Codebases and Autonomous Bug-Hunting.md"
    "$DOCS_DIR/part5/9.2 The Synthetic Senior Managing Intent vs Managing Code.md"
    "$DOCS_DIR/part5/9.3 The Psychopathology of AI-Driven Technical Debt.md"
    "$DOCS_DIR/part5/10.1 Vile Offspring Agents Writing Agents.md"
    "$DOCS_DIR/part5/10.2 From Programmer to Agent Wrangler The New Career Path.md"
    "$DOCS_DIR/part5/10.3 Post-Code When Software is Grown Not Written.md"
    "$DOCS_DIR/references.md"
  )

  # Filter out files that don't exist yet (planned chapters)
  EXISTING=()
  for f in "${CHAPTERS[@]}"; do
    [[ -f "$f" ]] && EXISTING+=("$f")
  done

  pandoc \
    --from gfm \
    --to pdf \
    --pdf-engine=weasyprint \
    -M title="Acceleralpho: Evolution of Coding Agents and Agentic Harnesses" \
    -M author="Acceleralpho" \
    --toc \
    --toc-depth=3 \
    --output "$PDF_OUT" \
    "${EXISTING[@]}"

  echo ""
  echo "✅  PDF ready at: $PDF_OUT"
  echo ""
fi
