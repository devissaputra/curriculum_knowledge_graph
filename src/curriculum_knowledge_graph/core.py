# Calculation reading guide: ../CALCULATIONS.md (repository root).
# Coverage = eligible entities with a required relation / all eligible entities.
# A graph edge is a supplied claim, not proof of a pedagogical dependency. Cycles prevent a valid prerequisite topological order. Coverage depends on the declared entity and relation definitions.

import csv
import json
from collections import defaultdict, deque
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from numbers import Real
from pathlib import Path


ENTITY_TYPES = {
    "Program",
    "Course",
    "Module",
    "Concept",
    "LearningOutcome",
    "Competency",
    "Assessment",
    "Resource",
}

RELATION_RULES = {
    "PART_OF": {
        ("Course", "Program"),
        ("Module", "Course"),
        ("Assessment", "Course"),
        ("Resource", "Course"),
    },
    "TEACHES": {
        ("Course", "Concept"),
        ("Module", "Concept"),
    },
    "HAS_OUTCOME": {
        ("Course", "LearningOutcome"),
        ("Module", "LearningOutcome"),
    },
    "ASSESSES": {
        ("Assessment", "LearningOutcome"),
        ("Assessment", "Competency"),
    },
    "ALIGNS_WITH": {
        ("LearningOutcome", "Competency"),
    },
    "PREREQUISITE_OF": {
        ("Concept", "Concept"),
    },
    "SUPPORTS": {
        ("Resource", "Concept"),
        ("Resource", "LearningOutcome"),
    },
}


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _optional_text(value, name):
    if value is None or value == "":
        return None
    return _text(value, name)


