import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from curriculum_knowledge_graph.core import CurriculumGraph

g=CurriculumGraph(); g.add_prerequisite('algebra','calculus'); g.add_prerequisite('calculus','optimization')
print('Concepts reachable from algebra:', ', '.join(sorted(g.descendants('algebra'))))
