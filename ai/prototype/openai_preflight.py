"""Zero-request verification for the proposed Batch 2B paid smoke."""

from __future__ import annotations

from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import openai

from .openai_responses_adapter import ROOT, load_authorization_sheet


MANIFEST_PATH = ROOT / "ai" / "eval" / "p0_baseline_manifest.v0.1.1.json"
EXPECTED_SDK_VERSION = "3.6.0"


def _normalized_lf_sha256(path: Path) -> str:
    normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _prompt_version(path: Path) -> str:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    prefix = "PROMPT_VERSION: "
    if not first_line.startswith(prefix):
        raise ValueError(f"prompt version header missing: {path.name}")
    return first_line.removeprefix(prefix)


def run_preflight() -> dict[str, Any]:
    """Verify all local preconditions without constructing a provider client."""

    sheet = load_authorization_sheet()
    pricing = sheet["pricing_snapshot_usd_per_1m_tokens"]
    calculated_worst_case = (
        Decimal(sheet["aggregate_planned_model_generation_input_ceiling"])
        * Decimal(str(pricing["input"]))
        + Decimal(sheet["aggregate_planned_model_generation_output_ceiling"])
        * Decimal(str(pricing["output"]))
    ) / Decimal(1_000_000)
    checks: dict[str, bool] = {}
    checks["sdk_import_and_version"] = openai.__version__ == EXPECTED_SDK_VERSION
    checks["model_configuration"] = sheet["model"] == "gpt-5.6-terra"
    checks["reasoning_configuration"] = sheet["reasoning_effort"] == "low"
    checks["official_api_base_url"] = sheet["base_url"] == "https://api.openai.com/v1"
    checks["execution_not_authorized"] = sheet["execution_authorized"] is False
    checks["tools_disabled"] = sheet["tools_enabled"] is False
    checks["call_ceiling"] = (
        sheet["max_logical_cases"] == 4
        and sheet["max_model_generation_calls"] == 8
        and sheet["max_pre_send_input_token_count_requests"] == 8
    )
    checks["paid_smoke_budget"] = (
        sheet["authorization_status"] == "PROPOSED_NOT_AUTHORIZED"
        and sheet["input_token_ceiling_per_model_generation_call"] == 8192
        and sheet["aggregate_planned_model_generation_input_ceiling"] == 65536
        and sheet["max_output_tokens_per_model_generation_call"] == 1024
        and sheet["aggregate_planned_model_generation_output_ceiling"] == 8192
        and calculated_worst_case == Decimal("0.229376")
        and Decimal(str(sheet["calculated_model_generation_worst_case_usd"]))
        == calculated_worst_case
        and Decimal(
            str(sheet["model_generation_absolute_planning_ceiling_usd"])
        )
        == Decimal("0.25")
        and sheet["input_token_count_endpoint_billing_status"]
        == "UNKNOWN_NOT_ESTABLISHED_BY_REVIEWED_PROVIDER_SOURCE"
        and sheet["cost_ceiling_methodology"]["scope"]
        == "MODEL_GENERATION_ONLY"
        and all(
            case["max_output_tokens_per_model_generation_attempt"]
            == sheet["max_output_tokens_per_model_generation_call"]
            for case in sheet["cases"]
        )
    )
    governance = sheet["governance"]
    checks["pre_send_input_ceiling_governance"] = (
        governance["recognised_execution_authorization_status"]
        == "AUTHORIZED_FOR_PAID_SMOKE"
        and governance["authorization_failure_reason"]
        == "PAID_SMOKE_NOT_AUTHORIZED"
        and governance["prepared_request_input_token_check_required"] is True
        and governance["input_token_count_method"]
        == "client.responses.input_tokens.count"
        and governance["stop_condition"] == "EXPECTED_INPUT_TOKENS_EXCEED_8192"
        and governance["required_action"] == "STOP_BEFORE_REQUEST_SEND"
        and governance["automatic_ceiling_increase_allowed"] is False
        and governance["model_generation_call_limit_reason"]
        == "MODEL_GENERATION_CALL_LIMIT_EXCEEDED"
        and governance["input_token_count_request_limit_reason"]
        == "INPUT_TOKEN_COUNT_REQUEST_LIMIT_EXCEEDED"
    )

    for component, schema_info in sheet["transport_schemas"].items():
        schema = json.loads((ROOT / schema_info["path"]).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        checks[f"{component}_transport_schema_loads"] = True

    checks["frozen_schemas_unchanged"] = all(
        _normalized_lf_sha256(ROOT / relative_path) == expected_hash
        for relative_path, expected_hash in sheet[
            "frozen_schema_sha256_normalized_lf"
        ].items()
    )

    loaded_prompt_versions: dict[str, str] = {}
    for component, prompt_info in sheet["prompts"].items():
        version = _prompt_version(ROOT / prompt_info["path"])
        loaded_prompt_versions[component] = version
        checks[f"{component}_prompt_version_loads"] = version == prompt_info["version"]

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_cases = {case["case_id"]: case for case in manifest["cases"]}
    selected_case_ids = [case["case_id"] for case in sheet["cases"]]
    checks["four_smoke_case_ids_resolve"] = (
        len(selected_case_ids) == 4
        and len(set(selected_case_ids)) == 4
        and all(case_id in manifest_cases for case_id in selected_case_ids)
    )

    measurement_directory = ROOT / sheet["measurement_output_directory"]
    directory_already_existed = measurement_directory.exists()
    measurement_directory.mkdir(parents=True, exist_ok=True)
    measurement_probe = measurement_directory / ".preflight-write-probe"
    measurement_probe.write_text("", encoding="utf-8")
    checks["measurement_location_writable"] = measurement_probe.is_file()
    measurement_probe.unlink()
    if not directory_already_existed:
        measurement_directory.rmdir()

    credentials_status = (
        "API_CREDENTIALS_CONFIGURED"
        if bool(os.environ.get("OPENAI_API_KEY"))
        else "API_CREDENTIALS_NOT_CONFIGURED"
    )
    result = {
        "preflight_passed": all(checks.values()),
        "checks": checks,
        "openai_sdk_version": openai.__version__,
        "provider": sheet["provider"],
        "api": sheet["api"],
        "model": sheet["model"],
        "reasoning_effort": sheet["reasoning_effort"],
        "prompt_versions": loaded_prompt_versions,
        "smoke_case_ids": selected_case_ids,
        "credentials_status": credentials_status,
        "api_requests_executed": 0,
    }
    return result


def main() -> int:
    print(json.dumps(run_preflight(), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
