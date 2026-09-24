import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from curriculum_knowledge_graph import core


def build_graph():
    graph = core.CurriculumGraph()
    graph.add_entity("P1", "Program", label="AI Education")
    graph.add_entity("C1", "Course", label="Foundations")
    graph.add_entity("C2", "Course", label="Applied AI")
    graph.add_entity("M1", "Module", label="Modeling Module")

    for concept in ("algebra", "statistics", "calculus", "ml", "optimization"):
        graph.add_entity(concept, "Concept", label=concept.title())

    graph.add_entity("LO1", "LearningOutcome", label="Explain models")
    graph.add_entity("LO2", "LearningOutcome", label="Build models")
    graph.add_entity("LO3", "LearningOutcome", label="Audit models")
    graph.add_entity("K1", "Competency", label="AI reasoning")
    graph.add_entity("K2", "Competency", label="Responsible AI")
    graph.add_entity("A1", "Assessment", label="Capstone")
    graph.add_entity("R1", "Resource", label="Modeling notebook")

    graph.add_relation("C1", "PART_OF", "P1")
    graph.add_relation("C2", "PART_OF", "P1")
    graph.add_relation("M1", "PART_OF", "C2")
    graph.add_relation("C1", "TEACHES", "algebra")
    graph.add_relation("C1", "TEACHES", "statistics")
    graph.add_relation("C2", "TEACHES", "ml")
    graph.add_relation("M1", "TEACHES", "optimization")
    graph.add_relation("C1", "HAS_OUTCOME", "LO1")
    graph.add_relation("C2", "HAS_OUTCOME", "LO2")
    graph.add_relation("A1", "PART_OF", "C2")
    graph.add_relation("A1", "ASSESSES", "LO2")
    graph.add_relation("LO1", "ALIGNS_WITH", "K1")
    graph.add_relation("LO2", "ALIGNS_WITH", "K1")
    graph.add_relation("R1", "PART_OF", "C2")
    graph.add_relation("R1", "SUPPORTS", "ml")

    graph.add_prerequisite("algebra", "calculus")
    graph.add_prerequisite("statistics", "ml")
    graph.add_prerequisite("calculus", "optimization")
    graph.add_prerequisite("ml", "optimization")
    return graph


