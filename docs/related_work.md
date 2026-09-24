# Related work and standards context

Curriculum Knowledge Graph is an original transparent implementation.

It does not claim conformance with the standards below or reproduce the methods/results of the cited research.

## 1EdTech CASE

The Competencies and Academic Standards Exchange (CASE) standard defines a machine-readable way to exchange academic standards, competencies, skills, learning outcomes, and associations among them.

CASE uses stable identifiers and structured associations so learning standards and competencies can be connected to courses, resources, assessments, and other systems.

This is directly relevant to the repository's emphasis on:

- stable curriculum identifiers
- explicit entity types
- competency/outcome alignment
- inspectable associations
- future interoperability

Current reference:
https://www.1edtech.org/standards/case

The repository does **not** currently implement the complete CASE information model, REST API, JSON-LD binding, rubric structures, or conformance requirements.

## Concept prerequisite knowledge graphs

Manrique, Pereira, and Mariño studied the use of knowledge graphs for identifying concept prerequisite relationships.

- Manrique R, Pereira B, Mariño O.
- *Exploring knowledge graphs for the identification of concept prerequisites.*
- Smart Learning Environments. 2019;6:21.
- https://doi.org/10.1186/s40561-019-0104-3

That work is relevant to the repository's explicit prerequisite graph, path reasoning, and the need to validate whether one concept genuinely precedes another.

The present implementation does not automatically infer prerequisite relations.

## Educational resource knowledge graphs

Reales, Manrique, and Grévisse investigated knowledge graphs constructed from educational resources to identify core concepts.

- Reales D, Manrique R, Grévisse C.
- *Core Concept Identification in Educational Resources via Knowledge Graphs and Large Language Models.*
- SN Computer Science. 2024;5:1029.
- https://doi.org/10.1007/s42979-024-03341-y

Their work illustrates a different problem: extracting and linking concepts from educational content.

The current repository deliberately does not perform entity extraction or automatic entity linking. Its entities and relations are explicit reviewed inputs.

## Knowledge-graph opportunities and limitations

Knowledge-graph research emphasizes that graph quality depends on knowledge acquisition, fusion, completion, reasoning, and representation choices.

- *Knowledge Graphs: Opportunities and Challenges.*
- Artificial Intelligence Review.
- https://doi.org/10.1007/s10462-023-10465-9

For curriculum graphs, this reinforces a practical point: a graph can only reason over the curriculum knowledge that was encoded, and incomplete or poorly governed relations can produce misleading structural conclusions.

## Current scope

Implemented:

- typed curriculum entities
- typed and semantically validated relations
- provenance/confidence fields
- prerequisite ancestors/descendants
- shortest and multiple paths
- cycle detection
- topological sequencing for acyclic prerequisite graphs
- connected components
- orphan detection
- bottleneck diagnostics
- assessment-load diagnostics
- alignment-gap detection
- structural coverage summaries
- CSV import
- JSON import/export

Not implemented:

- RDF/OWL serialization
- SPARQL
- CASE conformance
- ontology inference
- automatic concept extraction
- automatic entity linking
- learned prerequisite discovery
- learner mastery
- personalized sequencing
- graph embeddings
- graph neural networks

The current repository is best understood as a transparent curriculum semantic-graph and reasoning baseline designed for expert review.
