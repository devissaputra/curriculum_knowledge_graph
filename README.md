# Curriculum Knowledge Graph

> Directed curriculum graph for prerequisite reachability, isolated concept checks, and inspectable learning paths.

[![CI](https://github.com/devissaputra/curriculum-knowledge-graph/actions/workflows/ci.yml/badge.svg)](https://github.com/devissaputra/curriculum-knowledge-graph/actions/workflows/ci.yml)

![Curriculum Knowledge Graph workflow](assets/architecture.svg)

**Area:** Instructional Design & Curriculum Intelligence    
**Status:** working research prototype  
**Author:** Devis Wawan Saputra

## What this project is for

This repository represents concepts and explicit prerequisite relationships as a directed graph. The goal is to make prerequisite chains and isolated concepts visible without pretending that graph structure alone captures curriculum quality.

**Who may find it useful:** Curriculum designers and researchers working on curriculum mapping, pathway design, and program coherence.

## Research questions

1. Can graph structure reveal prerequisite gaps and isolated outcomes?
2. How can curriculum coverage be quantified without reducing design quality to a single score?
3. Which resources are structurally overloaded or disconnected?

## How it works

The graph stores explicit prerequisite edges and registered concepts. It can return every concept reachable from a starting point and identify concepts with no incoming or outgoing prerequisite relation. Traversal is cycle safe and does not return the starting concept as its own descendant.

![Curriculum Knowledge Graph data and reasoning flow](assets/data_flow.svg)

Outcomes or concepts are first represented as nodes, then explicit prerequisite links are added. The current baseline supports reachability and orphan checks; entity linking and automatic graph extraction remain future work.

![Synthetic demo snapshot for Curriculum Knowledge Graph](assets/demo_snapshot.svg)

This snapshot shows the bundled synthetic example for Curriculum Knowledge Graph. It checks the software path; it is not an empirical performance result.

## Methods in the current baseline

- directed prerequisite graph
- concept registration
- descendant queries
- orphan concept detection
- cycle safe traversal

## Data

A synthetic curriculum graph is included; CSV import templates support course-specific mapping.

`data/README.md` documents the sample schema and the conditions that should be recorded before any real dataset is connected. Restricted or identifiable learner data should stay outside the repository.

## Run the demo

```bash
git clone https://github.com/devissaputra/curriculum-knowledge-graph.git
cd curriculum-knowledge-graph
python scripts/run_demo.py
python -m unittest discover -s tests -v
```

The demo builds a three concept chain from algebra to calculus to optimization and prints the concepts reachable from algebra.

## What to evaluate next

A stronger study should build a graph from a real curriculum, have subject experts verify prerequisite links, and measure whether graph based path recommendations are educationally sensible.

## Evaluation view

![Curriculum Knowledge Graph evaluation dashboard](assets/evaluation_dashboard.svg)

The Curriculum Knowledge Graph dashboard is an evaluation checklist rather than a result chart. The bars are illustrative only; the labels show the evidence a real study would need to collect.

## Limits and responsible use

The graph only knows relationships that are explicitly entered. It does not infer prerequisites from text, estimate mastery, or prove that a path is pedagogically optimal. See `docs/ethics_and_risks.md` for the broader risk review.

## Repository map

```text
.
├── .github/workflows/ci.yml
├── assets/
│   ├── architecture.svg
│   ├── data_flow.svg
│   ├── demo_snapshot.svg
│   └── evaluation_dashboard.svg
├── data/
│   ├── README.md
│   └── sample.csv
├── docs/
│   ├── ethics_and_risks.md
│   ├── related_work.md
│   └── research_protocol.md
├── reports/model_card.md
├── scripts/run_demo.py
├── src/curriculum_knowledge_graph/core.py
├── tests/test_core.py
├── CITATION.cff
├── LICENSE
├── pyproject.toml
└── README.md
```

## Research path

A credible next version would:

1. encode one real curriculum with documented concept definitions
2. measure prerequisite link agreement across subject experts
3. evaluate path queries against actual course progression

## Related work

`docs/related_work.md` points to open projects that are relevant to this problem area. They are context for comparison and study design; this repository does not present their code as its own.

## Citation and license

`CITATION.cff` contains the software citation. The code and original SVG visuals use the MIT License. Any external dataset keeps its own license and usage conditions.
