import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from curriculum_knowledge_graph import core


class CoreTests(unittest.TestCase):
    def test_reachability_and_orphans(self):
        graph = core.CurriculumGraph()
        graph.add_prerequisite("a", "b")
        graph.add_prerequisite("b", "c")
        graph.add_concept("isolated")
        self.assertEqual(graph.descendants("a"), {"b", "c"})
        self.assertEqual(graph.orphans(), {"isolated"})

    def test_cycle_does_not_return_start(self):
        graph = core.CurriculumGraph()
        graph.add_prerequisite("a", "b")
        graph.add_prerequisite("b", "a")
        self.assertEqual(graph.descendants("a"), {"b"})


if __name__ == "__main__":
    unittest.main()
