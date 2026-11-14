import json
import time

EPSILON = 1e-9


def normalize_label(label):
    """
    라벨을 표준 형태로 바꾸는 함수
    예:
    '+' -> 'Cross'
    'cross' -> 'Cross'
    'X' -> 'X'
    'x' -> 'X'
    """
    if not isinstance(label, str):
        return None

    value = label.strip().lower()

    if value == "+" or value == "cross":
        return "Cross"
    if value == "x":
        return "X"

    return None


def extract_size_from_key(key):
    """
    문자열 key에서 크기 숫자를 추출하는 함수

    예:
    'size_5' -> 5
    'size_13_2' -> 13
    """
    if not isinstance(key, str):
        return None

    parts = key.split("_")

    if len(parts) < 2:
        return None

    if parts[0] != "size":
        return None

    try:
        return int(parts[1])
    except ValueError:
        return None


def is_number(value):
    """
    숫자(int, float)인지 확인
    """
    return isinstance(value, (int, float))


def is_square_matrix(matrix, n):
    """
    n x n 형태의 숫자 행렬인지 검사하는 함수

    예:
    [[1,2],[3,4]] 와 n=2 이면 True
    """
    if not isinstance(matrix, list):
        return False

    if len(matrix) != n:
        return False

    for row in matrix:
        if not isinstance(row, list):
            return False

        if len(row) != n:
            return False

        for item in row:
            if not is_number(item):
                return False

    return True


def main():
    print("=== Mini NPU Simulator ===")
    print("기본 설정 완료")
    print("EPSILON =", EPSILON)

    # 간단한 테스트
    print("\n[테스트]")
    print("normalize_label('+') ->", normalize_label("+"))
    print("normalize_label('x') ->", normalize_label("x"))
    print("extract_size_from_key('size_13_2') ->", extract_size_from_key("size_13_2"))
    print("is_square_matrix([[1, 0], [0, 1]], 2) ->", is_square_matrix([[1, 0], [0, 1]], 2))


if __name__ == "__main__":
    main()