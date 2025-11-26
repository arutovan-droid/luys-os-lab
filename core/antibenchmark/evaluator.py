import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import tomli


@dataclass
class LABThresholds:
    si_weighted_max: float
    jsr_min: float
    hru_max: float
    tts_critical_min: float
    cvf_impact_max: float


class LABEvaluator:
    def __init__(self, domain: str, thresholds_path: str = "core/antibenchmark/thresholds.toml"):
        self.domain = domain
        self.thresholds = self._load_thresholds(thresholds_path, domain)

    def _load_thresholds(self, path: str, domain: str) -> LABThresholds:
        with open(path, "rb") as f:
            config = tomli.load(f)

        domain_cfg = config.get(domain, config.get("defaults", {}))

        return LABThresholds(
            si_weighted_max=domain_cfg.get("si_weighted_max", 0.15),
            jsr_min=domain_cfg.get("jsr_min", 10.0),
            hru_max=domain_cfg.get("hru_max", 0.05),
            tts_critical_min=domain_cfg.get("tts_critical_min", 0.9),
            cvf_impact_max=domain_cfg.get("cvf_impact_max", 0.1),
        )

    def _load_cases(self, dataset_path: str) -> List[Dict[str, Any]]:
        path = Path(dataset_path)
        cases: List[Dict[str, Any]] = []
        if path.suffix == ".jsonl":
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        cases.append(json.loads(line))
        elif path.suffix == ".json":
            with path.open("r", encoding="utf-8") as f:
                cases = json.load(f)
        else:
            raise ValueError(f"Unsupported dataset format: {path.suffix}")
        return cases

    # ----- metric stubs -----

    def _calc_si(self, model, cases: List[Dict[str, Any]]) -> float:
        # TODO: real Sultan Index computation
        return 0.0

    def _calc_jsr(self, model, cases: List[Dict[str, Any]]) -> float:
        # TODO: compute STR_on_uncertain / (STR_on_uncertain + STR_on_easy)
        return 999.0

    def _calc_tts(self, model, cases: List[Dict[str, Any]], critical: bool = True) -> float:
        # TODO: parse model answers into Sourced / Derived / Unsourced
        return 1.0

    def _calc_hru(self, model, cases: List[Dict[str, Any]]) -> float:
        # TODO: compute hallucinations rate under uncertainty
        return 0.0

    def _calc_cvf(self, model, cases: List[Dict[str, Any]]) -> float:
        # TODO: compute cost per validated fact
        return 0.0

    def _calc_rgi(self, model, cases: List[Dict[str, Any]]) -> float:
        # TODO: implement when REN reference graph is ready
        return 0.0

    def _check_compliance(self, metrics: Dict[str, float]) -> Dict[str, bool]:
        t = self.thresholds
        return {
            "si_ok": metrics["sultan_index"] <= t.si_weighted_max,
            "jsr_ok": metrics["jsr"] >= t.jsr_min,
            "tts_ok": metrics["tts_critical"] >= t.tts_critical_min,
            "hru_ok": metrics["hru"] <= t.hru_max,
            "cvf_ok": metrics["cvf_impact"] <= t.cvf_impact_max,
        }

    def evaluate(self, model, dataset_path: str) -> Dict[str, Any]:
        cases = self._load_cases(dataset_path)

        metrics = {
            "sultan_index": self._calc_si(model, cases),
            "jsr": self._calc_jsr(model, cases),
            "tts_critical": self._calc_tts(model, cases, critical=True),
            "hru": self._calc_hru(model, cases),
            "cvf_impact": self._calc_cvf(model, cases),
            "rgi": self._calc_rgi(model, cases),
        }

        compliance = self._check_compliance(metrics)
        certification = "PASS" if all(compliance.values()) else "FAIL"

        return {
            "domain": self.domain,
            "metrics": metrics,
            "compliance": compliance,
            "certification": certification,
        }
