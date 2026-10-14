"""
DX-OS Open-Core: Workflow & Event Bus Orchestration Module (Tầng 1)
Quản lý luồng sự kiện (Event Streaming) và trạng thái quy trình tự động hóa (SOP).
"""

import asyncio
from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkflowEvent:
    event_id: str
    topic: str
    payload: Dict[str, Any]
    timestamp: str

class DXEventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DXEventBus, cls).__new__(cls)
            cls._instance.subscribers: Dict[str, List[Callable]] = {}
            cls._instance.event_history: List[WorkflowEvent] = []
        return cls._instance

    def subscribe(self, topic: str, handler: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    async def publish(self, topic: str, event_id: str, payload: Dict[str, Any]):
        event = WorkflowEvent(
            event_id=event_id,
            topic=topic,
            payload=payload,
            timestamp=datetime.utcnow().isoformat()
        )
        self.event_history.append(event)
        
        # Trigger subscribers
        if topic in self.subscribers:
            for handler in self.subscribers[topic]:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
        return event

# Singleton instance
event_bus = DXEventBus()
