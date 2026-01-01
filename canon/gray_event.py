"""
Gray Event - Standard representation for canon violations and degeneracy.

This module provides the GrayEvent class for creating and validating Gray events.
All Gray events should use this standard format for consistency across the Codex.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
import json


@dataclass
class EntropyMetrics:
    """Compression/entropy metrics for degeneracy-based Gray events."""
    compression_ratio: Optional[float] = None
    entropy_estimate: Optional[float] = None
    ncd_score: Optional[float] = None
    degeneracy_threshold: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class EventContext:
    """Contextual information for a Gray event."""
    sequence_length: Optional[int] = None
    window: Optional[List[int]] = None
    file: Optional[str] = None
    line: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        if self.sequence_length is not None:
            data["sequence_length"] = self.sequence_length
        if self.window is not None:
            data["window"] = self.window
        if self.file is not None:
            data["file"] = self.file
        if self.line is not None:
            data["line"] = self.line
        return data


@dataclass
class GrayEvent:
    """
    Standard Gray Event representation.

    A Gray event indicates a canon violation, illegal jump, or degeneracy condition.
    """

    type: str  # adjacency_violation, degeneracy_detected, unknown_token, entropy_plateau, mimic_loop
    index: int
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    from_color: Optional[int] = None
    to_color: Optional[int] = None
    delta: Optional[int] = None
    reason: str = ""
    severity: str = "error"  # warning, error, critical
    entropy_metrics: Optional[EntropyMetrics] = None
    context: Optional[EventContext] = None
    metadata: Optional[Dict[str, Any]] = None

    VALID_TYPES = {
        "adjacency_violation",
        "degeneracy_detected",
        "unknown_token",
        "entropy_plateau",
        "mimic_loop"
    }

    VALID_SEVERITIES = {"warning", "error", "critical"}

    def __post_init__(self):
        """Validate Gray event after initialization."""
        if self.type not in self.VALID_TYPES:
            raise ValueError(f"Invalid Gray event type: {self.type}")
        if self.severity not in self.VALID_SEVERITIES:
            raise ValueError(f"Invalid severity: {self.severity}")
        if self.index < 0:
            raise ValueError(f"Index must be non-negative, got {self.index}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary matching the JSON schema."""
        data = {
            "type": self.type,
            "index": self.index,
            "timestamp": self.timestamp,
            "reason": self.reason,
            "severity": self.severity,
        }

        # Add optional fields only if present
        if self.from_color is not None:
            data["from"] = self.from_color
        if self.to_color is not None:
            data["to"] = self.to_color
        if self.delta is not None:
            data["delta"] = self.delta
        if self.entropy_metrics is not None:
            data["entropy_metrics"] = self.entropy_metrics.to_dict()
        if self.context is not None:
            data["context"] = self.context.to_dict()
        if self.metadata is not None:
            data["metadata"] = self.metadata

        return data

    def to_json(self, indent: Optional[int] = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def adjacency_violation(
        cls,
        index: int,
        from_color: int,
        to_color: int,
        modulus: int = 7,
        **kwargs
    ) -> "GrayEvent":
        """Create an adjacency violation Gray event."""
        delta = (to_color - from_color) % modulus
        return cls(
            type="adjacency_violation",
            index=index,
            from_color=from_color,
            to_color=to_color,
            delta=delta,
            reason=f"Illegal jump: delta {delta} not in [1, 6]",
            **kwargs
        )

    @classmethod
    def degeneracy_detected(
        cls,
        index: int,
        entropy_metrics: EntropyMetrics,
        **kwargs
    ) -> "GrayEvent":
        """Create a degeneracy detection Gray event."""
        return cls(
            type="degeneracy_detected",
            index=index,
            entropy_metrics=entropy_metrics,
            reason="Compression/entropy indicates mimic loop or degeneracy",
            severity="warning",
            **kwargs
        )

    @classmethod
    def unknown_token(
        cls,
        index: int,
        token: str,
        **kwargs
    ) -> "GrayEvent":
        """Create an unknown token Gray event."""
        return cls(
            type="unknown_token",
            index=index,
            reason=f"Encountered unknown token '{token}' not in canonical sequence",
            **kwargs
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"GrayEvent({self.type} at index {self.index}: {self.reason})"

    def __repr__(self) -> str:
        return f"GrayEvent(type={self.type!r}, index={self.index}, severity={self.severity!r})"


# Convenience function for creating Gray events from validation results
def create_gray_events_from_violations(violations: List[Dict[str, Any]]) -> List[GrayEvent]:
    """
    Convert violation dicts from validate_sequence() to GrayEvent objects.

    Args:
        violations: List of violation dicts from canon.validate_sequence()

    Returns:
        List of GrayEvent objects
    """
    events = []
    for v in violations:
        event = GrayEvent.adjacency_violation(
            index=v["index"],
            from_color=v["from"],
            to_color=v["to"]
        )
        events.append(event)
    return events


__all__ = [
    "GrayEvent",
    "EntropyMetrics",
    "EventContext",
    "create_gray_events_from_violations",
]
