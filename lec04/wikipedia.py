import sys
from collections import deque


class Wikipedia:
    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file) -> None:
        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles: dict[int, str] = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links: dict[int, list[int]] = {}

        # A mapping from a page ID (integer) to the page rank (float).
        # For example, self.page_ranks[1234] returns the page rank of the
        # page whose ID is 1234
        self.page_ranks: dict[int, float] = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert id not in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self) -> None:
        titles: list[str] = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Find the most linked pages.
    def find_most_linked_pages(self) -> None:
        link_count: dict[int, int] = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max: int = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start: str, goal: str) -> None:
        for id, title in self.titles.items():
            if title == start:
                start_id: int = id
            elif title == goal:
                goal_id: int = id

        bfs_que: deque[dict[int, list[int]]] = deque([{start_id: [start_id]}])
        visited_ln: list[int] = [start_id]
        # 空でない限り回す
        while not len(bfs_que) == 0:
            popped_dict: dict[int, list[int]] = bfs_que.popleft()
            popped_id: int = next(iter(popped_dict))
            popped_list: list[int] = next(iter(popped_dict.values()))

            if popped_id == goal_id:
                print("found")
                show_list: list[str] = []
                for way in popped_list:
                    show_list.append(self.titles[way])
                print("最短経路：" + "→".join(show_list))
                return
            # goal_idでないなら追加する
            for id in self.links[popped_id]:
                if id not in visited_ln:
                    print("new push to que!" + str(id))
                    bfs_que.append({id: popped_list + [id]})
                    visited_ln.append(id)

        print("not found")
        return

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self) -> None:
        # 初期化
        for id in self.titles:
            self.page_ranks[id] = 1
        id_total: int = len(self.page_ranks)
        # 分配
        for _ in range(10):
            print("in")
            ## ページランク一時保存用
            temp_page_ranks: dict[int, float] = {}
            for target_id, target_page_rank in self.page_ranks.items():
                print(str(target_id))
                linked_id_count: int = len(self.links[target_id])
                unlinked_id_count: int = id_total - linked_id_count
                for id in self.page_ranks:
                    if id in self.links[target_id]:
                        temp_page_ranks[id] = (
                            temp_page_ranks.get(id, 0)
                            + 0.85 * target_page_rank / linked_id_count
                        )
                    else:
                        temp_page_ranks[id] = (
                            temp_page_ranks.get(id, 0)
                            + 0.15 * target_page_rank / unlinked_id_count
                        )
            self.page_ranks = temp_page_ranks
        print(self.page_ranks.values())
        print(str(sum(self.page_ranks.values())))
        popular_order_id_list: list[int] = sorted(
            self.page_ranks.keys(), key=lambda id: self.page_ranks[id], reverse=True
        )
        for idx, id in enumerate(popular_order_id_list):
            if idx < 5:
                print(str(idx + 1) + ". " + self.titles[id])
            else:
                break

    # Do something more interesting!!
    def find_something_more_interesting(self) -> None:
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # wikipedia.find_shortest_path("B", "E")
    wikipedia.find_most_popular_pages()