class CoreTests(unittest.TestCase):
    def test_add_entity_requires_type(self):
        graph = core.CurriculumGraph()
        with self.assertRaises(ValueError):
            graph.add_entity("x", "UnknownType")

    def test_whitespace_id_rejected(self):
        graph = core.CurriculumGraph()
        with self.assertRaises(ValueError):
            graph.add_entity("   ", "Concept")

    def test_duplicate_entity_rejected(self):
        graph = core.CurriculumGraph()
        graph.add_entity("x", "Concept")
        with self.assertRaises(ValueError):
            graph.add_entity("x", "Concept")

    def test_add_concept_is_backward_compatible(self):
        graph = core.CurriculumGraph()
        graph.add_concept("algebra")
        self.assertIn("algebra", graph.nodes)
        self.assertEqual(graph.entity("algebra")["type"], "Concept")

    def test_add_prerequisite_auto_registers_concepts(self):
        graph = core.CurriculumGraph()
        graph.add_prerequisite("a", "b")
        self.assertEqual(graph.descendants("a"), {"b"})

    def test_invalid_relation_semantics_rejected(self):
        graph = core.CurriculumGraph()
        graph.add_entity("course", "Course")
        graph.add_entity("outcome", "LearningOutcome")
        with self.assertRaises(ValueError):
            graph.add_relation("outcome", "TEACHES", "course")

    def test_dangling_relation_rejected(self):
        graph = core.CurriculumGraph()
        graph.add_entity("a", "Concept")
        with self.assertRaises(ValueError):
            graph.add_relation("a", "PREREQUISITE_OF", "missing")

    def test_duplicate_relation_rejected(self):
        graph = core.CurriculumGraph()
        graph.add_prerequisite("a", "b")
        with self.assertRaises(ValueError):
            graph.add_relation("a", "PREREQUISITE_OF", "b")

    def test_relation_provenance_is_retained(self):
        graph = core.CurriculumGraph()
        graph.add_concept("a")
        graph.add_concept("b")
        row = graph.add_relation(
            "a",
            "PREREQUISITE_OF",
            "b",
            confidence=0.8,
            source_type="expert_review",
            evidence="Workshop consensus",
            reviewed_on="2026-09-24",
        )
        self.assertEqual(row["confidence"], 0.8)
        self.assertEqual(row["source_type"], "expert_review")
        self.assertEqual(row["reviewed_on"], "2026-09-24")

    def test_confidence_range_validated(self):
        graph = core.CurriculumGraph()
        graph.add_concept("a")
        graph.add_concept("b")
        with self.assertRaises(ValueError):
            graph.add_relation(
                "a",
                "PREREQUISITE_OF",
                "b",
                confidence=2.0,
            )

    def test_direct_prerequisite_and_dependent_queries(self):
        graph = build_graph()
        self.assertEqual(
            graph.direct_prerequisites("optimization"),
            {"calculus", "ml"},
        )
        self.assertEqual(
            graph.direct_dependents("calculus"),
            {"optimization"},
        )

    def test_ancestors_and_descendants(self):
        graph = build_graph()
        self.assertEqual(
            graph.descendants("algebra"),
            {"calculus", "optimization"},
        )
        self.assertEqual(
            graph.ancestors("optimization"),
            {"algebra", "statistics", "calculus", "ml"},
        )

    def test_shortest_path(self):
        graph = build_graph()
        self.assertEqual(
            graph.shortest_path("algebra", "optimization"),
            ["algebra", "calculus", "optimization"],
        )

    def test_missing_shortest_path_returns_none(self):
        graph = build_graph()
        self.assertIsNone(
            graph.shortest_path("statistics", "calculus")
        )

    def test_all_paths_finds_alternatives(self):
        graph = build_graph()
        graph.add_prerequisite("statistics", "calculus")
        paths = graph.all_paths("statistics", "optimization")
        self.assertEqual(len(paths), 2)

    def test_all_paths_rejects_boolean_limit(self):
        graph = build_graph()
        with self.assertRaises(ValueError):
            graph.all_paths("algebra", "optimization", max_paths=True)

    def test_cycle_detection(self):
        graph = core.CurriculumGraph()
        graph.add_prerequisite("a", "b")
        graph.add_prerequisite("b", "c")
        graph.add_prerequisite("c", "a")
        self.assertEqual(
            graph.detect_prerequisite_cycles(),
            [["a", "b", "c", "a"]],
        )

    def test_cycle_safe_descendants_do_not_return_start(self):
        graph = core.CurriculumGraph()
        graph.add_prerequisite("a", "b")
        graph.add_prerequisite("b", "a")
        self.assertEqual(graph.descendants("a"), {"b"})

    def test_topological_order_respects_prerequisites(self):
        graph = build_graph()
        order = graph.topological_order()
        self.assertLess(order.index("algebra"), order.index("calculus"))
        self.assertLess(order.index("ml"), order.index("optimization"))

    def test_topological_order_rejects_cycle(self):
        graph = core.CurriculumGraph()
        graph.add_prerequisite("a", "b")
        graph.add_prerequisite("b", "a")
        with self.assertRaises(ValueError):
            graph.topological_order()

    def test_connected_components(self):
        graph = build_graph()
        graph.add_entity("isolated", "Concept")
        components = graph.connected_components()
        self.assertTrue(any(component == {"isolated"} for component in components))

    def test_orphans_across_full_graph(self):
        graph = build_graph()
        graph.add_entity("isolated", "Concept")
        self.assertEqual(graph.orphans(), {"LO3", "K2", "isolated"})

    def test_orphans_can_filter_type(self):
        graph = build_graph()
        graph.add_entity("isolated", "Concept")
        self.assertEqual(
            graph.orphans(entity_type="Concept"),
            {"isolated"},
        )

    def test_bottleneck_detection(self):
        graph = build_graph()
        rows = graph.bottlenecks(min_degree=2)
        ids = {row["entity_id"] for row in rows}
        self.assertIn("optimization", ids)

    def test_assessment_loads(self):
        graph = build_graph()
        graph.add_relation("A1", "ASSESSES", "K1")
        rows = graph.assessment_loads()
        self.assertEqual(rows[0]["target_count"], 2)

    def test_overloaded_assessments(self):
        graph = build_graph()
        graph.add_relation("A1", "ASSESSES", "K1")
        self.assertEqual(
            graph.overloaded_assessments(threshold=1)[0]["assessment"],
            "A1",
        )

    def test_alignment_gaps(self):
        graph = build_graph()
        gaps = graph.alignment_gaps()
        self.assertIn("LO1", gaps["unassessed_outcomes"])
        self.assertIn("LO3", gaps["unassessed_outcomes"])
        self.assertIn("K2", gaps["uncovered_competencies"])

    def test_coverage_summary(self):
        graph = build_graph()
        coverage = graph.coverage_summary()
        self.assertAlmostEqual(
            coverage["learning_outcomes"]["coverage"],
            1 / 3,
        )
        self.assertAlmostEqual(
            coverage["competencies"]["coverage"],
            0.5,
        )

    def test_validate_graph_reports_cycles_and_gaps(self):
        graph = build_graph()
        report = graph.validate_graph()
        self.assertIn("alignment_gaps", report)
        self.assertEqual(report["prerequisite_cycles"], [])

    def test_entities_of_type(self):
        graph = build_graph()
        self.assertEqual(graph.entities_of_type("Program"), {"P1"})

    def test_relation_records_filter(self):
        graph = build_graph()
        rows = graph.relation_records("PREREQUISITE_OF")
        self.assertEqual(len(rows), 4)

    def test_neighbors_can_query_incoming(self):
        graph = build_graph()
        self.assertEqual(
            graph.neighbors(
                "K1",
                relation="ALIGNS_WITH",
                direction="incoming",
            ),
            {"LO1", "LO2"},
        )

    def test_dict_round_trip(self):
        graph = build_graph()
        rebuilt = core.CurriculumGraph.from_records(
            graph.to_dict()["entities"],
            graph.to_dict()["relations"],
        )
        self.assertEqual(rebuilt.to_dict(), graph.to_dict())

    def test_json_round_trip(self):
        graph = build_graph()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "graph.json"
            graph.to_json(path)
            rebuilt = core.CurriculumGraph.from_json(path)
            self.assertEqual(rebuilt.to_dict(), graph.to_dict())

    def test_csv_import(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            entities = directory / "entities.csv"
            relations = directory / "relations.csv"
            entities.write_text(
                "id,type,label,description,domain\n"
                "a,Concept,Algebra,,Mathematics\n"
                "b,Concept,Calculus,,Mathematics\n",
                encoding="utf-8",
            )
            relations.write_text(
                "source,relation,target,confidence,source_type,evidence,reviewed_on\n"
                "a,PREREQUISITE_OF,b,0.9,expert_review,Panel,2026-09-24\n",
                encoding="utf-8",
            )
            graph = core.CurriculumGraph.from_csv(
                entities,
                relations,
            )
            self.assertEqual(graph.descendants("a"), {"b"})
            self.assertEqual(
                graph.entity("a")["metadata"]["domain"],
                "Mathematics",
            )

    def test_bad_review_date_rejected(self):
        graph = core.CurriculumGraph()
        graph.add_concept("a")
        graph.add_concept("b")
        with self.assertRaises(ValueError):
            graph.add_relation(
                "a",
                "PREREQUISITE_OF",
                "b",
                reviewed_on="24-09-2026",
            )


if __name__ == "__main__":
    unittest.main()
