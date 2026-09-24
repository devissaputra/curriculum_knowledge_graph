from collections import defaultdict, deque


class CurriculumGraph:
    """Small directed graph where edges point from prerequisites to later concepts."""

    def __init__(self):
        self.edges = defaultdict(set)
        self.nodes = set()

    def add_concept(self, concept: str) -> None:
        if not concept:
            raise ValueError("concept must not be empty")
        self.nodes.add(concept)

    def add_prerequisite(self, prerequisite: str, concept: str) -> None:
        if not prerequisite or not concept:
            raise ValueError("concept names must not be empty")
        if prerequisite == concept:
            raise ValueError("a concept cannot be its own direct prerequisite")
        self.nodes.update([prerequisite, concept])
        self.edges[prerequisite].add(concept)

    def descendants(self, start: str) -> set[str]:
        """Return concepts reachable from start without returning start itself."""
        if start not in self.nodes:
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

    def orphans(self) -> set[str]:
        """Return registered concepts with no incoming or outgoing prerequisite edge."""
        incoming = set()
        outgoing = set(self.edges)
        for targets in self.edges.values():
            incoming.update(targets)
        return self.nodes - incoming - outgoing
