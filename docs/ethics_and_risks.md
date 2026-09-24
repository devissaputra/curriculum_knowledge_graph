# Ethics, safety, and misuse risks

## Intended use

Curriculum Knowledge Graph is a curriculum-design and research prototype.

It is intended to make curriculum relationships visible and reviewable.

It is not a system for automatically deciding what every learner must study, which instructor is responsible for a curriculum problem, or whether a program is academically adequate.

## Graph structure is not curriculum truth

A graph can look precise while encoding disputed or incomplete curriculum assumptions.

A PREREQUISITE_OF edge should therefore be treated as a documented claim, not an unquestionable fact.

Important distinctions can be lost when relationships such as:

- required prerequisite
- recommended background
- co-requisite
- administrative sequence
- common teaching order

are collapsed into one edge type.

The current baseline should not be used to enforce learner progression automatically.

## Concept granularity

One reviewer may model “machine learning” as one concept while another decomposes it into dozens of concepts.

Graph measures such as degree, bottlenecks, path length, and coverage depend heavily on granularity.

Comparisons across programs or versions are misleading unless entity-definition rules are reasonably consistent.

## Cycles

A prerequisite cycle can identify:

- an actual curriculum-design problem
- inconsistent terminology
- concept granularity problems
- a relationship that should be a co-requisite rather than a prerequisite
- simple data-entry error

Do not automatically delete a cycle because the graph says it is invalid for topological sequencing.

Review the curriculum meaning first.

## Bottlenecks

A highly connected concept may be important, but degree is not a validated measure of pedagogical importance.

Do not allocate teaching time, staffing, or learner remediation solely from graph centrality.

## Alignment gaps

An “unassessed outcome” may reflect missing documentation rather than absent assessment.

An “untaught concept” may be intentionally learned through independent work, prior study, or another curriculum layer that is not represented.

Graph gaps are review prompts.

They are not automatic findings of curriculum failure.

## Assessment overload

An assessment connected to many outcomes may be genuinely integrative.

A high relation count should trigger review of assessment validity and workload, not automatic decomposition.

## Provenance and governance

Curriculum relations can have institutional consequences.

A real graph should identify:

- source document/version
- relation owner
- review status
- evidence
- date
- whether the relation is proposed or authoritative
- how disagreements are resolved

Historical graph versions should be retained when curriculum decisions need an audit trail.

## Standards and interoperability

Mapping internal curriculum entities to external competency or standards frameworks can create an appearance of equivalence that is stronger than the evidence supports.

Cross-framework mappings should preserve provenance and, where possible, relation strength or mapping status.

## Learner impact

If the graph is later used for course recommendation or adaptive learning, additional safeguards are needed.

A structural path should not become a mandatory personalized path without evidence that the sequence is appropriate for the learner and context.

Alternative routes, prior learning, accessibility, and recognition of existing competence should remain possible.

## Sensitive or restricted curriculum material

This prototype does not require learner data.

However, real curriculum graphs may reference:

- restricted assessment items
- accreditation evidence
- proprietary teaching materials
- unpublished program changes
- licensed competency frameworks

Do not publish protected content merely because a graph can represent it.

## Excluded uses

Do not use this prototype alone for:

- automated accreditation decisions
- automated grading
- admissions decisions
- restricting course access
- deciding learner capability or mastery
- employee performance decisions
- ranking instructors
- declaring a program compliant with a standard

## Before real institutional use

Establish entity-definition rules, relation governance, provenance requirements, versioning, expert-review procedures, disagreement handling, access controls, standards-mapping rules, deprecation procedures, and a human process for reviewing every graph-derived curriculum recommendation.
