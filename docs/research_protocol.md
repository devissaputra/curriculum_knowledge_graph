# Research protocol

## Project

Curriculum Knowledge Graph

## Questions

1. Can graph structure reveal prerequisite gaps and isolated outcomes?
2. How can curriculum coverage be quantified without reducing design quality to a single score?
3. Which resources are structurally overloaded or disconnected?

## Baseline methods

- directed prerequisite graph
- concept registration
- descendant queries
- orphan concept detection
- cycle safe traversal

## Evidence to collect

Start from the current transparent baseline and record every transformation needed to produce reachable prerequisite descendants and isolated concept flags. Keep a clear boundary between synthetic demonstration data and any future empirical dataset.

## Validation

Sample graph edges for expert review, report precision and coverage, and test whether suggested prerequisite paths match established curriculum sequencing. Cycles and disconnected components should be inspected explicitly.

## What counts as a useful result

A stronger study should build a graph from a real curriculum, have subject experts verify prerequisite links, and measure whether graph based path recommendations are educationally sensible.

## Threats to validity

Curriculum concepts can be defined at inconsistent levels, prerequisites may be conditional rather than absolute, and different experts may disagree on edge direction.
