from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path

from ai.prototype.openai_preflight import main, run_preflight


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION_SHEET = (
    ROOT / "ai" / "eval" / "paid_smoke_authorization.experimental.v0.1.json"
)


def test_zero_call_preflight_passes_without_credentials(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = run_preflight()

    assert result["preflight_passed"] is True
    assert result["openai_sdk_version"] == "3.6.0"
    assert result["model"] == "gpt-5.6-terra"
    assert result["reasoning_effort"] == "low"
    assert result["credentials_status"] == "API_CREDENTIALS_NOT_CONFIGURED"
    assert result["api_requests_executed"] == 0
    assert all(result["checks"].values())


def test_preflight_reports_key_presence_without_logging_or_persisting_value(
    monkeypatch, capsys
) -> None:
    secret = "test-only-secret-" + "that-must-not-appear"
    monkeypatch.setenv("OPENAI_API_KEY", secret)

    assert main() == 0
    output = capsys.readouterr().out

    assert "API_CREDENTIALS_CONFIGURED" in output
    assert secret not in output
    for directory in (ROOT / "ai", ROOT / "tests"):
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix not in {".pyc"}:
                assert secret not in path.read_text(encoding="utf-8", errors="ignore")


def test_preflight_resolves_exact_four_existing_smoke_cases() -> None:
    result = run_preflight()

    assert result["smoke_case_ids"] == [
        "dialogue-d18-valid",
        "headline-t01-four-claims",
        "headline-t02-zero-claims",
        "npc-n01-valid-answer",
    ]


def test_paid_smoke_authorization_budget_and_governance_are_explicit() -> None:
    sheet = json.loads(AUTHORIZATION_SHEET.read_text(encoding="utf-8"))
    pricing = sheet["pricing_snapshot_usd_per_1m_tokens"]
    calculated = (
        Decimal(sheet["aggregate_planned_model_generation_input_ceiling"])
        * Decimal(str(pricing["input"]))
        + Decimal(sheet["aggregate_planned_model_generation_output_ceiling"])
        * Decimal(str(pricing["output"]))
    ) / Decimal(1_000_000)

    assert sheet["authorization_status"] == "PROPOSED_NOT_AUTHORIZED"
    assert sheet["execution_authorized"] is False
    assert sheet["model"] == "gpt-5.6-terra"
    assert sheet["reasoning_effort"] == "low"
    assert sheet["sdk_internal_retries"] == 0
    assert sheet["max_logical_cases"] == 4
    assert sheet["max_model_generation_calls"] == 8
    assert sheet["max_pre_send_input_token_count_requests"] == 8
    assert sheet["input_token_ceiling_per_model_generation_call"] == 8192
    assert sheet["aggregate_planned_model_generation_input_ceiling"] == 65536
    assert sheet["max_output_tokens_per_model_generation_call"] == 1024
    assert sheet["aggregate_planned_model_generation_output_ceiling"] == 8192
    assert pricing == {"input": 2.0, "output": 12.0}
    assert calculated == Decimal("0.229376")
    assert (
        Decimal(str(sheet["calculated_model_generation_worst_case_usd"]))
        == calculated
    )
    assert Decimal(
        str(sheet["model_generation_absolute_planning_ceiling_usd"])
    ) == Decimal("0.25")
    assert sheet["cost_ceiling_methodology"]["scope"] == "MODEL_GENERATION_ONLY"
    assert sheet["input_token_count_endpoint_billing_status"] == (
        "UNKNOWN_NOT_ESTABLISHED_BY_REVIEWED_PROVIDER_SOURCE"
    )
    assert all(
        case["max_output_tokens_per_model_generation_attempt"] == 1024
        for case in sheet["cases"]
    )

    governance = sheet["governance"]
    assert governance["recognised_execution_authorization_status"] == (
        "AUTHORIZED_FOR_PAID_SMOKE"
    )
    assert governance["authorization_failure_reason"] == (
        "PAID_SMOKE_NOT_AUTHORIZED"
    )
    assert governance["prepared_request_input_token_check_required"] is True
    assert governance["input_token_count_method"] == (
        "client.responses.input_tokens.count"
    )
    assert governance["stop_condition"] == "EXPECTED_INPUT_TOKENS_EXCEED_8192"
    assert governance["required_action"] == "STOP_BEFORE_REQUEST_SEND"
    assert governance["automatic_ceiling_increase_allowed"] is False
    assert governance["model_generation_call_limit_reason"] == (
        "MODEL_GENERATION_CALL_LIMIT_EXCEEDED"
    )
    assert governance["input_token_count_request_limit_reason"] == (
        "INPUT_TOKEN_COUNT_REQUEST_LIMIT_EXCEEDED"
    )
