import itertools
import math

from utils import Day, aoc_main


def steps_to_reach(instructions, nodes, start_nodes, end_nodes):
    for target_node in start_nodes:
        node = target_node
        for step, ins in enumerate(itertools.cycle(instructions)):
            if node in end_nodes:
                yield step
                break
            node = nodes[node][ins]


class Day08(Day):
    def parse(self, input: str):
        inp = input.strip()
        instructions_block, nodes_block = inp.split("\n" * 2)

        instructions_block = instructions_block.replace("L", "0").replace("R", "1")
        instructions = [int(ins) for ins in list(instructions_block)]

        nodes = {}
        for line in nodes_block.splitlines():
            line = (
                line.replace(" = ", " ")
                .replace("(", "")
                .replace(")", "")
                .replace(",", "")
            )
            node, node_l, node_r = line.split()
            nodes[node] = (node_l, node_r)

        return instructions, nodes

    def part1(self, parsed):
        instructions, nodes = parsed
        start_nodes = ["A" * 3]
        end_nodes = ["Z" * 3]
        res = steps_to_reach(instructions, nodes, start_nodes, end_nodes)
        return next(res)

    def part2(self, parsed):
        instructions, nodes = parsed
        start_nodes = [node for node in nodes if node.endswith("A")]
        end_nodes = [node for node in nodes if node.endswith("Z")]
        res = steps_to_reach(instructions, nodes, start_nodes, end_nodes)
        return math.lcm(*res)


if __name__ == "__main__":
    aoc_main(Day08)
