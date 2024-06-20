import math
import random
import sys

from common import read_input, read_output, write_tour
from solver_greedy import distance


def simulated_annealing(
    city_dists: list[tuple[float, float]], cities_indexes: list[int]
) -> list[int]:
    n: int = len(cities_indexes)
    cities_indexes.append(cities_indexes[0])
    current_cities: list[int] = cities_indexes[:]
    best_cities: list[int] = current_cities[:]

    def total_distance(solution) -> float:
        return sum(
            distance(city_dists[solution[i]], city_dists[solution[i + 1]])
            for i in range(len(solution) - 1)
        )
    
    current_sum: float = total_distance(current_cities)
    best_sum: float = current_sum

    initial_temperature = 100.0
    final_temperature = 1.0
    alpha = 0.995
    temperature: float = initial_temperature

    while temperature > final_temperature:
        for i in range(1, n - 1):
            for j in range(i + 2, n):
                new_cities: list[int] = best_cities[:]

                # 検査するインデックスの代入
                i_idx: int= new_cities[i]
                j_idx: int = new_cities[j]

                new_cities[i_idx + 1:j_idx + 1] = reversed(new_cities[i_idx + 1:j_idx + 1])
                new_sum: float = total_distance(new_cities)

                # 新しい解が良い場合は受け入れる
                if new_sum < current_sum:
                    new_cities = new_cities[:]
                    current_sum = new_sum
                    if new_sum < best_sum:
                        best_cities = new_cities[:]
                        best_sum = new_sum
                else:
                    # 新しい解が悪化する場合は確率的に受け入れる
                    acceptance_probability: float = math.exp(
                        (current_sum - new_sum) / temperature
                    )
                    if acceptance_probability > random.random():
                        current_cities = new_cities[:]
                        current_sum = new_sum

        temperature *= alpha

    return best_cities[:-1]


if __name__ == "__main__":
    assert len(sys.argv) > 3
    # % python3 solver_2opt.py input_n.csv sample/greedy_n.csv output_n.csv
    tour: list[int] = simulated_annealing(read_input(sys.argv[1]), read_output(sys.argv[2]))
    print(tour)
    write_tour(sys.argv[3], tour)
