# プログラミング作法

## デバッグ

## モジュール化

## 宿題

### 型推論

調べていく中で、型推論が大切であることを知った

そこで、まず、`token`ハッシュテーブルの値として受け取れるものを、`'NUMBER'`や`'PLUS'`などに制限したいと考えた

#### Pythonで有限個数のリテラル値だけを許す型を定義

```python
Color = ['red', 'blue', 'yellow']
```

##### リテラルとは

1や "x" などの生のデータ

##### 宿題での活用

```python
# 型宣言
Operator = Literal['NUMBER', 'PLUS', 'MINUS']
KeyType = Literal['type', 'number']
Token = dict[KeyType, Union[Operator, float]]
```

##### 問題点

- Tokenのvalueが`Operator|float`となり、`float`である確証がないため計算ができない！
- そもそも、`Number`の時だけ要素が2となる辞書型はあまり綺麗ではないのではないか

##### 解決策

- 型の安全性を確保することが目的  
  - 型列挙で演算子を、`float`型のインスタンスとして`number`を保持すれば良いのではないか

#### クラスを用いた型列挙を定義

```python
# 型宣言
## 型列挙
class Operator(Enum):
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    OVER = auto()


## 数値のためのクラス
@dataclass
class Number:
    data: float


Token = Operator | Number
```

##### `auto()`とは

型列挙において、連番のアドレスを自動的に付与するための関数

##### `@dataclass`とは

`@`：デコレータ。クラスに機能を追加するために使用する

`@dataclass`の役割：

1. data はクラス変数じゃなくてインスタンス変数として定義される
2. コンストラクタを自動で生成する
3. `==`や文字列変換のためのメソッドの定義を自動で生成している

##### なぜ`float`ではなく`Number`のインスタンスとして定義するのか

統語論を考えると、`Token`の並列としてあげるのは両方クラスで揃えたほうが綺麗だから

<br>

### 割り算、掛け算の機能追加

```python
def evaluate(tokens) -> float:
    answer = 0
    tokens.insert(0, {"type": "PLUS"})  # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "NUMBER":
            if tokens[index - 1]["type"] == "PLUS":
                answer += tokens[index]["number"]
            elif tokens[index - 1]["type"] == "MINUS":
                answer -= tokens[index]["number"]
            else:
                print("Invalid syntax")
                exit(1)
        index += 1
    return answer
```

`evaluate(tokens)`関数内で、以下の機能を追加する必要がある

- *、/の時計算をして+、-、numberだけのtokensに書き換える

そのために、以下のように仕様を変える

1段階目の計算：

- *または/ を探す
  - あれば、tokenを書き換える
- +または-の計算をする

2段階目の計算：

- +または-の計算をする


### 括弧の機能追加

具体的ににどのような挙動をさせれば良いか考える

${4.0-(2*(3-1)+5)}$のとき、

```python
tokens: list[Token] = [N(4.0), O.M, O.L, N(2), O.T, O.L, N(3), O.M, N(1), O.R, O.P, N(5), O.R]
```

となる。

まず${(3-1)}$を計算するために`evaluate([N(3), O.M, N(1)])`を実行

したがって、`[N(3), O.M, N(1)]`を切り取る方法を考える

前から見ていって、`O.R`がきたらその後ろから切り取り、直後の`O.L`までを計算して`Number`のインスタンスとして元のリストに挿入するような関数があれば良い

→再帰

#### メンターさんからのアドバイス

`rindex`のポインタを後ろから見た方が良いのでは？

- リストの要素数が1なら、その中身を返す
- 一番外側の`()`を見つけたら、`()`の中身のリストを切り取って`evaluate_parentheses()`に再帰する
- `()`が見つからなければ、渡されたリストを`evaluate()`に渡す

#### 新しい関数の定義

今までの`evaluate_parentheses()`は。リスト全体と回していく中で最も右側にある左括弧のインデックス。右括弧を探すポインタのインデックスを受け取って、最も左側にある右括弧を見つけたら、そのリストを`evaluate()`に渡して計算し、その結果を用いてリスト全体を更新し、最後に括弧なしのリストを返していた

**問題点**

`evaluate()`は最後にも途中にも使うのに、操作を分けているのがわかりにくい！

一般的でない操作のため、わかりにくい

そこで、`Token`型のリストを受け取って小数を返す以下の関数を定義する

- リストの要素数が1ならばそれを`evaluate()`にわたした小数を返す
- 左かっこを見つけるまで`lindex`をインクリメント
- 右括弧を見つけるまで`rindex`をデクリメント
- かっこがあるならば括弧の中身を再帰する
- かっこがなければ、`evaluate()` に渡して返ってきた小数を返す