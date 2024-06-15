import sys

from common import read_input, read_output, write_tour
from solver_greedy import distance


def solve(city_dists: list[tuple[float, float]], cities_indexes: list[int]) -> list[int]:
    n: int = len(cities_indexes)
    cities_indexes.append(cities_indexes[0])
    new_cities: list[int] = cities_indexes[:]
    improvement: bool = True
    while improvement:
        improvement = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                # 両端は変化させない
                if i == 0 or j == n - 1:
                    continue

                # 検査するインデックスの代入
                i_idx, i_next_idx = new_cities[i], new_cities[i + 1]
                j_idx, j_next_idx = new_cities[j], new_cities[j + 1]

                current_sum: float = (
                    distance(city_dists[i_idx], city_dists[i_next_idx])
                    + distance(city_dists[j_idx], city_dists[j_next_idx])
                )
                # i-j, i+1-j+1の距離計算
                new_sum1: float = (
                    distance(city_dists[i_idx], city_dists[j_idx])
                    + distance(city_dists[i_next_idx], city_dists[j_next_idx])
                )
                print(f'今の距離：{current_sum} 更新後の距離:{new_sum1}')
                # 現在の距離が新しい距離より大きいとき、改善する
                if new_sum1 < current_sum:
                    print(f"検査しているインデックス： {i_idx}, {j_idx}")
                    print(new_cities)
                    improvement = True
                    new_cities[i + 1 : j + 1] = reversed(new_cities[i + 1 : j + 1])
                    print(new_cities)
                    break
            if improvement:
                break
        if not improvement:
            break
        else:
            cities_indexes = new_cities[:]

    return cities_indexes[:-1]


if __name__ == "__main__":
    assert len(sys.argv) > 3
    tour: list[int] = solve(read_input(sys.argv[1]), read_output(sys.argv[2]))
    print(tour)
    write_tour(sys.argv[3], tour)