import pytest

import support_func

list_to_test = [([], [[]]),
                ([[], [], []], [[]]),
                ([[]], [[]]),
                ([[1]], [[1]]),
                ([[1], [1], [1]], [[1, 1, 1]]),
                ([[1, 2], [3, 4]], [[1, 3], [1, 4], [2, 3], [2, 4]]),
                ([[1, 2], []], [[1], [2]]),
                ([[1, 2], [3, 4, 5]], [[1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]])]


@pytest.fixture(params=list_to_test)
def param_list(request):
    return request.param


def test_combinations(param_list):
    data, expected = param_list
    actual = [i for i in support_func.combinations(data)]
    j = 0
    for i in support_func.combinations(data):
        assert i == expected[j]
        j += 1


