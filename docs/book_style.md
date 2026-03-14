# Book Style Guide

Use this guide for every chapter and section draft.

## Chapter shape

1. **Orientation before detail**
   - Open with the problem being solved, why it matters, and what the reader should retain.
2. **How to read this chapter**
   - For math-heavy material, tell the reader what to understand now, what to memorize, and what is reference material.
3. **Concept loops**
   - Use 3-6 short loops in the order: concept -> worked example -> code -> check-yourself prompt.
4. **Deliverable and verification**
   - State what the reader will have built or understood by the end.
   - Include a verification checklist.
5. **Retrieval practice**
   - End with a short wrapping-up section and exercises or check-yourself prompts.

## House style

- Prefer beginner-friendly language first, production-grade detail second.
- Keep explanation, diagram, code, and verification steps physically close together.
- Prefer mermaid for flowcharts and block diagrams.
- Title important blocks:
  - `Example 2-1. Tracking stagnation`
  - `Equation 5-1. Token cost per loop`
- Use visible callouts instead of burying traps in prose:
  - `> **Tip:**`
  - `> **Warning:**`
  - `> **Pitfall:**`
  - `> **Key idea:**`

## File naming

- Write chapter outputs as Markdown files under part directories such as:
  - `docs/part1/2.1 I'm in Danger Feedback Loops.md`

## Verification standard

- If a code snippet is presented as executable, run it from `./src` during authoring.
- Document the observed output or behavior so future iterations can confirm it still matches the text.
