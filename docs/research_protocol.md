# Research protocol

## Project

Curriculum Knowledge Graph

## Research questions

1. Can typed curriculum relations expose alignment gaps that are difficult to see in document-based curriculum maps?
2. Which prerequisite structures create cycles, bottlenecks, disconnected concepts, or competing learning paths?
3. How consistently do subject-matter experts agree on prerequisite and alignment relations?
4. Which assessments carry unusually broad outcome coverage?
5. How completely are learning outcomes assessed, concepts taught, competencies aligned, and courses connected to outcomes?
6. How stable are graph findings across curriculum versions and expert-review rounds?

## Current graph model

The repository represents eight entity types:

- Program
- Course
- Module
- Concept
- LearningOutcome
- Competency
- Assessment
- Resource

It validates seven relation types:

- PART_OF
- TEACHES
- HAS_OUTCOME
- ASSESSES
- ALIGNS_WITH
- PREREQUISITE_OF
- SUPPORTS

Each relation can include confidence, source type, evidence, and a review date.

The implementation does not automatically infer these relations.

## Semantic validation

A knowledge graph is only useful when relation semantics are constrained.

The code therefore rejects combinations such as:

- LearningOutcome → TEACHES → Course
- Assessment → PREREQUISITE_OF → Concept
- unknown source/target identifiers
- duplicate relations
- self-relations
- invalid confidence values

Validation protects schema consistency, not educational truth.

A semantically valid relation can still be pedagogically wrong.

## Prerequisite reasoning

The current baseline implements:

- direct prerequisite lookup
- direct dependent lookup
- all prerequisite ancestors
- prerequisite descendants
- shortest prerequisite path
- multiple simple prerequisite paths
- prerequisite cycle detection
- topological sequencing when the prerequisite graph is acyclic

Cycles are reported rather than silently interpreted as valid learning sequences.

## Structural diagnostics

The current graph can report:

- orphans
- weakly connected components
- prerequisite bottlenecks
- assessment load
- overloaded assessments
- unassessed learning outcomes
- untaught concepts
- uncovered competencies
- courses without learning outcomes
- structural coverage summaries

These are graph diagnostics.

They are not direct measures of curriculum quality.

## Provenance

Every nontrivial curriculum relation should be traceable to evidence.

For real studies, record at least:

- curriculum document/version
- reviewer or review group
- relation rationale
- confidence or agreement procedure
- review date
- whether the relation is authoritative, inferred, proposed, or disputed

The current synthetic graph uses provenance fields only to exercise that workflow.

## Expert validation

A real study should sample relations for independent expert review.

Useful analyses include:

- agreement on whether the relation exists
- agreement on direction
- agreement on relation type
- confidence distributions
- disagreement by domain
- changes after adjudication

For prerequisite edges, reviewers should distinguish:

- strictly required prerequisite
- strongly recommended prerequisite
- helpful background
- co-requisite
- common sequence but not prerequisite

The current relation vocabulary uses a single PREREQUISITE_OF edge and therefore cannot yet represent those finer distinctions.

## Coverage interpretation

The repository reports structural coverage such as:

- proportion of learning outcomes with at least one assessment link
- proportion of concepts with at least one teaching link
- proportion of competencies with at least one aligned learning outcome
- proportion of courses with at least one learning outcome

A 100% structural coverage value does not prove quality, sufficient depth, cognitive alignment, fairness, or actual learner attainment.

## Evaluation study

A credible empirical study should include several layers.

### Schema validity

Can curriculum experts understand and consistently apply the entity and relation definitions?

### Relation validity

How often do experts confirm the entered relations?

### Path validity

Are prerequisite paths educationally sensible and consistent with course progression?

### Gap usefulness

Do reported orphans, alignment gaps, bottlenecks, or overloaded assessments lead to useful curriculum-review decisions?

### Version sensitivity

Do findings remain stable when the curriculum is revised?

### Interoperability

Can identifiers and competency/outcome relationships be mapped cleanly to an external standard such as 1EdTech CASE without losing meaning?

## Threats to validity

Major threats include:

- inconsistent concept granularity
- different interpretations of prerequisite strength
- curriculum documents that omit tacit relationships
- expert disagreement
- outdated relations after curriculum revision
- administrative sequence being mistaken for pedagogical prerequisite
- one outcome label representing several distinct skills
- assessments appearing aligned on paper but not in actual tasks
- resources being linked because of availability rather than pedagogical suitability
- graph centrality being overinterpreted as educational importance
- sparse documentation creating false orphan or coverage signals

The graph should support curriculum review, not replace expert curriculum judgment.
