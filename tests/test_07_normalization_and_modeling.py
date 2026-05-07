from conftest import load_ko_module


def test_3nf_decomposition_preserves_dependencies():
    m = load_ko_module("07-normalization-and-modeling.py")
    R = frozenset({"order_id", "user_id", "user_email", "product_id", "product_name"})
    F = [
        (frozenset({"order_id"}), frozenset({"user_id"})),
        (frozenset({"user_id"}), frozenset({"user_email"})),
        (frozenset({"product_id"}), frozenset({"product_name"})),
    ]
    decomp = m.synthesize_3nf(R, F)
    assert m.is_dependency_preserved(decomp, F)
