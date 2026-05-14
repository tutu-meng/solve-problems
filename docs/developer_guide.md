# Developer Guide

This repository stores each Project Euler solution in a numbered problem folder. Put implementation files and problem-specific documentation together in that folder.

Expected layout:

```text
NNN/
  README.md
  <model-name>/
    solve.cpp
```

Guidelines:
- Reuse existing solver patterns where practical.
- Keep derivations, diagrams, verification notes, and final answers in `NNN/README.md`.
- Do not place new problem writeups in the shared `docs/` folder.
- Keep temporary build and test files under `tmp/` and remove them after verification.
