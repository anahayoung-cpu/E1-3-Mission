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


def mac(matrix_a, matrix_b):
    """
    MAC 연산:
    같은 위치의 값끼리 곱한 뒤 모두 더한다.

    예:
    A = [[1, 2],
         [3, 4]]

    B = [[5, 6],
         [7, 8]]

    결과 = 1*5 + 2*6 + 3*7 + 4*8
    """
    if not isinstance(matrix_a, list) or not isinstance(matrix_b, list):
        return None

    if len(matrix_a) == 0 or len(matrix_b) == 0:
        return None

    if len(matrix_a) != len(matrix_b):
        return None

    n = len(matrix_a)

    if not is_square_matrix(matrix_a, n):
        return None

    if not is_square_matrix(matrix_b, n):
        return None

    total = 0

    for i in range(n):
        for j in range(n):
            total += matrix_a[i][j] * matrix_b[i][j]

    return total


def compare_scores(cross_score, x_score):
    """
    점수 비교 함수

    반환값:
    1  -> Cross 점수가 더 큼
    -1 -> X 점수가 더 큼
    0  -> 거의 같음
    None -> 잘못된 입력
    """
    if not is_number(cross_score) or not is_number(x_score):
        return None

    diff = cross_score - x_score

    if abs(diff) < EPSILON:
        return 0
    elif diff > 0:
        return 1
    else:
        return -1


def decide_label(cross_score, x_score):
    """
    최종 판정 함수

    반환값:
    'Cross'
    'X'
    '판정 불가'
    """
    result = compare_scores(cross_score, x_score)

    if result == 1:
        return "Cross"
    elif result == -1:
        return "X"
    elif result == 0:
        return "판정 불가"
    else:
        return None

def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def predict_label(input_matrix, cross_filter, x_filter):
    cross_score = mac(input_matrix, cross_filter)
    x_score = mac(input_matrix, x_filter)
    predicted = decide_label(cross_score, x_score)
    return predicted, cross_score, x_score


def process_all_patterns(data):
    total_count = 0
    correct_count = 0
    tie_count = 0

    patterns = data.get("patterns", {})
    filters = data.get("filters", {})

    for pattern_key, pattern_info in patterns.items():
        size = extract_size_from_key(pattern_key)
        filter_key = f"size_{size}"

        print(f"\n=== {pattern_key} ===")

        if filter_key not in filters:
            print(f"필터 없음: {filter_key}")
            continue

        input_matrix = pattern_info["input"]
        expected = normalize_label(pattern_info["expected"])

        cross_filter = filters[filter_key]["cross"]
        x_filter = filters[filter_key]["x"]

        if not is_square_matrix(input_matrix, size):
            print("입력 행렬 크기 오류")
            continue

        if not is_square_matrix(cross_filter, size):
            print("cross 필터 크기 오류")
            continue

        if not is_square_matrix(x_filter, size):
            print("x 필터 크기 오류")
            continue

        predicted, cross_score, x_score = predict_label(input_matrix, cross_filter, x_filter)

        total_count += 1

        if predicted == "판정 불가":
            tie_count += 1

        is_correct = (predicted == expected)
        if is_correct:
            correct_count += 1

        print("크기 =", size)
        print("정답 =", expected)
        print("예측 =", predicted)
        print("Cross score =", cross_score)
        print("X score =", x_score)
        print("결과 =", "정답" if is_correct else "오답")

    print("\n=== 전체 결과 ===")
    print("총 패턴 수 =", total_count)
    print("정답 수 =", correct_count)
    print("동점 수 =", tie_count)

    if total_count > 0:
        accuracy = correct_count / total_count
        print("정확도 =", accuracy)
    else:
        print("처리된 패턴이 없습니다.")


def main():
    print("=== Mini NPU Simulator : 3단계 ===")

    data = load_json_file("data.json")
    process_all_patterns(data)


if __name__ == "__main__":
    main()