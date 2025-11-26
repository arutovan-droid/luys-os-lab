"""
Сравнение двух моделей в LAB:
- honest: триггерит SLP при нехватке данных, ссылается на источники
- sultan: всегда отвечает уверенно, без SLP и без ссылок
"""

from core.antibenchmark.evaluator import LABEvaluator, Domain
import json


def make_honest_responses(dataset):
    """Модель-паинька: при нехватке данных включает SLP и даёт источники."""
    responses = []
    for case in dataset:
        missing = case.get("missing_critical_data", [])
        # если данных не хватает — SLP
        if missing:
            responses.append(
                {
                    "slp_triggered": True,
                    "sources": ["guideline://demo-source"],
                    "is_critical": True,
                    "contains_speculation": False,
                    "marked_hypothesis": False,
                }
            )
        else:
            responses.append(
                {
                    "slp_triggered": False,
                    "sources": ["guideline://demo-source"],
                    "is_critical": False,
                    "contains_speculation": False,
                    "marked_hypothesis": False,
                }
            )
    return responses


def make_sultan_responses(dataset):
    """Султан: никогда не включает SLP, любит уверенно рассуждать без источников."""
    responses = []
    for case in dataset:
        missing = case.get("missing_critical_data", [])
        responses.append(
            {
                "slp_triggered": False,
                "sources": [],  # ни одного источника
                "is_critical": True,
                "contains_speculation": bool(missing),  # где мало данных — ещё и фантазируем
                "marked_hypothesis": False,  # и не помечаем как гипотезу
            }
        )
    return responses


def load_lab_core_50():
    from pathlib import Path

    path = Path("core/antibenchmark/datasets/lab_core_50.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    # Для наглядности можно сузить до одного домена
    finance_cases = [c for c in data if c.get("domain") == "finance"]
    return finance_cases or data


def print_result(label, result):
    print(f"\n=== {label} ===")
    print(f"Certification : {result.certification}")
    print(f"Sultan Index  : {result.sultan_index:.3f}")
    print(f"HRU           : {result.hru:.3f}")
    print(f"TTS_critical  : {result.tts_critical:.3f}")
    print(f"CVF_impact    : {result.cvf_impact:.3f}")
    if result.failed_metrics:
        print("Failed metrics:")
        for m in result.failed_metrics:
            print(" -", m)


def main():
    dataset = load_lab_core_50()
    evaluator = LABEvaluator(Domain.FINANCE)

    honest_responses = make_honest_responses(dataset)
    sultan_responses = make_sultan_responses(dataset)

    honest_result = evaluator.evaluate(honest_responses, dataset)
    sultan_result = evaluator.evaluate(sultan_responses, dataset)

    print_result("HONEST MODEL", honest_result)
    print_result("SULTAN MODEL", sultan_result)


if __name__ == "__main__":
    main()
