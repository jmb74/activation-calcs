# Project Instructions

This repository contains FLUKA simulation files.

## Shared expertise

Use the installed FLUKA Codex skill for:
- FLUKA input development and validation
- Documentation lookup
- Flair project operations
- Scoring and output interpretation
- User-routine development

Do not duplicate the shared skill's instructions here.

## Project rules

- Preserve original simulation inputs.
- Make changes in working copies or dedicated branches.
- Keep generated simulation outputs out of Git.
- Document significant changes to physics settings.
- Current supplied beam condition is 30 MeV protons with the existing 3 mm water
  layer, 400 microA for seven days (latest user correction supersedes earlier
  40 microA and 16 MeV conditions).
- Explicitly recommend and document the executable before each run. The user's
  selected project executable is `flukadpm`; retain that choice unless a change
  is discussed. Check whether its additional models are needed for the actual
  projectile and energy rather than assuming it improves every calculation.
- Do not execute computationally expensive simulations
  without approval.

##Goals
- The goal of this project is to generate the isotope inventory of the target and then use it for radiation calculations. Isotope generation is the highest priority for physical accuracy.
