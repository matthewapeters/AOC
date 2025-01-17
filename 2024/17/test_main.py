from main import load_file, Computer
import pytest


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("sample1.txt", ("", {"B": 1})),
        ("sample2.txt", ("0,1,2", {})),
        ("sample3.txt", ("4,2,5,6,7,7,7,7,3,1,0", {"A": 0})),
        ("sample4.txt", ("", {"B": 26})),
        ("sample5.txt", ("", {"B": 44354})),
        ("sample7.txt", ("4,6,3,5,6,3,5,2,1,0", {})),
        ("input2.txt", ("4,6,3,5,6,3,5,2,1,0", {})),
    ],
)
def test_run(file_name, expected):
    """
    test_run
    """
    program, registers = load_file(file_name)
    c = Computer()
    output = c.run(program, registers)
    if expected[0]:
        assert (
            expected[0] == output
        ), f"expected {file_name} to have output {expected[0]}, got '{output}'"
    if len(expected[1]) > 0:
        for k, v in expected[1].items():
            assert (
                c.registers[k] == v
            ), f"expected registry {k} to be {v} but got {c.registers[k]}"
