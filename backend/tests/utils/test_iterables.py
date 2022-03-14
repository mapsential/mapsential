from backend.utils.iterables import chunk_iter


def test_chunk_iter():
    assert [
        [i for i in range(0, 10)],
        [i for i in range(10, 20)],
        [i for i in range(20, 30)],
        [i for i in range(30, 40)],
        [i for i in range(40, 42)],
    ] == [chunk for chunk in chunk_iter(range(42), 10)]
