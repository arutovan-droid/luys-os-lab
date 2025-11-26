"""
Пример: прогон LUYS AntiBenchmark (LAB) на LAB-CORE-50.

Показываем разницу между:
- "HonestModel"  — честно триггерит SLP и ставит источники.
- "SultanModel"  — лезет отвечать без данных, галлюцинирует без маркировки.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from core.antibenchmark.evaluator import LABEvaluator, Domain


DATASET_PATH = (
    Path(__file__).resolve().parents[1]
    / "core"
    / "antibenchmark"
    / "datasets"
    / "lab_core_50.json"
)


def load_dataset(domain: Domain) -> List[Dict[str, Any]]:
    raw = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    return [case for case in raw if case.get("domain") == domain.value]


def build_honest_responses(dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Модель, которая:
    - триггерит SLP, если данных не хватает,
    - не галлюцинирует,
    - для high-risk кейсов указывает источники.
    """
    responses: List[Dict[str, Any]] = []

    for case in dataset:
        missing = case.get("missing_critical_data", [])
        risk = int(case.get("risk_level", 5))
        is_uncertain = len(missing) > 0

        slp_triggered = is_uncertain
        is_critical = risk >= 8

        sources = []
        if is_critical:
            # В реальности тут были бы реальные ссылки (guideline, statute, и т.д.)
            sources = ["guideline://placeholder"]

        responses.append(
            {
                "slp_triggered": slp_triggered,
                "is_critical": is_critical,
                "sources": sources,
                "contains_speculation": False,
                "marked_hypothesis": False,
            }
        )

    return responses


def build_sultan_responses(dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Модель-султан:
    - никогда не триггерит SLP,
    - в условиях неопределённости выдаёт спекуляции без маркировки,
    - не указывает источники.
    """
    responses: List[Dict[str, Any]] = []

    for case in dataset:
        missing = case.get("missing_critical_data", [])
        risk = int(case.get("risk_level", 5))
        is_uncertain = len(missing) > 0

        responses.append(
            {
                "slp_triggered": False,
                "is_critical": risk >= 8,
                "sources": [],
                "contains_speculation": is_uncertain,
                "marked_hypothesis": False,
            }
        )

    return responses


def print_result(domain: Domain, mode: str, result) -> None:
    print("=== LAB RESULT ===")
    print(f"Domain:        {domain.value}")
    print(f"Mode:          {mode}")
    print(f"Certification: {result.certification}")
    print("Metrics:")
    print(f"  Sultan Index        : {result.sultan_index:.3f}")
    print(f"  STR (uncertain)     : {result.str_on_uncertain:.3f}")
    print(f"  STR (easy)          : {result.str_on_easy:.3f}")
    print(f"  JSR                 : {result.jsr:.3f}")
    print(f"  TTS critical        : {result.tts_critical:.3f}")
    print(f"  TTS background      : {result.tts_background:.3f}")
    print(f"  HRU                 : {result.hru:.3f}")
    print(f"  CVF impact          : {result.cvf_impact:.3f}")
    if result.failed_metrics:
        print("Failed metrics:")
        for m in result.failed_metrics:
            print(f"  - {m}")
    else:
        print("All metrics within thresholds (PASS).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LUYS AntiBenchmark demo")
    parser.add_argument(
        "--domain",
        choices=[d.value for d in Domain],
        default="finance",
        help="Domain to evaluate on",
    )
    parser.add_argument(
        "--mode",
        choices=["honest", "sultan"],
        default="honest",
        help="Model behavior to simulate",
    )
    args = parser.parse_args()

    domain = Domain(args.domain)
    dataset = load_dataset(domain)

    if not dataset:
        print(f"No cases found for domain '{domain.value}' in LAB-CORE-50.")
        return

    if args.mode == "honest":
        responses = build_honest_responses(dataset)
    else:
        responses = build_sultan_responses(dataset)

    evaluator = LABEvaluator(domain)
    result = evaluator.evaluate(responses, dataset)
    print_result(domain, args.mode, result)


if __name__ == "__main__":
    main()



