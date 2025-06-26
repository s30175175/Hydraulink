from press.utils.shortener import create_slug


def test_create_slug_length():
    assert len(create_slug(length=8)) == 8


def test_create_slug_unique():
    slugs = [create_slug() for _ in range(100)]
    assert len(set(slugs)) == 100
