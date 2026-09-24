import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from curriculum_knowledge_graph.core import CurriculumGraph


graph = CurriculumGraph.from_csv(
    ROOT / "data" / "entities.csv",
    ROOT / "data" / "relations.csv",
)

report = graph.validate_graph()

print("Curriculum Knowledge Graph synthetic demo")
print()
print("Graph size:")
print(
    {
        "entities": report["entity_count"],
        "relations": report["relation_count"],
        "entity_types": {
            entity_type: len(graph.entities_of_type(entity_type))
            for entity_type in (
                "Program",
                "Course",
                "Module",
                "Concept",
                "LearningOutcome",
                "Competency",
                "Assessment",
                "Resource",
            )
        },
    }
)

print("\nPrerequisite diagnostics:")
print("cycles:", report["prerequisite_cycles"])
print(
    "direct prerequisites of recommender systems:",
    sorted(
        graph.direct_prerequisites(
            "concept.recommender_systems"
        )
    ),
)
print(
    "all ancestors of recommender systems:",
    sorted(graph.ancestors("concept.recommender_systems")),
)

print("\nPath reasoning:")
print(
    "shortest statistics -> recommender systems:",
    graph.shortest_path(
        "concept.statistics",
        "concept.recommender_systems",
    ),
)
print(
    "alternative statistics -> recommender systems paths:",
    graph.all_paths(
        "concept.statistics",
        "concept.recommender_systems",
        max_paths=10,
    ),
)

print("\nStructural diagnostics:")
print("orphans:", report["orphans"])
print("bottlenecks:", graph.bottlenecks(min_degree=4))
print(
    "overloaded assessments:",
    graph.overloaded_assessments(threshold=3),
)

print("\nAlignment gaps:")
for name, values in report["alignment_gaps"].items():
    print(name, values)

print("\nCoverage summary:")
for name, values in report["coverage"].items():
    printable = dict(values)
    if printable["coverage"] is not None:
        printable["coverage"] = round(
            printable["coverage"],
            3,
        )
    print(name, printable)

try:
    graph.topological_order()
except ValueError as exc:
    print("\nTopological sequence on full graph:", str(exc))

clean_relations = [
    row
    for row in graph.to_dict()["relations"]
    if row["evidence"] != "Deliberate synthetic cycle edge"
]
clean_graph = CurriculumGraph.from_records(
    graph.to_dict()["entities"],
    clean_relations,
)
clean_order = clean_graph.topological_order()
print(
    "Topological sequence after removing deliberate cycle:",
    clean_order,
)

print(
    "\nNote: all entities, relations, provenance records, and alignment "
    "issues are synthetic. The demo verifies graph reasoning and curriculum "
    "diagnostics; it does not establish that these prerequisite or alignment "
    "claims are pedagogically correct in a real program."
)
