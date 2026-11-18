import json
import time

EPSILON = 1e-9


def normalize_label(label): # 라벨 정규화 (이름 맞추기)
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


def extract_size_from_key(key): # key size 추출
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


def is_number(value): # 숫자 검증
    """
    숫자(int, float)인지 확인
    """
    return isinstance(value, (int, float))


def is_square_matrix(matrix, n): # n x n 확인
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

def input_matrix(name, n=3): # 행렬 입력
    print(f"\n{name} ({n}줄 입력, 공백 구분)")

    matrix = []

    for i in range(n):
        while True:
            user_input = input(f"{i + 1}행: ")

            values = user_input.split()

            if len(values) != n:
                print(f"입력 오류: 숫자 {n}개를 입력하세요.")
                continue

            try:
                row = [float(value) for value in values]

                matrix.append(row)
                break

            except ValueError:
                print("입력 오류: 숫자만 입력하세요.")

    return matrix

def mac(matrix_a, matrix_b): # MAC 연산
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

def measure_mac_time(matrix_a, matrix_b, repeat=10):
    total_time = 0

    for i in range(repeat):
        start = time.perf_counter()

        mac(matrix_a, matrix_b)

        end = time.perf_counter()

        elapsed = end - start
        total_time += elapsed

    average_time = total_time / repeat

    return average_time * 1000


def generate_matrix(n):
    matrix = []

    for i in range(n):
        row = []

        for j in range(n):
            row.append(1)

        matrix.append(row)

    return matrix


def analyze_performance():
    print("\n=== 성능 분석 (평균/10회) ===")

    sizes = [3, 5, 13, 25]

    print(f"{'크기':<12}{'평균 시간(ms)':<20}{'연산 횟수(N²)'}")
    print("-" * 45)

    for n in sizes:
        matrix_a = generate_matrix(n)
        matrix_b = generate_matrix(n)

        average_time = measure_mac_time(
            matrix_a, matrix_b, repeat=10
        )

        operation_count = n * n

        print(
            f"{n}x{n:<9}"
            f"{average_time:<20.6f}"
            f"{operation_count}"
        )


def compare_scores(cross_score, x_score): # +,X 라벨 비교
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
    result = compare_scores(cross_score, x_score)

    if result == 1:
        return "Cross"
    elif result == -1:
        return "X"
    elif result == 0:
        return "UNDECIDED"
    else:
        return None


def load_json_file(filename): # JSON 파일 PYTHON으로 불러옴(딕셔너리 형태)
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def predict_label(input_matrix, cross_filter, x_filter): # 라벨 예측
    cross_score = mac(input_matrix, cross_filter)
    x_score = mac(input_matrix, x_filter)
    predicted = decide_label(cross_score, x_score)
    return predicted, cross_score, x_score


