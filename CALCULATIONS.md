# Calculation guide

## Question and evidence

Where are curriculum prerequisites and assessment gaps?

Supplied typed entities and provenance-labeled relationships.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Validate relation semantics; traverse prerequisites; detect cycles; inspect coverage, bottlenecks and alignment gaps.

## Calculation and interpretation

`Coverage = eligible entities with a required relation / all eligible entities.`

A graph edge is a supplied claim, not proof of a pedagogical dependency. Cycles prevent a valid prerequisite topological order. Coverage depends on the declared entity and relation definitions.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| coverage: 3 assessed / 4 outcomes | 0.75 | unitless | `outputs.coverage: 3 assessed / 4 outcomes` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This curriculum graph represents courses, concepts, outcomes, assessments, and resources through typed, provenance-aware relationships. It validates relation semantics and exposes prerequisite paths, cycles, disconnected entities, and assessment-coverage gaps. These structural diagnostics help experts inspect a curriculum; the graph does not independently verify the pedagogical truth of its edges.

## Verification performed in this review

36 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`nodes`](src/curriculum_knowledge_graph/core.py#L110) | Inspect the explicit implementation and its callers. |
| [`add_entity`](src/curriculum_knowledge_graph/core.py#L113) | Inspect the explicit implementation and its callers. |
| [`add_concept`](src/curriculum_knowledge_graph/core.py#L147) | Inspect the explicit implementation and its callers. |
| [`add_relation`](src/curriculum_knowledge_graph/core.py#L158) | Inspect the explicit implementation and its callers. |
| [`add_prerequisite`](src/curriculum_knowledge_graph/core.py#L222) | Inspect the explicit implementation and its callers. |
| [`entity`](src/curriculum_knowledge_graph/core.py#L250) | Inspect the explicit implementation and its callers. |
| [`entities_of_type`](src/curriculum_knowledge_graph/core.py#L254) | Inspect the explicit implementation and its callers. |
| [`relation_records`](src/curriculum_knowledge_graph/core.py#L266) | Inspect the explicit implementation and its callers. |
| [`neighbors`](src/curriculum_knowledge_graph/core.py#L280) | Inspect the explicit implementation and its callers. |
| [`direct_prerequisites`](src/curriculum_knowledge_graph/core.py#L306) | Inspect the explicit implementation and its callers. |
| [`direct_dependents`](src/curriculum_knowledge_graph/core.py#L313) | Inspect the explicit implementation and its callers. |
| [`descendants`](src/curriculum_knowledge_graph/core.py#L320) | Return prerequisite descendants reachable from start. |
| [`ancestors`](src/curriculum_knowledge_graph/core.py#L336) | Return all prerequisite ancestors of a concept. |
| [`shortest_path`](src/curriculum_knowledge_graph/core.py#L357) | Inspect the explicit implementation and its callers. |
| [`all_paths`](src/curriculum_knowledge_graph/core.py#L387) | Inspect the explicit implementation and its callers. |
| [`detect_prerequisite_cycles`](src/curriculum_knowledge_graph/core.py#L420) | Return canonical prerequisite cycles as node sequences. |
| [`topological_order`](src/curriculum_knowledge_graph/core.py#L460) | Return a prerequisite-respecting order for all concepts. |
| [`connected_components`](src/curriculum_knowledge_graph/core.py#L494) | Return weakly connected components for all or one relation type. |
| [`orphans`](src/curriculum_knowledge_graph/core.py#L530) | Return entities with no incoming or outgoing relation. |
| [`bottlenecks`](src/curriculum_knowledge_graph/core.py#L543) | Inspect the explicit implementation and its callers. |
| [`assessment_loads`](src/curriculum_knowledge_graph/core.py#L580) | Inspect the explicit implementation and its callers. |
| [`overloaded_assessments`](src/curriculum_knowledge_graph/core.py#L605) | Inspect the explicit implementation and its callers. |
| [`alignment_gaps`](src/curriculum_knowledge_graph/core.py#L616) | Inspect the explicit implementation and its callers. |
| [`coverage_summary`](src/curriculum_knowledge_graph/core.py#L649) | Inspect the explicit implementation and its callers. |
| [`validate_graph`](src/curriculum_knowledge_graph/core.py#L698) | Inspect the explicit implementation and its callers. |
| [`to_dict`](src/curriculum_knowledge_graph/core.py#L708) | Inspect the explicit implementation and its callers. |
| [`to_json`](src/curriculum_knowledge_graph/core.py#L727) | Inspect the explicit implementation and its callers. |
| [`from_records`](src/curriculum_knowledge_graph/core.py#L735) | Inspect the explicit implementation and its callers. |
| [`from_json`](src/curriculum_knowledge_graph/core.py#L776) | Inspect the explicit implementation and its callers. |
| [`from_csv`](src/curriculum_knowledge_graph/core.py#L788) | Inspect the explicit implementation and its callers. |
| [`canonical_cycle`](src/curriculum_knowledge_graph/core.py#L428) | Inspect the explicit implementation and its callers. |
| [`visit`](src/curriculum_knowledge_graph/core.py#L437) | Inspect the explicit implementation and its callers. |

## What remains before a stronger research claim

A graph edge is a supplied claim, not proof of a pedagogical dependency. Cycles prevent a valid prerequisite topological order. Coverage depends on the declared entity and relation definitions. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
