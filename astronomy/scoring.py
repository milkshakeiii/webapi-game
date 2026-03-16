"""Uplink scoring for science reports and hunting reports."""

import math
from .physics import SIGMA_PLAYER_POS_AU, CHARGING_WINDOW_FACTOR, RECALIBRATION_WINDOW_FACTOR


# ---------------------------------------------------------------------------
# Science report scoring (Appendix A)
# ---------------------------------------------------------------------------

def science_accuracy_score(estimate, truth, scale, question_type="scalar") -> float:
    """Compute accuracy score for a science report.

    question_type: "scalar", "vector", or "enum"
    """
    if question_type == "enum":
        return 1.0 if estimate == truth else 0.0

    if question_type == "vector":
        if isinstance(estimate, dict) and isinstance(truth, dict):
            dx = estimate.get("x", 0) - truth.get("x", 0)
            dy = estimate.get("y", 0) - truth.get("y", 0)
            dz = estimate.get("z", 0) - truth.get("z", 0)
            normalized_error = math.sqrt(dx*dx + dy*dy + dz*dz) / max(scale, 1e-15)
        else:
            normalized_error = abs(float(estimate) - float(truth)) / max(scale, 1e-15)
    else:
        normalized_error = abs(float(estimate) - float(truth)) / max(scale, 1e-15)

    return math.exp(-(normalized_error ** 2))


def freshness_factor(staleness_sec: float, halflife_sec: float) -> float:
    """How fresh the data is. Decays with half-life."""
    if halflife_sec <= 0:
        return 1.0
    return math.exp(-math.log(2) * staleness_sec / halflife_sec)


def novelty_factor(prior_reports: int) -> float:
    """Diminishing returns for repeat reports."""
    return 1.0 / (1.0 + prior_reports)


def science_reward(accuracy: float, freshness: float, novelty: float,
                   base_data: int, base_intel: int) -> tuple[int, int]:
    """Compute data and intel rewards for a science report."""
    factor = accuracy * freshness * novelty
    return round(base_data * factor), round(base_intel * factor)


# ---------------------------------------------------------------------------
# Hunting report scoring (Appendix A)
# ---------------------------------------------------------------------------

def hunting_position_score(predicted_pos: dict, true_pos: dict) -> float:
    """Score a predicted position against the truth.

    Uses Gaussian falloff with SIGMA_PLAYER_POS_AU.
    """
    dx = predicted_pos.get("x", 0) - true_pos.get("x", 0)
    dy = predicted_pos.get("y", 0) - true_pos.get("y", 0)
    dz = predicted_pos.get("z", 0) - true_pos.get("z", 0)
    d_pos = math.sqrt(dx*dx + dy*dy + dz*dz)
    return math.exp(-((d_pos / SIGMA_PLAYER_POS_AU) ** 2))


def hunting_hit_score(position_score: float, classification_correct: bool,
                      target_state: str) -> float:
    """Compute effective hit score for a hunting report."""
    class_factor = 1.0 if classification_correct else 0.0

    if target_state == "jump_charging":
        window_factor = CHARGING_WINDOW_FACTOR
    elif target_state == "recalibrating":
        window_factor = RECALIBRATION_WINDOW_FACTOR
    else:
        window_factor = 1.0

    hit = class_factor * position_score
    return min(1.0, hit * window_factor)


def hunting_rewards(effective_hit_score: float) -> dict:
    """Compute intel reward and target consequences."""
    intel = round(100 * effective_hit_score)

    data_loss_fraction = 0.5 * (effective_hit_score ** 1.5)

    if effective_hit_score < 0.25:
        relay_scrutiny_sec = 0
    else:
        relay_scrutiny_sec = round(180 * (effective_hit_score ** 2))

    uplink_disrupted = effective_hit_score >= 0.60
    uplink_delayed = 0.30 <= effective_hit_score < 0.60

    return {
        "intel_reward": intel,
        "data_loss_fraction": round(data_loss_fraction, 4),
        "relay_scrutiny_sec": relay_scrutiny_sec,
        "uplink_disrupted": uplink_disrupted,
        "uplink_delayed": uplink_delayed,
    }


def position_error_au(predicted: dict, truth: dict) -> float:
    """Euclidean distance between predicted and true position."""
    dx = predicted.get("x", 0) - truth.get("x", 0)
    dy = predicted.get("y", 0) - truth.get("y", 0)
    dz = predicted.get("z", 0) - truth.get("z", 0)
    return math.sqrt(dx*dx + dy*dy + dz*dz)
