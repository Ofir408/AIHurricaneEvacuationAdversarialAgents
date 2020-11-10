from bl.Simulator import Simulator
from bl.agents.part1.GreedyAgent import GreedyAgent
from bl.agents.part1.HumanAgent import HumanAgent
from bl.agents.part1.SaboteurAgent import SaboteurAgent
from configuration_reader.EnvironmentConfiguration import EnvironmentConfiguration
from data_structures.State import State
from utils.EnvironmentUtils import EnvironmentUtils


class Runner:

    def run(self, env_config: EnvironmentConfiguration):
        agents = [HumanAgent(), GreedyAgent(), SaboteurAgent(env_config.get_vertices_num())]
        chosen_agents = []
        states = []
        for _ in range(2):
            agent_num = int(input("Choose Agent: \n 1) Human Agent\n 2) Greedy Agent\n 3) Saboteur agent\n"))
            while agent_num > 4 or agent_num < 1:
                print("Invalid agent number")
                agent_num = input("Choose Agent: \n 1) Human Agent\n 2) Greedy Agent\n 3) Saboteur agent\n")
            chosen_agents.append(agents[agent_num - 1])
            EnvironmentUtils.print_environment(env_config)
            initial_state_name = input("Choose initial state\n")
            states.append(State(initial_state_name, EnvironmentUtils.get_required_vertexes(env_config)))

        simulator = Simulator()
        scores = simulator.run_simulate(chosen_agents, simulator.update_func, simulator.terminate_func,
                                        simulator.performance_func, env_config, states)
        print("--------------------------------------")
        print("Scores:")
        print(scores)
