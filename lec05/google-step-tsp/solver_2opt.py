import sys

from common import print_tour, read_input, read_output, write_tour
from solver_greedy import distance


def solve(city_dists: list[tuple[float, float]], cities_indexes: list[int]) -> list[int]:
    n: int = len(cities_indexes)
    cities_indexes.append(cities_indexes[0])
    new_cities: list[int] = cities_indexes
    for num in range(10000):
        improvement: bool = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                # 両端は変化させない
                if i == 0 or j == n - 1:
                    continue

                # 検査するインデックスの代入
                i_idx, i_next_idx = new_cities[i], new_cities[i + 1]
                j_idx, j_next_idx = new_cities[j], new_cities[j + 1]
                print("検査するi:" + str(i_idx))
                print("検査するj:" + str(j_idx))
                current_sum: float = (
                    distance(city_dists[i_idx], city_dists[i_next_idx])
                    + distance(city_dists[j_idx], city_dists[j_next_idx])
                )
                
                # i-j, i+1-j+1の距離計算
                new_sum1: float = (
                    distance(city_dists[i_idx], city_dists[j_idx])
                    + distance(city_dists[i_next_idx], city_dists[j_next_idx])
                )
                # i-j+1, i+1-jの距離計算
                new_sum2: float = (
                    distance(city_dists[i_idx], city_dists[j_next_idx])
                    + distance(city_dists[i_next_idx], city_dists[j_idx])
                )
                # 現在の距離が新しい距離のいずれかより大きいとき、改善する
                if min(new_sum1, new_sum2) < current_sum:
                    improvement = True
                    if new_sum1 < new_sum2:
                        new_cities[i + 1 : j + 1] = reversed(new_cities[i + 1 : j + 1])
                    else:
                        new_cities[i : j + 1] = reversed(new_cities[i : j + 1])

        if not improvement:
            print(str(num) + "で終わった")
            break
        else:
            cities_indexes = new_cities

    return cities_indexes[:-1]


if __name__ == "__main__":
    assert len(sys.argv) > 3
    tour: list[int] = solve(read_input(sys.argv[1]), read_output(sys.argv[2]))
    # print_tour(tour)
    print(tour)
    write_tour(sys.argv[3], tour)