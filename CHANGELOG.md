# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Added a project-local Cursor rule requiring problem-specific documentation to live in each numbered problem folder.
- Added problem-local documentation files for Project Euler 994 and 995.
- Completed implementation for Project Euler 995: Divisor Residues.
- Added `995/GPT-5.5/solve.cpp` with a C++17 solver using discrete logs, cyclic mixed-radix DP, and scientific-notation formatting.
- Updated project documentation for the Project Euler 995 residue criterion, transition-prime search, DP approach, and final answer.
- Completed implementation for Project Euler 994: Triangle Count.
- Added `994/GPT-5.5/solve.cpp` with a C++17 solver using endpoint-pattern classification and a totient-weighted concurrency correction.
- Updated project documentation for the Project Euler 994 formula, weighted totient prefix recursion, verification checks, and final answer.
- Completed implementation for Project Euler 984: Knights and Horses.
- Added `Gemini 3.1 Pro (High)/solve.py` containing a fast evaluation algorithm of the degree 11 linear recurrence.
- Updated comprehensive documentation suite (`developer_guide.md`, `project_context.md`, `quick_reference.md`, `README.md`) detailing the mathematical insights, graph connectivity constraints, and FSM approach.
- Included Mermaid diagrams in `README.md` to represent the DP FSM transitions and solution logic.

### Changed
- Reworked shared `docs/` files to document repository conventions instead of individual Project Euler problem derivations.

### Removed
- Removed temporary C++ and Python development scripts (`explore_width.py`, `check_counts.py`, `find_rules.py`, `dp_fsm2.py`, etc.) generated during the discovery phase.