def process_all_patterns(data):
    total_count = 0
    pass_count = 0
    fail_cases = []

    # JSON 최상위 구조 확인
    if not isinstance(data, dict):
        print("JSON 오류: 최상위 데이터가 객체가 아닙니다.")
        return

    patterns = data.get("patterns", {})
    filters = data.get("filters", {})

    if not isinstance(patterns, dict) or not isinstance(filters, dict):
        print("JSON 오류: patterns 또는 filters 형식이 잘못되었습니다.")
        return

    for pattern_key, pattern_info in patterns.items():
        total_count += 1

        print(f"\n=== {pattern_key} ===")

        # 1. 패턴 크기 확인
        size = extract_size_from_key(pattern_key)

        if size not in (5, 13, 25):
            reason = "패턴 키 또는 크기 오류"
            print("FAIL:", reason)
            fail_cases.append((pattern_key, reason))
            continue

        filter_key = f"size_{size}"

        # 2. 필터 존재 여부 확인
        if filter_key not in filters:
            reason = f"필터 없음: {filter_key}"
            print("FAIL:", reason)
            fail_cases.append((pattern_key, reason))
            continue

        # 3. 패턴 및 필터 구조 확인
        filter_info = filters[filter_key]

        if not isinstance(pattern_info, dict):
            reason = "패턴 데이터 형식 오류"
        elif not isinstance(filter_info, dict):
            reason = "필터 데이터 형식 오류"
        else:
            reason = None

        if reason is not None:
            print("FAIL:", reason)
            fail_cases.append((pattern_key, reason))
            continue

        # 4. 데이터 가져오기
        input_matrix = pattern_info.get("input")
        expected = normalize_label(pattern_info.get("expected"))

        # filter 키의 대소문자와 표기 정규화
        normalized_filters = {}

        for key, value in filter_info.items():
            label = normalize_label(key)

            if label is not None:
                normalized_filters[label] = value

        cross_filter = normalized_filters.get("Cross")
        x_filter = normalized_filters.get("X")

        # 5. 라벨 검증
        if expected is None:
            reason = "expected 라벨 오류"
        elif cross_filter is None or x_filter is None:
            reason = "Cross 또는 X 필터 누락"
        elif not is_square_matrix(input_matrix, size):
            reason = "입력 행렬 크기 또는 값 오류"
        elif not is_square_matrix(cross_filter, size):
            reason = "Cross 필터 크기 또는 값 오류"
        elif not is_square_matrix(x_filter, size):
            reason = "X 필터 크기 또는 값 오류"
        else:
            reason = None

        if reason is not None:
            print("FAIL:", reason)
            fail_cases.append((pattern_key, reason))
            continue

        # 6. MAC 연산 및 판정
        predicted, cross_score, x_score = predict_label(
            input_matrix, cross_filter, x_filter
        )

        # 7. PASS / FAIL 비교
        is_pass = (predicted == expected)

        print("크기 =", size)
        print("Cross 점수 =", cross_score)
        print("X 점수 =", x_score)
        print("판정 =", predicted)
        print("expected =", expected)
        print("결과 =", "PASS" if is_pass else "FAIL")

        if is_pass:
            pass_count += 1
        else:
            if predicted == "UNDECIDED":
                reason = "epsilon 기준 동점 처리"
            else:
                reason = "예측 결과와 expected 불일치"

            fail_cases.append((pattern_key, reason))
            print("실패 사유 =", reason)

    return total_count, pass_count, fail_cases


def print_result_summary(total_count, pass_count, fail_cases):
    fail_count = total_count - pass_count

    print("\n=== 전체 결과 요약 ===")
    print("총 테스트:", total_count)
    print("통과:", pass_count)
    print("실패:", fail_count)

    if fail_cases:
        print("\n실패 케이스:")

        for key, reason in fail_cases:
            print(f"- {key}: {reason}")
    else:
        print("모든 테스트가 통과했습니다.")


def run_user_mode():
    print("\n=== 사용자 입력 모드 (3x3) ===")

    # 1. 필터 A와 B 입력
    print("\n[1] 필터 입력")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    # 2. 필터 저장 확인
    print("\n[2] 필터 저장 확인")
    print("필터 A:", filter_a)
    print("필터 B:", filter_b)

    # 3. 패턴 입력
    print("\n[3] 패턴 입력")

    pattern = input_matrix("패턴")

    # 4. MAC 연산
    print("\n[4] MAC 연산")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    print("A 점수:", score_a)
    print("B 점수:", score_b)

    # 5. 점수 비교
    result = compare_scores(score_a, score_b)

    # 6. 최종 판정
    if result == 1:
        print("판정: A")

    elif result == -1:
        print("판정: B")

    elif result == 0:
        print("판정: 판정 불가 (동점)")

    else:
        print("판정 오류: 점수를 비교할 수 없습니다.")

      # 7. MAC 연산 성능 분석
    print("\n[5] 성능 분석")

    average_a = measure_mac_time(pattern, filter_a)
    average_b = measure_mac_time(pattern, filter_b)

    n = len(pattern)
    operation_count = n * n

    print(f"행렬 크기: {n}x{n}")
    print(f"MAC 연산 횟수: {operation_count}")
    print(f"A 평균 연산 시간: {average_a:.6f} ms")
    print(f"B 평균 연산 시간: {average_b:.6f} ms")


def main():
    print("=== Mini NPU Simulator ===")

    while True:
        print("\n[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")

        choice = input("선택: ")

        if choice == "1":
            run_user_mode()
            break

        elif choice == "2":
            data = load_json_file("data.json")

            total_count, pass_count, fail_cases = process_all_patterns(data)

            analyze_performance()

            print_result_summary(total_count, pass_count, fail_cases)

            break

        else:
            print("입력 오류: 1 또는 2를 선택하세요.")


if __name__ == "__main__":
    main()
