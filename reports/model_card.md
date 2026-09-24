# Analytic system card

## System

Curriculum Knowledge Graph

## Purpose

Typed, provenance-aware curriculum graph for prerequisite reasoning, alignment review, structural diagnostics, and inspectable curriculum paths.

## Current maturity

Working research prototype.

The bundled graph is synthetic and deliberately contains several alignment and prerequisite problems so the software path can be tested.

It does not establish curriculum quality or pedagogical validity for a real program.

## Entity model

Supported entity types:

- Program
- Course
- Module
- Concept
- LearningOutcome
- Competency
- Assessment
- Resource

## Relation model

Supported relation types:

- PART_OF
- TEACHES
- HAS_OUTCOME
- ASSESSES
- ALIGNS_WITH
- PREREQUISITE_OF
- SUPPORTS

The implementation validates permitted source and target entity types for every relation.

## Provenance

Each relation can contain:

- confidence
- source type
- evidence note
- review date

These fields support auditability.

They do not make a curriculum claim true.

## Main outputs

### Prerequisite reasoning

- direct prerequisites
- direct dependents
- prerequisite ancestors
- prerequisite descendants
- shortest paths
- multiple simple paths
- prerequisite cycles
- topological sequence when acyclic

### Structural diagnostics

- weakly connected components
- orphans
- prerequisite bottlenecks
- assessment target load
- overloaded-assessment flags

### Alignment diagnostics

- unassessed learning outcomes
- untaught concepts
- uncovered competencies
- courses without outcomes
- structural coverage summaries

### Interchange

- CSV import
- record/dictionary construction
- JSON import/export

## Interpretation boundary

The system can state:

- a relation is present in the graph
- a path exists
- a cycle exists
- an entity is structurally disconnected
- an outcome lacks an explicit assessment link
- a competency lacks an explicit outcome alignment

It cannot establish:

- that the relation is pedagogically correct
- that the path is optimal for learners
- that a structurally covered outcome is taught well
- that an assessment validly measures an outcome
- that graph degree equals educational importance
- that a program meets accreditation requirements

## Main limitations

The current baseline:

- uses an intentionally small relation vocabulary
- has one prerequisite relation strength rather than required/recommended/co-requisite distinctions
- does not implement ontology inference
- does not implement RDF/OWL or SPARQL
- does not implement CASE conformance
- does not extract entities or relations automatically
- does not represent learner mastery
- does not model curriculum versions internally
- does not estimate expert agreement
- does not estimate uncertainty beyond a stored confidence field

## Evidence needed before real use

A real curriculum study should provide:

- entity-definition rules
- authoritative curriculum version
- source documents
- expert-review method
- prerequisite-definition rubric
- relation agreement/adjudication
- assessment-alignment procedure
- competency-alignment procedure
- version-change process
- evidence that graph findings are useful in curriculum review

## Human oversight

Every graph-derived curriculum finding should be reviewed by people who understand the curriculum domain.

The graph is a structured review aid, not an autonomous curriculum authority.
