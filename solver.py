from dataclasses import dataclass
from os import path
from os.path import dirname
from typing import List, Optional


class Item:
    def __init__(self, value: int, weight: int, value_to_weight: float = None):
        self.value: int = value
        self.weight: int = weight
        self.value_to_weight: float = value / weight if value_to_weight is None else value_to_weight


@dataclass
class Node:
    level: int
    included_items_indexes: List[int]


class Solver:
    def __init__(self, max_weight: int, items: List[Item]):
        self.max_weight: int = max_weight
        self.items: List[Item] = sorted(items, key=lambda el: el.value_to_weight, reverse=True)
        self.items.insert(0, Item(value=0, weight=0, value_to_weight=0))

        self.best_profit: int = 0
        self.possible_solutions: List[Node] = []

    def solve(self) -> None:
        def _recursion_step(current_root: Node):
            if self._get_upper_bound(current_root) < self.best_profit or self._is_infeasible(current_root):
                return

            current_node_profit = sum((self.items[i].value for i in current_root.included_items_indexes))
            if current_node_profit > self.best_profit:
                self.best_profit = current_node_profit

            if current_root.level == len(self.items) - 1:
                self.possible_solutions.append(current_root)
                return

            left_node = Node(level=current_root.level + 1,
                             included_items_indexes=current_root.included_items_indexes + [current_root.level + 1])

            right_node = Node(level=current_root.level + 1,
                              included_items_indexes=current_root.included_items_indexes[:])

            _recursion_step(left_node)
            _recursion_step(right_node)

        dummy_node = Node(level=0, included_items_indexes=[])
        _recursion_step(dummy_node)

        return self._get_best_solution()

    def _get_upper_bound(self, node: Node) -> float:
        value = sum((self.items[i].value for i in node.included_items_indexes))
        weight = sum((self.items[i].weight for i in node.included_items_indexes))

        if node.level == len(self.items) - 1:
            next_element = Item(value=0, weight=0, value_to_weight=0)
        else:
            next_element = self.items[node.level + 1]

        return value + (self.max_weight - weight) * next_element.value_to_weight

    def _is_infeasible(self, node: Node) -> bool:
        return sum((self.items[i].weight for i in node.included_items_indexes)) > self.max_weight

    def _get_best_solution(self) -> Optional[int]:
        if not self.possible_solutions:
            return None

        values = [sum((self.items[i].value for i in node.included_items_indexes)) for node in self.possible_solutions]
        return max(values)


if __name__ == "__main__":
    file_name = "ks_50_1"

    with open(path.join(dirname(__file__), "data", file_name)) as input_file:
        meta_data, *data = input_file.read().splitlines()
        _, max_weight = meta_data.split()

        split_lines = [line.split() for line in data]
        items = [Item(value=int(value), weight=int(weight)) for value, weight in split_lines]

    solver = Solver(max_weight=int(max_weight_), items=items_)
    print(solver.solve())