def _unit_interval(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def _parse_date(value, name):
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be an ISO date string")
    try:
        return date.fromisoformat(value.strip()).isoformat()
    except ValueError as exc:
        raise ValueError(f"{name} must use YYYY-MM-DD format") from exc


def _rate(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator


class CurriculumGraph:
    """Typed curriculum knowledge graph with validated curriculum relations."""

    def __init__(self):
        self.entities = {}
        self.relations = []
        self._relation_keys = set()
        # Backward-compatible prerequisite adjacency.
        self.edges = defaultdict(set)

    @property
    def nodes(self):
        return set(self.entities)

    def add_entity(
        self,
        entity_id,
        entity_type,
        *,
        label=None,
        description=None,
        metadata=None,
    ):
        entity_id = _text(entity_id, "entity_id")
        entity_type = _text(entity_type, "entity_type")
        if entity_type not in ENTITY_TYPES:
            raise ValueError(
                f"entity_type must be one of {sorted(ENTITY_TYPES)}"
            )
        if entity_id in self.entities:
            raise ValueError(f"duplicate entity id: {entity_id}")

        label = entity_id if label is None else _text(label, "label")
        description = _optional_text(description, "description")
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, Mapping):
            raise ValueError("metadata must be a mapping")

        self.entities[entity_id] = {
            "id": entity_id,
            "type": entity_type,
            "label": label,
            "description": description,
            "metadata": dict(metadata),
        }
        return self.entities[entity_id]

    def add_concept(self, concept):
        concept = _text(concept, "concept")
        if concept in self.entities:
            if self.entities[concept]["type"] != "Concept":
                raise ValueError(
                    f"{concept} already exists as "
                    f"{self.entities[concept]['type']}"
                )
            return self.entities[concept]
        return self.add_entity(concept, "Concept", label=concept)

    def add_relation(
        self,
        source,
        relation,
        target,
        *,
        confidence=1.0,
        source_type="manual_entry",
        evidence=None,
        reviewed_on=None,
    ):
        source = _text(source, "source")
        target = _text(target, "target")
        relation = _text(relation, "relation").upper()
        if source == target:
            raise ValueError("self-relations are not allowed")
        if source not in self.entities:
            raise ValueError(f"unknown source entity: {source}")
        if target not in self.entities:
            raise ValueError(f"unknown target entity: {target}")
        if relation not in RELATION_RULES:
            raise ValueError(
                f"relation must be one of {sorted(RELATION_RULES)}"
            )

        source_type_name = self.entities[source]["type"]
        target_type_name = self.entities[target]["type"]
        if (
            source_type_name,
            target_type_name,
        ) not in RELATION_RULES[relation]:
            raise ValueError(
                f"{relation} does not allow "
                f"{source_type_name} -> {target_type_name}"
            )

        key = (source, relation, target)
        if key in self._relation_keys:
            raise ValueError(
                f"duplicate relation: {source} {relation} {target}"
            )

        confidence = _unit_interval(confidence, "confidence")
        source_type = _text(source_type, "source_type")
        evidence = _optional_text(evidence, "evidence")
        reviewed_on = _parse_date(reviewed_on, "reviewed_on")

        record = {
            "source": source,
            "relation": relation,
            "target": target,
            "confidence": confidence,
            "source_type": source_type,
            "evidence": evidence,
            "reviewed_on": reviewed_on,
        }
        self.relations.append(record)
        self._relation_keys.add(key)

        if relation == "PREREQUISITE_OF":
            self.edges[source].add(target)

        return record

    def add_prerequisite(
        self,
        prerequisite,
        concept,
        *,
        confidence=1.0,
        source_type="manual_entry",
        evidence=None,
        reviewed_on=None,
    ):
        prerequisite = _text(prerequisite, "prerequisite")
        concept = _text(concept, "concept")
        if prerequisite == concept:
            raise ValueError(
                "a concept cannot be its own direct prerequisite"
            )
        self.add_concept(prerequisite)
        self.add_concept(concept)
        return self.add_relation(
            prerequisite,
            "PREREQUISITE_OF",
            concept,
            confidence=confidence,
            source_type=source_type,
            evidence=evidence,
            reviewed_on=reviewed_on,
        )

    def entity(self, entity_id):
        entity_id = _text(entity_id, "entity_id")
        return self.entities.get(entity_id)

    def entities_of_type(self, entity_type):
        entity_type = _text(entity_type, "entity_type")
        if entity_type not in ENTITY_TYPES:
            raise ValueError(
                f"entity_type must be one of {sorted(ENTITY_TYPES)}"
            )
        return {
            entity_id
            for entity_id, entity in self.entities.items()
            if entity["type"] == entity_type
        }

    def relation_records(self, relation=None):
        if relation is None:
            return [dict(row) for row in self.relations]
        relation = _text(relation, "relation").upper()
        if relation not in RELATION_RULES:
            raise ValueError(
                f"relation must be one of {sorted(RELATION_RULES)}"
            )
        return [
            dict(row)
            for row in self.relations
            if row["relation"] == relation
        ]

    def neighbors(self, entity_id, *, relation=None, direction="outgoing"):
        entity_id = _text(entity_id, "entity_id")
        if entity_id not in self.entities:
            return set()
        if direction not in {"outgoing", "incoming"}:
            raise ValueError(
                "direction must be 'outgoing' or 'incoming'"
            )
        relation_filter = None
        if relation is not None:
            relation_filter = _text(relation, "relation").upper()
            if relation_filter not in RELATION_RULES:
                raise ValueError(
                    f"relation must be one of {sorted(RELATION_RULES)}"
                )

        output = set()
        for row in self.relations:
            if relation_filter and row["relation"] != relation_filter:
                continue
            if direction == "outgoing" and row["source"] == entity_id:
                output.add(row["target"])
            if direction == "incoming" and row["target"] == entity_id:
                output.add(row["source"])
        return output

    def direct_prerequisites(self, concept):
        return self.neighbors(
            concept,
            relation="PREREQUISITE_OF",
            direction="incoming",
        )

    def direct_dependents(self, concept):
        return self.neighbors(
            concept,
            relation="PREREQUISITE_OF",
            direction="outgoing",
        )

    def descendants(self, start):
        """Return prerequisite descendants reachable from start."""
        start = _text(start, "start")
        if start not in self.entities:
            return set()
        seen = {start}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for next_node in self.edges.get(node, set()):
                if next_node not in seen:
                    seen.add(next_node)
                    queue.append(next_node)
        seen.remove(start)
        return seen

    def ancestors(self, start):
        """Return all prerequisite ancestors of a concept."""
        start = _text(start, "start")
        if start not in self.entities:
            return set()
        reverse = defaultdict(set)
        for source, targets in self.edges.items():
            for target in targets:
                reverse[target].add(source)

        seen = {start}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for previous in reverse.get(node, set()):
                if previous not in seen:
                    seen.add(previous)
                    queue.append(previous)
        seen.remove(start)
        return seen

    def shortest_path(
        self,
        source,
        target,
        *,
        relation="PREREQUISITE_OF",
    ):
        source = _text(source, "source")
        target = _text(target, "target")
        relation = _text(relation, "relation").upper()
        if source not in self.entities or target not in self.entities:
            return None
        if source == target:
            return [source]

        queue = deque([[source]])
        seen = {source}
        while queue:
            path = queue.popleft()
            node = path[-1]
            for next_node in sorted(
                self.neighbors(node, relation=relation)
            ):
                if next_node == target:
                    return path + [next_node]
                if next_node not in seen:
                    seen.add(next_node)
                    queue.append(path + [next_node])
        return None

    def all_paths(
        self,
        source,
        target,
        *,
        relation="PREREQUISITE_OF",
        max_paths=100,
    ):
        source = _text(source, "source")
        target = _text(target, "target")
        relation = _text(relation, "relation").upper()
        if isinstance(max_paths, bool) or not isinstance(max_paths, int):
            raise ValueError("max_paths must be an integer")
        if max_paths <= 0:
            raise ValueError("max_paths must be positive")
        if source not in self.entities or target not in self.entities:
            return []

        found = []
        stack = [(source, [source])]
        while stack and len(found) < max_paths:
            node, path = stack.pop()
            if node == target:
                found.append(path)
                continue
            for next_node in sorted(
                self.neighbors(node, relation=relation),
                reverse=True,
            ):
                if next_node not in path:
                    stack.append((next_node, path + [next_node]))
        return found

    def detect_prerequisite_cycles(self):
        """Return canonical prerequisite cycles as node sequences."""
        concepts = sorted(self.entities_of_type("Concept"))
        state = {}
        stack = []
        position = {}
        cycles = set()

        def canonical_cycle(nodes):
            core = nodes[:-1]
            rotations = [
                tuple(core[index:] + core[:index])
                for index in range(len(core))
            ]
            best = min(rotations)
            return best + (best[0],)

        def visit(node):
            state[node] = 1
            position[node] = len(stack)
            stack.append(node)

            for next_node in sorted(self.edges.get(node, set())):
                if state.get(next_node, 0) == 0:
                    visit(next_node)
                elif state.get(next_node) == 1:
                    start_index = position[next_node]
                    cycle = stack[start_index:] + [next_node]
                    cycles.add(canonical_cycle(cycle))

            stack.pop()
            position.pop(node, None)
            state[node] = 2

        for concept in concepts:
            if state.get(concept, 0) == 0:
                visit(concept)

        return [list(cycle) for cycle in sorted(cycles)]

    def topological_order(self):
        """Return a prerequisite-respecting order for all concepts."""
        concepts = self.entities_of_type("Concept")
        indegree = {concept: 0 for concept in concepts}
        for source, targets in self.edges.items():
            if source not in concepts:
                continue
            for target in targets:
                if target in indegree:
                    indegree[target] += 1

        queue = deque(
            sorted(
                concept
                for concept, degree in indegree.items()
                if degree == 0
            )
        )
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for target in sorted(self.edges.get(node, set())):
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)

        if len(order) != len(concepts):
            raise ValueError(
                "prerequisite graph contains a cycle; "
                "topological order is undefined"
            )
        return order

    def connected_components(self, *, relation=None):
        """Return weakly connected components for all or one relation type."""
        if relation is not None:
            relation = _text(relation, "relation").upper()
            if relation not in RELATION_RULES:
                raise ValueError(
                    f"relation must be one of {sorted(RELATION_RULES)}"
                )

        adjacency = defaultdict(set)
        for entity_id in self.entities:
            adjacency[entity_id]
        for row in self.relations:
            if relation and row["relation"] != relation:
                continue
            adjacency[row["source"]].add(row["target"])
            adjacency[row["target"]].add(row["source"])

        remaining = set(self.entities)
        components = []
        while remaining:
            start = min(remaining)
            queue = deque([start])
            component = set()
            while queue:
                node = queue.popleft()
                if node in component:
                    continue
                component.add(node)
                remaining.discard(node)
                for neighbor in sorted(adjacency[node]):
                    if neighbor not in component:
                        queue.append(neighbor)
            components.append(component)
        return components

    def orphans(self, *, entity_type=None):
        """Return entities with no incoming or outgoing relation."""
        if entity_type is not None:
            candidates = self.entities_of_type(entity_type)
        else:
            candidates = set(self.entities)

        connected = set()
        for row in self.relations:
            connected.add(row["source"])
            connected.add(row["target"])
        return candidates - connected

    def bottlenecks(
        self,
        *,
        relation="PREREQUISITE_OF",
        min_degree=3,
    ):
        relation = _text(relation, "relation").upper()
        if isinstance(min_degree, bool) or not isinstance(min_degree, int):
            raise ValueError("min_degree must be an integer")
        if min_degree < 1:
            raise ValueError("min_degree must be positive")

        rows = []
        for entity_id in sorted(self.entities):
            incoming = self.neighbors(
                entity_id,
                relation=relation,
                direction="incoming",
            )
            outgoing = self.neighbors(
                entity_id,
                relation=relation,
                direction="outgoing",
            )
            degree = len(incoming) + len(outgoing)
            if degree >= min_degree:
                rows.append(
                    {
                        "entity_id": entity_id,
                        "incoming": len(incoming),
                        "outgoing": len(outgoing),
                        "degree": degree,
                    }
                )
        rows.sort(key=lambda row: (-row["degree"], row["entity_id"]))
        return rows

    def assessment_loads(self):
        rows = []
        for assessment in sorted(
            self.entities_of_type("Assessment")
        ):
            outcomes = self.neighbors(
                assessment,
                relation="ASSESSES",
                direction="outgoing",
            )
            rows.append(
                {
                    "assessment": assessment,
                    "targets": sorted(outcomes),
                    "target_count": len(outcomes),
                }
            )
        rows.sort(
            key=lambda row: (
                -row["target_count"],
                row["assessment"],
            )
        )
        return rows

    def overloaded_assessments(self, threshold=3):
        if isinstance(threshold, bool) or not isinstance(threshold, int):
            raise ValueError("threshold must be an integer")
        if threshold < 1:
            raise ValueError("threshold must be positive")
        return [
            row
            for row in self.assessment_loads()
            if row["target_count"] > threshold
        ]

    def alignment_gaps(self):
        outcomes = self.entities_of_type("LearningOutcome")
        concepts = self.entities_of_type("Concept")
        competencies = self.entities_of_type("Competency")
        courses = self.entities_of_type("Course")

        assessed = set()
        taught = set()
        aligned = set()
        courses_with_outcomes = set()

        for row in self.relations:
            if row["relation"] == "ASSESSES":
                if self.entities[row["target"]]["type"] == "LearningOutcome":
                    assessed.add(row["target"])
            elif row["relation"] == "TEACHES":
                taught.add(row["target"])
            elif row["relation"] == "ALIGNS_WITH":
                aligned.add(row["target"])
            elif row["relation"] == "HAS_OUTCOME":
                courses_with_outcomes.add(row["source"])

        return {
            "unassessed_outcomes": sorted(outcomes - assessed),
            "untaught_concepts": sorted(concepts - taught),
            "uncovered_competencies": sorted(
                competencies - aligned
            ),
            "courses_without_outcomes": sorted(
                courses - courses_with_outcomes
            ),
        }

    def coverage_summary(self):
        outcomes = self.entities_of_type("LearningOutcome")
        concepts = self.entities_of_type("Concept")
        competencies = self.entities_of_type("Competency")
        courses = self.entities_of_type("Course")
        gaps = self.alignment_gaps()

        assessed_count = (
            len(outcomes) - len(gaps["unassessed_outcomes"])
        )
        taught_count = len(concepts) - len(gaps["untaught_concepts"])
        aligned_count = (
            len(competencies)
            - len(gaps["uncovered_competencies"])
        )
        outcome_course_count = (
            len(courses)
            - len(gaps["courses_without_outcomes"])
        )

        return {
            "learning_outcomes": {
                "total": len(outcomes),
                "assessed": assessed_count,
                "coverage": _rate(assessed_count, len(outcomes)),
            },
            "concepts": {
                "total": len(concepts),
                "taught": taught_count,
                "coverage": _rate(taught_count, len(concepts)),
            },
            "competencies": {
                "total": len(competencies),
                "aligned": aligned_count,
                "coverage": _rate(
                    aligned_count,
                    len(competencies),
                ),
            },
            "courses": {
                "total": len(courses),
                "with_outcomes": outcome_course_count,
                "coverage": _rate(
                    outcome_course_count,
                    len(courses),
                ),
            },
        }

    def validate_graph(self):
        return {
            "entity_count": len(self.entities),
            "relation_count": len(self.relations),
            "prerequisite_cycles": self.detect_prerequisite_cycles(),
            "orphans": sorted(self.orphans()),
            "alignment_gaps": self.alignment_gaps(),
            "coverage": self.coverage_summary(),
        }

    def to_dict(self):
        return {
            "entities": [
                dict(self.entities[entity_id])
                for entity_id in sorted(self.entities)
            ],
            "relations": [
                dict(row)
                for row in sorted(
                    self.relations,
                    key=lambda row: (
                        row["source"],
                        row["relation"],
                        row["target"],
                    ),
                )
            ],
        }

    def to_json(self, path):
        path = Path(path)
        path.write_text(
            json.dumps(self.to_dict(), indent=2) + "\n",
            encoding="utf-8",
        )

    @classmethod
    def from_records(cls, entities, relations):
        if not isinstance(entities, Sequence) or isinstance(
            entities, (str, bytes)
        ):
            raise ValueError("entities must be a sequence")
        if not isinstance(relations, Sequence) or isinstance(
            relations, (str, bytes)
        ):
            raise ValueError("relations must be a sequence")

        graph = cls()
        for row in entities:
            if not isinstance(row, Mapping):
                raise ValueError("entity records must be mappings")
            metadata = row.get("metadata", {})
            graph.add_entity(
                row.get("id"),
                row.get("type"),
                label=row.get("label"),
                description=row.get("description"),
                metadata=metadata,
            )

        for row in relations:
            if not isinstance(row, Mapping):
                raise ValueError("relation records must be mappings")
            graph.add_relation(
                row.get("source"),
                row.get("relation"),
                row.get("target"),
                confidence=row.get("confidence", 1.0),
                source_type=row.get(
                    "source_type",
                    "manual_entry",
                ),
                evidence=row.get("evidence"),
                reviewed_on=row.get("reviewed_on"),
            )
        return graph

    @classmethod
    def from_json(cls, path):
        payload = json.loads(
            Path(path).read_text(encoding="utf-8")
        )
        if not isinstance(payload, Mapping):
            raise ValueError("JSON payload must be a mapping")
        return cls.from_records(
            payload.get("entities", []),
            payload.get("relations", []),
        )

    @classmethod
    def from_csv(cls, entities_path, relations_path):
        entities = []
        with Path(entities_path).open(
            encoding="utf-8",
            newline="",
        ) as handle:
            for row in csv.DictReader(handle):
                metadata = {
                    key: value
                    for key, value in row.items()
                    if key not in {
                        "id",
                        "type",
                        "label",
                        "description",
                    }
                    and value not in (None, "")
                }
                entities.append(
                    {
                        "id": row.get("id"),
                        "type": row.get("type"),
                        "label": row.get("label"),
                        "description": row.get("description"),
                        "metadata": metadata,
                    }
                )

        relations = []
        with Path(relations_path).open(
            encoding="utf-8",
            newline="",
        ) as handle:
            for row in csv.DictReader(handle):
                confidence = row.get("confidence")
                relations.append(
                    {
                        "source": row.get("source"),
                        "relation": row.get("relation"),
                        "target": row.get("target"),
                        "confidence": (
                            1.0
                            if confidence in (None, "")
                            else float(confidence)
                        ),
                        "source_type": row.get(
                            "source_type"
                        )
                        or "manual_entry",
                        "evidence": row.get("evidence"),
                        "reviewed_on": row.get("reviewed_on"),
                    }
                )
        return cls.from_records(entities, relations)
