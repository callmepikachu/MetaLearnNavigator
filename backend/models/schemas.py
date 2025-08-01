from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class RelationshipType(str, Enum):
    PARENT = "上级"
    CHILD = "下级"
    SIBLING = "并列"
    RELATED = "相关"


class MasteryLevel(str, Enum):
    SEMANTIC_DERIVATION = "语义级别的公式推导"
    INTUITIVE_UNDERSTANDING = "建立表象的直觉理解"


class JOLLevel(str, Enum):
    COMPLETELY_REMEMBER = "完全记得住"
    MOSTLY_REMEMBER = "大部分记得住"
    BARELY_REMEMBER = "记不太住"
    CANNOT_REMEMBER = "完全不记得"


class FOKLevel(str, Enum):
    MASTER_COMPLETELY = "吃透"
    UNDERSTAND_WELL = "能了解"
    UNDERSTAND_LITTLE = "能了解一点点"
    CANNOT_HANDLE = "啃不下来"


class ConfidenceLevel(str, Enum):
    CONFIDENT = "有信心完成任务"
    NO_CONFIDENCE_WITH_MATERIALS = "没信心完成任务，但是有资料"
    NO_CONFIDENCE_NO_MATERIALS = "没信心完成任务，而且没资料"


class TimeAllocation(str, Enum):
    TWENTY_MIN = "20min"
    THIRTY_MIN = "30min"
    ONE_HOUR = "1h"
    LONGER = "更长时间"


# 认知地图节点
class CognitiveNode(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    x: float
    y: float
    created_at: Optional[datetime] = None


class CognitiveNodeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    x: float
    y: float


# 认知地图连线
class CognitiveEdge(BaseModel):
    id: str
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    custom_name: Optional[str] = None  # 仅当relationship_type为RELATED时使用
    created_at: Optional[datetime] = None


class CognitiveEdgeCreate(BaseModel):
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    custom_name: Optional[str] = None


# 认知地图
class CognitiveMap(BaseModel):
    id: str
    session_id: str
    nodes: List[CognitiveNode]
    edges: List[CognitiveEdge]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CognitiveMapCreate(BaseModel):
    session_id: str
    nodes: List[CognitiveNodeCreate]
    edges: List[CognitiveEdgeCreate]


# 子任务
class SubTask(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    order: int
    mastery_expectation: Optional[MasteryLevel] = None


class SubTaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    order: int
    mastery_expectation: Optional[MasteryLevel] = None


# 学习会话
class LearningSession(BaseModel):
    id: str
    problem_statement: str
    current_step: str
    cognitive_map_id: Optional[str] = None
    selected_edge_id: Optional[str] = None
    sub_tasks: List[SubTask] = []
    session_data: Dict[str, Any] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class LearningSessionCreate(BaseModel):
    problem_statement: str


# 知识卡片
class KnowledgeCard(BaseModel):
    id: str
    title: str
    content: str
    keywords: List[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class KnowledgeCardCreate(BaseModel):
    title: str
    content: str
    keywords: List[str]


# API请求和响应模型
class TaskDecompositionRequest(BaseModel):
    problem_statement: str


class TaskDecompositionResponse(BaseModel):
    nodes: List[CognitiveNodeCreate]
    edges: List[CognitiveEdgeCreate]


class ResourceSearchRequest(BaseModel):
    query: str
    task_context: Optional[str] = None


class ResourceSearchResponse(BaseModel):
    resources: List[Dict[str, Any]]


class JOLAssessmentRequest(BaseModel):
    session_id: str
    assessment: JOLLevel


class FOKAssessmentRequest(BaseModel):
    session_id: str
    assessment: FOKLevel


class ConfidenceAssessmentRequest(BaseModel):
    session_id: str
    confidence: ConfidenceLevel


class TimeAllocationRequest(BaseModel):
    session_id: str
    time_allocation: TimeAllocation


# 流程状态更新
class FlowStateUpdate(BaseModel):
    session_id: str
    current_step: str
    step_data: Dict[str, Any] = {}
