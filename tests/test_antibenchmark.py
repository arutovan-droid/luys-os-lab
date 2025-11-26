from core.antibenchmark import LABEvaluator


def test_lab_evaluator_thresholds_load():
    evaluator = LABEvaluator(domain="medicine", thresholds_path="core/antibenchmark/thresholds.toml")
    t = evaluator.thresholds
    assert t.si_weighted_max > 0
    assert t.jsr_min > 0
