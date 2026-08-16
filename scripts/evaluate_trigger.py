#!/usr/bin/env python3
"""Evaluate in-session signals and decide whether to suggest a review."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from storage import add_storage_args, resolve_store


STATUS_CHOICES = ("unknown", "in_progress", "stalled", "blocked", "done")


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def nonnegative(value: int) -> int:
    return max(int(value), 0)


def detect_reasons(args: argparse.Namespace) -> list[dict]:
    status = args.goal_status
    reasons: list[dict] = []
    revisions = max(args.revision_count, args.same_topic_revisions)

    if revisions >= 2:
        reasons.append(
            {
                "code": "repeated_refinement",
                "severity": "medium",
                "message": "同一目标或问题已经被反复改写，说明当前提示词可能没有一次性进入 AI 的决策空间。",
                "suggested_action": "先复盘目标、约束和完成标准，再改写下一条提示词。",
                "evidence": {"revision_count": revisions},
            }
        )

    if args.correction_count >= 3:
        reasons.append(
            {
                "code": "repeated_correction",
                "severity": "medium",
                "message": "本次会话出现多次纠错，可能存在未被明确指出的根本假设。",
                "suggested_action": "暂停继续修补，明确错误假设、保留部分和验证方式。",
                "evidence": {"correction_count": args.correction_count},
            }
        )

    stalled = (
        status in ("stalled", "blocked")
        and (args.last_progress_turns >= 2 or args.goal_miss_count >= 1)
    ) or (
        status != "done"
        and args.user_turns >= 6
        and args.last_progress_turns >= 3
    )
    if stalled:
        reasons.append(
            {
                "code": "multi_round_stall",
                "severity": "high",
                "message": "经过多轮交互仍没有可确认的目标进展。",
                "suggested_action": "先复盘当前目标是否仍然正确，并决定继续、缩小范围还是更换方案。",
                "evidence": {
                    "user_turns": args.user_turns,
                    "last_progress_turns": args.last_progress_turns,
                    "goal_miss_count": args.goal_miss_count,
                    "goal_status": status,
                },
            }
        )

    if status != "done" and args.goal_miss_count >= 2:
        reasons.append(
            {
                "code": "repeated_goal_miss",
                "severity": "high",
                "message": "AI 的结果连续没有达到当前目标。",
                "suggested_action": "不要只继续补充细节；先重新声明目标、验收标准和不可妥协的边界。",
                "evidence": {"goal_miss_count": args.goal_miss_count},
            }
        )

    if args.verification_failures >= 2:
        reasons.append(
            {
                "code": "verification_loop",
                "severity": "medium",
                "message": "验证连续失败，当前问题可能不在最后一个输出，而在方案或验收标准。",
                "suggested_action": "把验证拆成可观察的检查项，并要求 AI 先解释失败原因。",
                "evidence": {"verification_failures": args.verification_failures},
            }
        )

    return reasons


def is_in_cooldown(session_state: dict, args: argparse.Namespace) -> bool:
    if args.turn is not None and session_state.get("last_prompt_turn") is not None:
        return args.turn - int(session_state["last_prompt_turn"]) < args.cooldown_turns

    last_prompt_at = session_state.get("last_prompt_at")
    if not last_prompt_at:
        return False
    try:
        previous = datetime.fromisoformat(last_prompt_at)
    except ValueError:
        return False
    elapsed_seconds = (datetime.now(timezone.utc) - previous).total_seconds()
    return elapsed_seconds < args.cooldown_minutes * 60


def build_prompt(reasons: list[dict]) -> str:
    labels = "、".join(reason["message"].rstrip("。") for reason in reasons[:2])
    return (
        f"我注意到：{labels}。现在先做一次 1 分钟复盘，确认目标、卡点和下一条提示词吗？"
        " 可回复“先复盘”“继续”或“稍后”。"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    add_storage_args(parser)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--turn", type=int, default=None, help="Current user-turn number in the visible session.")
    parser.add_argument("--user-turns", type=int, default=0)
    parser.add_argument("--revision-count", type=int, default=0, help="Material revisions to the same goal or prompt.")
    parser.add_argument("--same-topic-revisions", type=int, default=0)
    parser.add_argument("--correction-count", type=int, default=0)
    parser.add_argument("--goal-miss-count", type=int, default=0, help="Outputs that visibly failed the current goal.")
    parser.add_argument("--last-progress-turns", type=int, default=0, help="User turns since the last accepted or verified progress.")
    parser.add_argument("--verification-failures", type=int, default=0)
    parser.add_argument("--goal-status", choices=STATUS_CHOICES, default="unknown")
    parser.add_argument("--cooldown-turns", type=int, default=4)
    parser.add_argument("--cooldown-minutes", type=int, default=20)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for name in (
        "user_turns",
        "revision_count",
        "same_topic_revisions",
        "correction_count",
        "goal_miss_count",
        "last_progress_turns",
        "verification_failures",
        "cooldown_turns",
        "cooldown_minutes",
    ):
        setattr(args, name, nonnegative(getattr(args, name)))
    if args.turn is not None:
        args.turn = nonnegative(args.turn)

    storage = resolve_store(args)
    state_path = storage.path / "data" / "trigger-state.json"
    state = read_json(state_path, {"sessions": {}})
    if not isinstance(state, dict):
        state = {"sessions": {}}
    if not isinstance(state.get("sessions"), dict):
        state["sessions"] = {}
    session_state = state.setdefault("sessions", {}).setdefault(args.session_id, {})
    if not isinstance(session_state, dict):
        session_state = {}
        state["sessions"][args.session_id] = session_state
    reasons = detect_reasons(args)
    prompted_codes = set(session_state.get("prompted_codes", []))
    new_reasons = [reason for reason in reasons if reason["code"] not in prompted_codes]
    cooldown = bool(new_reasons) and is_in_cooldown(session_state, args)
    due = bool(new_reasons) and not cooldown

    if due and not args.dry_run:
        now = datetime.now(timezone.utc).isoformat()
        session_state["last_prompt_at"] = now
        if args.turn is not None:
            session_state["last_prompt_turn"] = args.turn
        session_state["prompted_codes"] = sorted(prompted_codes | {reason["code"] for reason in new_reasons})
        session_state["trigger_count"] = int(session_state.get("trigger_count", 0)) + 1
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = {
        **storage.as_dict(),
        "session_id": args.session_id,
        "review_due": due,
        "review_mode": "pause_now" if due else "none",
        "reasons": new_reasons if new_reasons else reasons,
        "suppressed_by_cooldown": cooldown,
        "prompt": build_prompt(new_reasons) if due else "",
        "dry_run": args.dry_run,
        "state_path": str(state_path),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
