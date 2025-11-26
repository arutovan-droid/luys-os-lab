from core.antibenchmark import LABEvaluator


class DummyModel:
    """
    Заглушка модели.
    Пока просто демонстрирует интерфейс: как LAB будет с ней общаться.
    """
    def answer(self, case):
        # case — словарь с полями из LAB-датасета
        # Здесь потом можно будет:
        # - звать реальную LLM
        # - возвращать confidence, slp_triggered и т.д.
        return {
            "raw_answer": "I need more data about your risk profile and investment horizon.",
            "confidence": 0.5,
            "slp_triggered": True,
        }


def main():
    evaluator = LABEvaluator(
        domain="finance",
        thresholds_path="core/antibenchmark/thresholds.toml"
    )
    model = DummyModel()

    result = evaluator.evaluate(
        model,
        "core/antibenchmark/datasets/lab_core_50.json"
    )

    print("=== LAB RESULT ===")
    print("Domain:", result["domain"])
    print("Certification:", result["certification"])
    print("Metrics:", result["metrics"])
    print("Compliance:", result["compliance"])


if __name__ == "__main__":
    main()
