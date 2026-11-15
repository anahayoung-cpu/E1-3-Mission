# E1-3-Mission
AI가 계산하는 방식을 흉내 내는 작은 계산기 만들기


*1단계 뼈대 검증(기본 함수들 정상 검증)
'''text
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
'''

*1단계 python main.py 실행 결과
'''text
PS C:\Users\ana23773640\Desktop\E1-3-Mission> python main.py
=== Mini NPU Simulator ===
기본 설정 완료
EPSILON = 1e-09

[테스트]
normalize_label('+') -> Cross
normalize_label('x') -> X
extract_size_from_key('size_13_2') -> 13
is_square_matrix([[1, 0], [0, 1]], 2) -> True
'''
<img width="679" height="260" alt="image" src="https://github.com/user-attachments/assets/f35a0d1f-829b-4c31-9caf-fc214d85a465" />

*2단계 연산 핵심 검증(MAC 계산 정상 확인)
1. 새로 추가된 함수 3개 (기능 찾아 넣기-추 수정)
'''text
def mac(matrix_a, matrix_b):
    """
    MAC 연산:
    같은 위치의 값끼리 곱한 뒤 모두 더한다.
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
'''
2. main()에서 2단계에 추가된 테스트
'''text
    # 테스트용 필터
    cross_filter = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]

    x_filter = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]

    # 테스트용 입력 패턴 1: Cross 느낌
    input_cross_like = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    # 테스트용 입력 패턴 2: X 느낌
    input_x_like = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]

    print("\n[MAC 테스트 1: Cross 느낌 입력]")
    cross_score_1 = mac(input_cross_like, cross_filter)
    x_score_1 = mac(input_cross_like, x_filter)
    print("Cross score =", cross_score_1)
    print("X score =", x_score_1)
    print("판정 =", decide_label(cross_score_1, x_score_1))

    print("\n[MAC 테스트 2: X 느낌 입력]")
    cross_score_2 = mac(input_x_like, cross_filter)
    x_score_2 = mac(input_x_like, x_filter)
    print("Cross score =", cross_score_2)
    print("X score =", x_score_2)
    print("판정 =", decide_label(cross_score_2, x_score_2))
'''
*2단계 python main.py 실행 결과
'''text
PS C:\Users\ana23773640\Desktop\E1-3-Mission> python main.py
=== Mini NPU Simulator ===
2단계: MAC + 판정 함수 테스트
EPSILON = 1e-09

[기본 함수 테스트]
normalize_label('+') -> Cross
normalize_label('x') -> X
extract_size_from_key('size_13_2') -> 13
is_square_matrix([[1, 0], [0, 1]], 2) -> True

[MAC 테스트 1: Cross 느낌 입력]
Cross score = 1
X score = 1
판정 = 판정 불가

[MAC 테스트 2: X 느낌 입력]
Cross score = 5
X score = 5
판정 = 판정 불가
'''
<img width="670" height="523" alt="image" src="https://github.com/user-attachments/assets/5b704f2f-0cb1-4b7d-a697-d23cb2bd69c9" />

3. cross_filter와 x_filter 수정
'''text
cross_filter = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]
'''
4. filter 수정 결과
'''text
PS C:\Users\ana23773640\Desktop\E1-3-Mission> python main.py
=== Mini NPU Simulator ===
2단계: MAC + 판정 함수 테스트
EPSILON = 1e-09

[기본 함수 테스트]
normalize_label('+') -> Cross
normalize_label('x') -> X
extract_size_from_key('size_13_2') -> 13
is_square_matrix([[1, 0], [0, 1]], 2) -> True

[MAC 테스트 1: Cross 느낌 입력]
Cross score = 5
X score = 1
판정 = Cross

[MAC 테스트 2: X 느낌 입력]
Cross score = 1
X score = 5
판정 = X
'''

<img width="669" height="518" alt="image" src="https://github.com/user-attachments/assets/d818935d-8816-4e1f-8d2a-e89144b6cd24" />

*3단계 data.json의 patterns를 전부 읽어서 자동 판정
1. 새로 추가된 함수
  가. JSON 읽기
'''text
def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
'''

  나. 전체 패턴 자동 처리
'''text
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

'''
  다. 3단계 검증용 main()으로 수정 
'''text
def main():
    print("=== Mini NPU Simulator : 3단계 ===")

    data = load_json_file("data.json")
    process_all_patterns(data)


if __name__ == "__main__":
    main()

'''

2. 2단계 python main.py 실행 결과
'''text
PS C:\Users\ana23773640\Desktop\E1-3-Mission> python main.py
=== Mini NPU Simulator : 3단계 ===

=== size_5_1 ===
크기 = 5
정답 = X
예측 = 판정 불가
Cross score = 0.9
X score = 0.8999999999999999
결과 = 오답

=== size_5_2 ===
크기 = 5
정답 = Cross
예측 = Cross
Cross score = 8.9
X score = 0.1
결과 = 정답

=== size_13_1 ===
크기 = 13
정답 = X
예측 = X
Cross score = 0.3
X score = 14.700000000000008
결과 = 정답

=== size_13_2 ===
크기 = 13
정답 = Cross
예측 = 판정 불가
Cross score = 7.499999999999997
X score = 7.5
결과 = 오답

=== size_25_1 ===
크기 = 25
정답 = X
예측 = 판정 불가
Cross score = 4.9
X score = 4.899999999999999
결과 = 오답

=== size_25_2 ===
크기 = 25
정답 = Cross
예측 = Cross
Cross score = 52.9
X score = 0.1
결과 = 정답

=== 전체 결과 ===
총 패턴 수 = 6
정답 수 = 3
동점 수 = 3
정확도 = 0.5
'''

<img width="674" height="1455" alt="image" src="https://github.com/user-attachments/assets/b533cd8d-68ee-40de-97eb-25b11bc49195" />




