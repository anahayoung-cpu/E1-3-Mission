
import time
import statistics


# 2차원 배열 MAC 연산
def mac_2d(matrix_a, matrix_b):
    total = 0

    n = len(matrix_a)

    for i in range(n):
        for j in range(n):
            total += matrix_a[i][j] * matrix_b[i][j]

    return total


# 1차원 배열 MAC 연산
def mac_1d(matrix_a, matrix_b):
    total = 0

    for i in range(len(matrix_a)):
        total += matrix_a[i] * matrix_b[i]

    return total


# 두 연산 함수의 평균 실행 시간 측정
def measure_time(func, a, b, repeat=30):
    times = []

    # 초기 실행 비용을 측정에서 제외
    for _ in range(5):
        func(a, b)

    for _ in range(repeat):
        start = time.perf_counter()

        func(a, b)

        end = time.perf_counter()

        times.append((end - start) * 1000)

    return statistics.mean(times)


def main():
    sizes = [3, 5, 13, 25, 100, 300]

    print("=== CPU 메모리 접근 방식 비교 ===")
    print("각 함수 30회 반복 측정")
    print()

    print(
        f"{'크기':<10}"
        f"{'2D 평균(ms)':<17}"
        f"{'1D 평균(ms)':<17}"
        f"{'결과 일치'}"
    )

    for n in sizes:
        # 동일한 값으로 테스트 데이터 생성
        matrix_2d = [
            [1 for _ in range(n)]
            for _ in range(n)
        ]

        # 2차원 배열을 1차원으로 변환
        matrix_1d = [
            value
            for row in matrix_2d
            for value in row
        ]

        # 두 방식의 결과가 같은지 확인
        result_2d = mac_2d(matrix_2d, matrix_2d)
        result_1d = mac_1d(matrix_1d, matrix_1d)

        # 연산 시간 측정
        time_2d = measure_time(
            mac_2d, matrix_2d, matrix_2d
        )

        time_1d = measure_time(
            mac_1d, matrix_1d, matrix_1d
        )

        print(
            f"{str(n) + 'x' + str(n):<10}"
            f"{time_2d:<17.6f}"
            f"{time_1d:<17.6f}"
            f"{result_2d == result_1d}"
        )


if __name__ == "__main__":
    main()
