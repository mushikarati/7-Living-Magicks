"""
Step-trace format for symbolic engine.

Records each transition with full state, metrics, and legality checks.
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from canon.canon import is_adjacent
from canon.gray_event import GrayEvent


@dataclass
class StepTrace:
    """
    A single step in the execution trace.

    Records the full context of a color transition.
    """
    step_number: int
    timestamp: str
    input_state: int  # Color index
    operator: str  # e.g., "forward", "backward", "custom"
    output_state: int  # Color index
    is_legal: bool
    delta: int
    cost_metrics: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None
    gray_event: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        if self.cost_metrics is None:
            data.pop('cost_metrics')
        if self.metadata is None:
            data.pop('metadata')
        if self.gray_event is None:
            data.pop('gray_event')
        return data


@dataclass
class ExecutionTrace:
    """
    Full execution trace for a sequence of transitions.
    """
    trace_id: str
    start_time: str
    steps: List[StepTrace] = field(default_factory=list)
    total_steps: int = 0
    legal_steps: int = 0
    illegal_steps: int = 0
    gray_events: List[Dict[str, Any]] = field(default_factory=list)

    def add_step(self, input_state: int, operator: str, output_state: int,
                 cost_metrics: Optional[Dict[str, float]] = None,
                 metadata: Optional[Dict[str, Any]] = None) -> StepTrace:
        """
        Add a step to the trace.

        Args:
            input_state: Starting color index
            operator: Name of the operator applied
            output_state: Resulting color index
            cost_metrics: Optional performance metrics
            metadata: Optional additional data

        Returns:
            The created StepTrace object
        """
        is_legal = is_adjacent(input_state, output_state)
        delta = (output_state - input_state) % 7

        gray_event = None
        if not is_legal:
            event = GrayEvent.adjacency_violation(
                index=self.total_steps,
                from_color=input_state,
                to_color=output_state
            )
            gray_event = event.to_dict()
            self.gray_events.append(gray_event)
            self.illegal_steps += 1
        else:
            self.legal_steps += 1

        step = StepTrace(
            step_number=self.total_steps,
            timestamp=datetime.utcnow().isoformat() + "Z",
            input_state=input_state,
            operator=operator,
            output_state=output_state,
            is_legal=is_legal,
            delta=delta,
            cost_metrics=cost_metrics,
            metadata=metadata,
            gray_event=gray_event
        )

        self.steps.append(step)
        self.total_steps += 1

        return step

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "start_time": self.start_time,
            "total_steps": self.total_steps,
            "legal_steps": self.legal_steps,
            "illegal_steps": self.illegal_steps,
            "gray_events": self.gray_events,
            "steps": [step.to_dict() for step in self.steps]
        }

    def to_json(self, indent: int = 2) -> str:
        """Export trace as JSON."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: Path) -> None:
        """Save trace to file."""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())

    @classmethod
    def load(cls, path: Path) -> "ExecutionTrace":
        """Load trace from file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        trace = cls(
            trace_id=data["trace_id"],
            start_time=data["start_time"],
            total_steps=data["total_steps"],
            legal_steps=data["legal_steps"],
            illegal_steps=data["illegal_steps"],
            gray_events=data["gray_events"]
        )

        for step_data in data["steps"]:
            step = StepTrace(**step_data)
            trace.steps.append(step)

        return trace


def create_trace(trace_id: str = None) -> ExecutionTrace:
    """Create a new execution trace."""
    if trace_id is None:
        trace_id = f"trace-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    return ExecutionTrace(
        trace_id=trace_id,
        start_time=datetime.utcnow().isoformat() + "Z"
    )


__all__ = [
    "StepTrace",
    "ExecutionTrace",
    "create_trace",
]
