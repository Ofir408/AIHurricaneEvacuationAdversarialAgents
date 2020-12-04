from abc import ABC
from collections import deque
from typing import Tuple, List

from bl.agents.IAgent import IAgent
from bl.search_tree.IGeneralSearchTree import IGeneralSearchTree
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.Edge import Edge
from data_structures.State import State
from data_structures.Vertex import Vertex
from utils.EnvironmentUtils import EnvironmentUtils


class ITreeSearchAgent(IAgent, ABC):

    TRAVELLING = "TRAVELLING"

    def __init__(self, search_tree_algo: IGeneralSearchTree):
        super().__init__()
        self._search_tree_algo = search_tree_algo
        self._path_queue = deque()

    def get_action(self, percepts: Tuple[State, EnvironmentConfiguration]) -> str:
        if self.is_travelling():
            self._distance_left_to_travel -= 1  # Travel this step
            return ITreeSearchAgent.TRAVELLING

        if len(self._path_queue) == 0:
            was_path_found = self.__init_path(percepts)
            if not was_path_found:
                print("path not found")
                self._was_terminated = True
                return IGeneralSearchTree.SOLUTION_NOT_FOUND
        edge_name = self._path_queue.popleft()
        env_config = percepts[1]
        self._distance_left_to_travel = env_config.get_edges()[edge_name].get_weight()
        return edge_name

    def __init_path(self, percepts: Tuple[State, EnvironmentConfiguration]):
        self._path_queue.clear()
        vertexes_path = self._get_path(percepts)
        for vertex in vertexes_path:
            edge = vertex.get_action()
            if edge is not None:
                self._path_queue.append(edge)
        was_path_found = len(self._path_queue) > 0
        return was_path_found

    def _get_path(self, percepts: Tuple[State, EnvironmentConfiguration]) -> List[Vertex]:
        initial_state, env_config = percepts
        goal_state = EnvironmentUtils.get_goal_state(env_config)
        solution_vertex, was_path_found = self._search_tree_algo.search((initial_state, goal_state, env_config), [])
        vertexes_path, cost = self._search_tree_algo.restore_solution(solution_vertex, env_config)
        return vertexes_path

    def step_cost(self, parent_node: Vertex, action: Edge, new_node: Vertex) -> int:
        return self._search_tree_algo.step_cost(parent_node, action, new_node)
