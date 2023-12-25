from collections import Counter
import math
from typing import Any
import more_itertools

import networkx
from utils import *


tests = [
    test(
        """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""
    ),
]


@runs(
    *tests,
    submit,
)
def a(inp: Input) -> Any:
    graph = networkx.Graph()
    all_nodes = set()
    for line in inp.lines:
        name, connections = line.split(": ")
        for connection in connections.split():
            graph.add_edge(name, connection)
            all_nodes.add(name)
            all_nodes.add(connection)

    counter = Counter()

    # we need this function so we can count both (a, b) and (b, a) as the same edge
    def shs(s1: str, s2: str, /) -> tuple[str, str]:
        if s1 < s2:
            return s1, s2
        return s2, s1

    # since this is aoc, the graph is guaranteed to be fully connected and need exactly 3 edges removed
    # this means we can simply find the "most commonly traversed" edges
    # count all the edges by traversing from everywhere to everywhere
    for path in networkx.all_pairs_dijkstra_path(graph):
        for p in path[1].values():
            for node in more_itertools.sliding_window(p, 2):
                counter[shs(*node)] += 1

    for node in counter.most_common(3):
        graph.remove_edge(*node[0])

    return math.prod(map(len, networkx.connected_components(graph)))
