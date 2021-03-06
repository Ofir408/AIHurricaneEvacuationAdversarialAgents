from typing import Tuple

from bl.search_tree.IGeneralSearchTree import IGeneralSearchTree
from bl.search_tree.heuristic_functions.IHueristicFunc import IHueristicFunc
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Edge import Edge
from data_structures.State import State
from data_structures.Vertex import Vertex


class AStarSearchTree(IGeneralSearchTree):

    def __init__(self, heuristic_func: IHueristicFunc, limit: int = 10000):
        super().__init__()
        self.__heuristic_func = heuristic_func
        self.__limit = limit

    def goal_test(self, problem: Tuple[State, State, EnvironmentConfiguration], current_state: State):
        if self._expansions_num >= self.__limit:
            self._was_terminate = True
        _, goal_state, _ = problem
        return goal_state.get_required_vertexes() == current_state.get_required_vertexes()

    def step_cost(self, parent_node: Vertex, action: Edge, new_node: Vertex) -> int:
        g_value = action.get_weight()  # weights until g was calculated within get_next_vertex
        h_value = self.__heuristic_func.calc_estimation_from_goal(new_node.get_state(), None)
        return g_value + h_value


