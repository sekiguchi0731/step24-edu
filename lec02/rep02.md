# rep02

## 宿題1

### `delete`関数の実装

#### 実行結果

```
Functional tests passed!
0 0.263718
1 0.470705
2 0.850535
3 1.265877
4 2.354070
5 3.284340
6 4.276555
7 6.105094
8 10.730750
9 7.452860
10 8.203143
11 8.932753
12 9.773539
13 11.300473
14 12.413954
15 13.893585
16 13.400740
17 16.160237
18 15.840439
19 17.402189
20 17.306016
21 22.350814
22 20.193405
23 20.207294
24 22.208018
25 23.060667
26 22.777707
27 25.466514
28 26.657808
29 26.830760
30 30.635449
31 29.522644
32 29.337702
33 31.066089
34 30.051191
35 33.468639
36 32.642064
37 34.048937
38 35.084887
39 45.237792
40 35.451961
41 34.838298
42 43.056191
43 38.100876
44 47.052438
45 44.305828
46 43.667841
47 44.069524
48 52.420155
49 52.785968
50 61.542476
51 48.387272
52 80.610425
53 46.444108
54 49.607067
55 48.000501
56 53.547120
57 51.941896
58 53.599803
59 59.572815
60 61.272443
61 53.293626
62 58.889546
63 58.484761
64 58.606692
65 63.261032
66 62.108316
67 69.910935
68 62.344807
69 63.023444
70 67.450781
71 67.544578
72 65.181361
73 64.792740
74 64.921246
75 66.039746
76 67.514366
77 68.398317
78 70.327662
79 73.879657
80 69.636776
81 62.090967
82 81.288491
83 58.224054
84 60.129901
85 59.177813
86 59.435054
87 60.033428
88 60.848801
89 61.046502
90 61.274574
91 61.281170
92 63.550148
93 69.032449
94 69.890826
95 68.878124
96 67.567274
97 66.158055
98 66.999767
99 68.177922
Performance tests passed!
python3 hash_table.py  7256.78s user 70.36s system 95% cpu 2:07:48.80 total
```

### `calculate_hash(key)`関数の改善

#### なぜ良くないのか

- unicodeの値の和であるため、アナグラム同士で衝突が起こる
  - 衝突回数が増える

#### 改善案1

```python
def calculate_hash(key):
    assert type(key) == str
    hash = 0
    for idx, i in enumerate(key):
        hash += idx * ord(i)
    return hash
```

これをすることで、アナグラムが同じkeyになることは無くなった

しかし、似ている文字だとあまり分散しないことがわかり、調べてみたところ、以下の方法を知った。

#### 改善案2

```python
def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    hash = 0
    prime = 31
    for i in key:
        hash = hash * prime + ord(i) 
    return hash
```

累乗法と呼ばれるらしい

#### 実行結果

```
Functional tests passed!
0 0.141541
1 0.233262
2 0.442551
3 0.634433
4 0.890107
5 1.463651
6 1.894262
7 2.299411
8 2.838852
9 3.354997
10 3.578078
11 3.997570
12 4.315337
13 5.767285
14 5.223390
15 5.402242
16 6.095132
17 6.226888
18 6.912284
19 7.311317
20 7.564164
21 8.122624
22 9.228989
23 8.864746
24 9.445307
25 9.662085
26 10.273865
27 10.345749
28 11.056661
29 11.711907
30 11.572733
31 12.211141
32 12.837137
33 13.437133
34 13.459093
35 13.890037
36 13.930989
37 15.857067
38 15.184528
39 15.286004
40 15.648420
41 16.260106
42 16.357638
43 16.847304
44 17.116591
45 19.041067
46 17.930679
47 18.652035
48 20.146649
49 19.274089
50 20.501043
51 20.427671
52 20.398103
53 20.706543
54 21.128843
55 21.600407
56 22.555049
57 23.085467
58 22.863400
59 24.252648
60 23.668354
61 23.719990
62 25.222950
63 24.628056
64 26.241208
65 25.504551
66 25.761658
67 26.497134
68 26.631673
69 27.049492
70 27.565072
71 30.201878
72 28.621947
73 28.721425
74 29.849176
75 29.836100
76 30.018197
77 31.291282
78 30.725256
79 31.075377
80 31.456230
81 32.102517
82 32.736249
83 34.204439
84 33.740243
85 35.294318
86 35.930142
87 35.269815
88 35.104461
89 35.520879
90 37.363011
91 36.001186
92 36.331044
93 37.412752
94 38.654066
95 37.654995
96 38.513172
97 50.908392
98 38.962821
99 39.541412
ssPerformance tests passed!
python3 hash_table.py  3943.18s user 39.02s system 96% cpu 1:08:40.57 total
```

### リハッシュ関数の実装

#### 案1

```python
    def reput(self, original_size):
        self.item_count = 0
        for i in range(original_size):
            item = self.buckets[i]
            while item:
                self.put(item.key, item.value)
                item = item.next
                
        
    # 要素数がテーブルサイズの70%を上回ったらテーブルサイズを2倍に拡張
    ## put時に検証
    # 要素数がテーブルサイズの30%を下回ったら、テーブルサイズを半分に縮小
    ## delete時に検証
    def rehash(self):
        # 要素数がテーブルサイズの70%を上回ったらテーブルサイズを2倍に拡張
        if self.item_count > self.bucket_size * 0.7:
            # 常に奇数に保つように
            self.buckets += [None] * self.bucket_size + 1
            original_size = self.bucket_size
            self.bucket_size = self.bucket_size * 2 + 1
            self.reput(original_size)
         # 要素数がテーブルサイズの30%を下回ったら、テーブルサイズを半分に縮小
        if self.item_count < self.bucket_size * 0.3:
            original_size = self.bucket_size
            self.bucket_size = self.bucket_size // 2 + 1
            self.reput(original_size)
```

