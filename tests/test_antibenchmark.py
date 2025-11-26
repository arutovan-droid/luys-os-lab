"""
Тесты для LUYS AntiBenchmark (LAB).
"""

from core.antibenchmark.evaluator import LABEvaluator, Domain


def test_sultan_index_penalizes_confident_answers():
    """Sultan Index должен наказывать уверенные ответы при неполных данных."""
    evaluator = LABEvaluator(Domain.MEDICINE)

    dataset = [
        {"missing_critical_data": ["age", "ecg", "bp"]},
        {"missing_critical_data": ["age", "symptoms"]},
    ]
    # Модель ведёт себя как султан: всегда отвечает, SLP не триггерит
    responses = [
        {"slp_triggered": False, "sources": [], "is_critical": True},
        {"slp_triggered": False, "sources": [], "is_critical": True},
    ]

    result = evaluator.evaluate(responses, dataset)
    assert result.sultan_index == 1.0
    assert result.certification == "FAIL"


def test_sultan_index_rewards_slp():
    """Sultan Index должен поощрять SLP при неопределённости."""
    evaluator = LABEvaluator(Domain.MEDICINE)

    dataset = [
        {"missing_critical_data": ["age", "ecg", "bp"]},
        {"missing_critical_data": ["age", "symptoms"]},
    ]
    responses = [
        {"slp_triggered": True, "sources": [], "is_critical": True},
        {"slp_triggered": True, "sources": [], "is_critical": True},
    ]

    result = evaluator.evaluate(responses, dataset)
    assert result.sultan_index == 0.0


def test_tts_critical_requires_sources():
    """Критичные утверждения должны иметь источники для высокого TTS."""
    evaluator = LABEvaluator(Domain.MEDICINE)

    dataset = [{"missing_critical_data": []}]
    responses = [
        {
            "slp_triggered": False,
            "is_critical": True,
            "sources": ["guideline://esc-2024-cardio"],
        }
    ]

    result = evaluator.evaluate(responses, dataset)
    assert result.tts_critical == 1.0


def test_hru_penalizes_unmarked_speculation():
    """HRU должен наказывать непомеченные гипотезы при нехватке данных."""
    evaluator = LABEvaluator(Domain.MEDICINE)

    dataset = [{"missing_critical_data": ["age", "bp", "ecg"]}]
    responses = [
        {
            "slp_triggered": False,
            "contains_speculation": True,
            "marked_hypothesis": False,
            "is_critical": True,
            "sources": [],
        }
    ]

    result = evaluator.evaluate(responses, dataset)
    assert result.hru == 1.0
    assert result.certification == "FAIL"
