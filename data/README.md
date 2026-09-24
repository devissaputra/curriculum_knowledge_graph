# Data documentation

## Included data

All curriculum data in this folder are synthetic.

- `entities.csv` contains typed curriculum entities.
- `relations.csv` contains typed, provenance-aware graph relations.
- `sample.csv` is a compact relation sample for quick inspection.

No learner records are required by the current graph model.

## Entity schema

`entities.csv` contains:

- `id`: stable graph identifier
- `type`: one of the supported entity types
- `label`: human-readable name
- `description`: short definition
- `domain`: synthetic subject/domain metadata

Supported entity types:

- Program
- Course
- Module
- Concept
- LearningOutcome
- Competency
- Assessment
- Resource

Stable identifiers matter because labels can change while graph references need to remain durable.

## Relation schema

`relations.csv` contains:

- `source`
- `relation`
- `target`
- `confidence`
- `source_type`
- `evidence`
- `reviewed_on`

Supported relation types:

- `PART_OF`
- `TEACHES`
- `HAS_OUTCOME`
- `ASSESSES`
- `ALIGNS_WITH`
- `PREREQUISITE_OF`
- `SUPPORTS`

The software validates which source and target entity types are permitted for each relation.

For example:

- Course → TEACHES → Concept
- Assessment → ASSESSES → LearningOutcome
- LearningOutcome → ALIGNS_WITH → Competency
- Concept → PREREQUISITE_OF → Concept

Invalid semantic combinations are rejected.

## Provenance

A graph relation is a curriculum claim.

The current baseline therefore stores:

- confidence
- source type
- evidence note
- review date

These fields do not make a relation correct. They make the basis of the relation inspectable.

For real curriculum work, provenance should identify the authoritative curriculum document, subject-matter expert review, standards mapping, governance decision, or other source used to justify the relation.

## Deliberate synthetic issues

The bundled graph intentionally contains problems so the analytics have something meaningful to discover:

- one prerequisite cycle
- one orphan concept
- one competency with no learning-outcome alignment
- one learning outcome with no assessment
- one capstone assessment connected to more than three outcomes
- several prerequisite bottlenecks
- more than one path to a later AIED concept

These are test fixtures, not recommended curriculum designs.

## Interoperability context

1EdTech CASE provides a standardized way to exchange competencies, academic standards, learning outcomes, and associations between them.

The current repository does not claim CASE conformance.

Its use of stable identifiers, typed curriculum entities, associations, and explicit alignments is designed to make later interoperability work more straightforward.

Reference:
https://www.1edtech.org/standards/case

## Import and export

The package supports:

- CSV import through `CurriculumGraph.from_csv(...)`
- dictionary/record construction through `from_records(...)`
- JSON import through `from_json(...)`
- JSON export through `to_json(...)`

Importers validate entity types, relation semantics, duplicate identifiers, dangling relations, confidence bounds, and review-date format.

## Before real curriculum data are connected

Document:

- curriculum version
- program/course ownership
- identifier policy
- entity definitions
- concept granularity rules
- relation definitions
- prerequisite evidence
- expert-review procedure
- confidence interpretation
- standards/competency source
- assessment-alignment method
- resource-alignment method
- update/version process
- disagreement resolution
- deprecation rules

## What this dataset does not represent

The graph does not contain learner mastery or performance data.

It does not infer prerequisites from text.

It does not prove that a prerequisite relation is necessary.

It does not prove that a topological sequence is pedagogically optimal.

It does not treat structural coverage as equivalent to curriculum quality.

## Do not commit

Do not commit confidential curriculum documents, licensed standards that prohibit redistribution, restricted assessment items, unpublished accreditation evidence, identifiable student records, or proprietary course materials unless redistribution is explicitly permitted.

Keep restricted sources in an approved storage environment and retain only permissible references or derived metadata in the repository.
