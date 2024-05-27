#! /usr/bin/python3
from dataclasses import dataclass
from enum import Enum, auto


# 型宣言
## 型列挙
class Operator(Enum):
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    OVER = auto()
    LEFT = auto()
    RIGHT = auto()
    ABS = auto()
    INT = auto()
    ROUND = auto()


## 数値のためのクラス
@dataclass
class Number:
    data: float


Token = Operator | Number


def read_number(line: str, index: int) -> tuple[Token, int]:
    number = 0
    while index < len(line) and line[index].isdigit():
        number: float = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == ".":
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token: Token = Number(number)
    return token, index


def read_plus(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.PLUS
    return token, index + 1


def read_minus(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.MINUS
    return token, index + 1


def read_times(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.TIMES
    return token, index + 1


def read_over(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.OVER
    return token, index + 1


def read_left(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.LEFT
    return token, index + 1


def read_right(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.RIGHT
    return token, index + 1

def read_abs(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.ABS
    return token, index + 3


def read_int(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.INT
    return token, index + 3


def read_round(line: str, index: int) -> tuple[Token, int]:
    token: Token = Operator.ROUND
    return token, index + 5


# タプルのアンパック時に直接型注釈を追加することはできない
def tokenize(line: str) -> list[Token]:
    tokens: list[Token] = []
    index: int = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == "+":
            (token, index) = read_plus(line, index)
        elif line[index] == "-":
            (token, index) = read_minus(line, index)
        elif line[index] == "*":
            (token, index) = read_times(line, index)
        elif line[index] == "/":
            (token, index) = read_over(line, index)
        elif line[index] == "(":
            (token, index) = read_left(line, index)
        elif line[index] == ")":
            (token, index) = read_right(line, index)
        elif line[index] == "a":
            (token, index) = read_abs(line, index)
        elif line[index] == "i":
            (token, index) = read_int(line, index)
        elif line[index] == "r":
            (token, index) = read_round(line, index)
        else:
            print("Invalid character found: " + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_plus(tokens: list[Token], index: int, answer: float) -> float:
    answer += tokens[index + 1].data  # type: ignore
    return answer


def evaluate_minus(tokens: list[Token], index: int, answer: float) -> float:
    answer -= tokens[index + 1].data  # type: ignore
    return answer


def evaluate_times(tokens: list[Token], index: int) -> tuple[list[Token], int]:
    if not isinstance(tokens[index - 1], Number) or not isinstance(
        tokens[index + 1], Number
    ):
        print("Error!\n")
    else:
        num1: float = tokens[index - 1].data  # type: ignore
        num2: float = tokens[index + 1].data  # type: ignore
        tokens[index - 1] = Number(num1 * num2)
        tokens = tokens[0:index] + tokens[index + 2 :]
    return tokens, index - 2


def evaluate_over(tokens: list[Token], index: int) -> tuple[list[Token], int]:
    if not isinstance(tokens[index - 1], Number) or not isinstance(
        tokens[index + 1], Number
    ):
        print("Error!\n")
    else:
        num1: float = tokens[index - 1].data  # type: ignore
        num2: float = tokens[index + 1].data  # type: ignore
        tokens[index - 1] = Number(num1 / num2)
        tokens = tokens[0:index] + tokens[index + 2 :]
    return tokens, index - 2


def evaluate_parentheses(tokens: list[Token], lindex: int, rindex: int) -> list[Token]:
    # 再帰の終点
    if rindex >= len(tokens):
        return tokens
    elif tokens[rindex] == Operator.RIGHT:
        # 直前の(...)を(tokens)にして、evaluateに渡して計算し、
        # その答えをNumberのインスタンスにしてリストの一要素として足して返す
        print("left:" + str(lindex) + " right:" + str(rindex))
        print(tokens[lindex - 1])
        print(tokens[lindex + 1 : rindex])
        answer: float = evaluate(tokens[lindex + 1 : rindex])
        print("right" + str(answer))
        if tokens[lindex - 1] == Operator.ABS:
            answer = abs(answer)
            lindex -= 1
        elif tokens[lindex - 1] == Operator.INT:
            answer = int(answer)
            lindex -= 1
        elif tokens[lindex - 1] == Operator.ROUND:
            answer = round(answer)
            lindex -= 1
        else:
            pass
        calculated_token: list[Token] = (
            tokens[:lindex] + [Number(answer)] + tokens[rindex + 1 :]
        )
        print(calculated_token)
        return evaluate_parentheses(calculated_token, 0, 0)
    elif tokens[rindex] == Operator.LEFT:
        # (の次を初項とするリストに関して、evaluate_parenthesesを回す
        print("left")
        return evaluate_parentheses(tokens, rindex, rindex + 1)
    else:
        # leftがあるまで回す
        print("else" + str(rindex))
        return evaluate_parentheses(tokens, lindex, rindex + 1)


def evaluate(tokens: list[Token]) -> float:
    answer: float = 0
    # Insert a dummy '+' token
    if tokens[0] == Operator.MINUS:
        tokens = [Number(0)] + tokens
    else:
        tokens = [
            Number(0),
            Operator.PLUS,
        ] + tokens
    print(tokens)
    print("here")
    index: int = len(tokens) - 1
    # 掛け算と割り算
    while index > 1:
        if tokens[index] == Operator.TIMES:
            tokens, index = evaluate_times(tokens, index)
        elif tokens[index] == Operator.OVER:
            tokens, index = evaluate_over(tokens, index)
        else:
            index -= 1
    # 足し算と引き算
    index = 1
    while index < len(tokens):
        if tokens[index] == Operator.PLUS:
            answer = evaluate_plus(tokens, index, answer)
        elif tokens[index] == Operator.MINUS:
            answer = evaluate_minus(tokens, index, answer)
        else:
            pass
        index += 1
    return answer


def test(line: str) -> None:
    tokens: list[Token] = tokenize(line)
    print(tokens)
    tokens = evaluate_parentheses(tokens, 0, 0)
    actual_answer: float = evaluate(tokens)
    expected_answer: float = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print(
            "FAIL! (%s should be %f but was %f)"
            % (line, expected_answer, actual_answer)
        )


# Add more tests to this function :)
def run_test() -> None:
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0+2.1*3")
    test("1.0+((2-1)*3-2)")
    test("3/2+1.5-(2+3*(5-1))")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")
    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line: str = input()
    tokens: list[Token] = tokenize(line)
    tokens = evaluate_parentheses(tokens, 0, 0)
    answer: float = evaluate(tokens)
    print("answer = %f\n" % answer)