これでは、`rehash()`と`put()`で無限ループが起こってしまい、うまくいかないことがわかった。

#### 案2

```python
    def reput(self, original_size, new_size):
        new_buckets = [None] * new_size
        new_count = 0
        for i in range(original_size):
            item = self.buckets[i]
            if item is not None:
                new_bucket_index = calculate_hash(item.key) % new_size
                new_buckets[new_bucket_index] = item
                new_count += 1
        self.buckets = new_buckets
        self.item_count = new_count
```

`put()`と違う点として、

- 重複のチェックがない
- item.nextのwhile文がない
  - itemをnew_bucketsにいれることで勝手にitem.nextの情報も追加されると思ったため

**問題点**

`performance_test()`にて、最終的なアイテム数が0にならない

**原因**

- bucket_sizeが変われば連結リストも変わるので、`reput()`の再配置のたびに`Item`インスタンスを作り直す必要がある

#### 案3

以下が修正案

```python
    def reput(self, original_size, new_size):
        new_buckets = [None] * new_size
        for i in range(original_size):
            item = self.buckets[i]
            while item is not None:
                new_bucket_index = calculate_hash(item.key) % new_size
                # 新しいバケットにアイテムを挿入
                new_item = Item(item.key, item.value, new_buckets[new_bucket_index])
                new_buckets[new_bucket_index] = new_item
                item = item.next
        self.buckets = new_buckets
        self.bucket_size = new_size
```

#### 実行結果

実行結果は以下

```
Functional tests passed!
0 0.100941
1 0.201465
2 0.111336
3 0.150338
4 0.113876
5 0.060905
6 0.062104
7 0.320182
8 0.056662
9 0.058136
10 0.058686
11 0.135372
12 0.061031
13 0.072880
14 0.540540
15 0.146770
16 0.061155
17 0.059331
18 0.058553
19 0.057377
20 0.058141
21 0.057756
22 0.073610
23 0.181498
24 0.062532
25 0.060185
26 0.061356
27 0.067377
28 1.104646
29 0.058547
30 0.059104
31 0.058894
32 0.062327
33 0.059218
34 0.059658
35 0.057799
36 0.059407
37 0.059294
38 0.057503
39 0.219057
40 0.059996
41 0.059077
42 0.060606
43 0.065168
44 0.063246
45 0.062313
46 0.060327
47 0.061630
48 0.063528
49 0.070324
50 0.065536
51 0.062280
52 0.317795
53 0.061685
54 0.060754
55 0.059866
56 2.108336
57 0.062119
58 0.059464
59 0.058995
60 0.059074
61 0.061212
62 0.058907
63 0.059007
64 0.059478
65 0.061321
66 0.057793
67 0.057274
68 0.057719
69 0.059024
70 0.308343
71 0.060951
72 0.061630
73 0.068908
74 0.063635
75 0.066365
76 0.063490
77 0.074696
78 0.063412
79 0.069128
80 0.065364
81 0.067415
82 0.066595
83 0.066304
84 0.071650
85 0.065114
86 0.068195
87 0.062972
88 0.079635
89 0.087854
90 0.524871
91 0.067073
92 0.061079
93 0.064128
94 0.073533
95 0.070198
96 0.065255
97 0.075729
98 0.074018
99 0.064183
Performance tests passed!
```

## 宿題2

- ハッシュテーブルは、ハッシュ関数やハッシュテーブルなどの大きさを事前に決めておかなければならず、実装に時間がかかるから
- データ数が大規模な場合、テーブルを大きくするか、連結リストを大きくしなければならず、前者の場合は空間容量が大きくなり、後者の場合は探索にかかる計算量や時間が増えるため、ハッシュテーブルの恩恵を受けにくいから

## 宿題3・4

追加・削除が$O(1)$

- リストの特徴

探索が$O(1)$

- ハッシュテーブル(辞書型)の特徴

よって、これらを組み合わせれば良いのではないかと考えた

```python
Urls = []
Url_Page_Dic = {}

# 追加
## a.com: a, b.com:b, ...
Urls.append('a.com')
Url_Page_Dic.setdefault('a.com', a)

# 削除
Url_Page_Dic.pop(Urls[0])
Urls.pop(0)

# 探索
Url_Page_Dic[key]
```

**問題点**

メンターさんより

- pythonの`[]`は$O(1)$ではない
- もしUrlsに含まれているURLに再びアクセスしたら、どういう挙動になるのか？

というご指摘をいただきました。

それを受けて調べたところ、pythonの`[]`は配列、すなわちスタックであり、FIFOであるため、リストの先頭の要素を削除するのにかかる計算量は、実際には$O(1)$ではないことがわかりました。

したがって、pythonの`collections`モジュールの`deque`などを用いて、キューで実装した方が良いと思いました。

擬似コードは以下です

```python
# 用意するデータ
アクセスしたURLを格納するdeque = deque([])
{key=URL: value=HTMLファイル}となる辞書1 = {}
{key=URL: value=キューに格納した数}となる辞書2 = {}

# 'a.com'にアクセスし、そのhtmlファイルが'a.html'だった場合

current_count = 辞書2.setdefault('a.com', 1)
# 'a.com'がキューに一つも存在しない場合
if current_count == 1:
  辞書1['a.com'] = 'a.html'
# 一つ以上存在する場合
else:
  辞書2['a.com'] += 1 
deque.append('a.com')
# 長さが指定された長さを超える場合
if len(辞書1) > N:
  last_el = deque.popleft()
  while 辞書2[last_el] > 1:
    辞書2[last_el] -= 1
    last_el = deque.popleft()
  辞書1.pop(last_element)
  辞書2.pop(last_element)
```