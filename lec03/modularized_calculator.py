#! /usr/bin/python3
from typing import Literal, Union

# 型宣言
Operator = Literal["NUMBER", "PLUS", "MINUS", "TIMES", "OVER"]
KeyType = Literal["type", "number"]
Token = dict[KeyType, Union[Operator, float]]


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
    token: Token = {"type": "NUMBER", "number": number}
    return token, index


def read_plus(line: str, index: int) -> tuple[Token, int]:
    token: Token = {"type": "PLUS"}
    return token, index + 1


def read_minus(line: str, index: int) -> tuple[Token, int]:
    token: Token = {"type": "MINUS"}
    return token, index + 1


def read_times(line: str, index: int) -> tuple[Token, int]:
    token: Token = {"type": "TIMES"}
    return token, index + 1


def read_over(line: str, index: int) -> tuple[Token, int]:
    token: Token = {"type": "OVER"}
    return token, index + 1


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
        else:
            print("Invalid character found: " + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_multiplication_and_division(
    tokens: list[Token], index: int
) -> None:
    num1: float = float(tokens[index - 1]["number"])
    num2: float = float(tokens[index + 1]["number"])
    if tokens[index]["type"] == "TIMES":
        evaluated_num: float = num1 * num2
    else:
        evaluate_num:float = num1 / num2
    #todo
    
    evaluate(tokens)


def evaluate(tokens) -> float:
    answer = 0
    tokens.insert(0, {"type": "PLUS"})  # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "TIMES" or tokens[index]["type"] == "TIMES":
            pass
        else:
            index += 1

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


def test(line: str) -> None:
    tokens: list[Token] = tokenize(line)
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
    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line: str = input()
    tokens: list[Token] = tokenize(line)
    answer: float = evaluate(tokens)
    print("answer = %f\n" % answer)
