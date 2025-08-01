from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.database import get_async_db
from database.models import LearningSessionDB, SubTaskDB
from models.schemas import (
    LearningSession, LearningSessionCreate, FlowStateUpdate,
    JOLAssessmentRequest, FOKAssessmentRequest, ConfidenceAssessmentRequest,
    TimeAllocationRequest, SubTask, SubTaskCreate
)
from services.flow_engine import FlowEngine

router = APIRouter()


@router.post("/sessions", response_model=LearningSession)
async def create_learning_session(
    session_data: LearningSessionCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """创建新的学习会话"""
    db_session = LearningSessionDB(
        problem_statement=session_data.problem_statement,
        current_step="problem_input"
    )
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)
    
    return LearningSession(
        id=db_session.id,
        problem_statement=db_session.problem_statement,
        current_step=db_session.current_step,
        cognitive_map_id=db_session.cognitive_map_id,
        selected_edge_id=db_session.selected_edge_id,
        sub_tasks=[],
        session_data=db_session.session_data,
        created_at=db_session.created_at,
        updated_at=db_session.updated_at
    )


@router.get("/sessions/{session_id}", response_model=LearningSession)
async def get_learning_session(
    session_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """获取学习会话详情"""
    result = await db.execute(
        select(LearningSessionDB).where(LearningSessionDB.id == session_id)
    )
    db_session = result.scalar_one_or_none()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    
    # 获取子任务
    sub_tasks_result = await db.execute(
        select(SubTaskDB).where(SubTaskDB.session_id == session_id).order_by(SubTaskDB.order)
    )
    sub_tasks = sub_tasks_result.scalars().all()
    
    return LearningSession(
        id=db_session.id,
        problem_statement=db_session.problem_statement,
        current_step=db_session.current_step,
        cognitive_map_id=db_session.cognitive_map_id,
        selected_edge_id=db_session.selected_edge_id,
        sub_tasks=[
            SubTask(
                id=task.id,
                name=task.name,
                description=task.description,
                order=task.order,
                mastery_expectation=task.mastery_expectation
            ) for task in sub_tasks
        ],
        session_data=db_session.session_data,
        created_at=db_session.created_at,
        updated_at=db_session.updated_at
    )


@router.put("/sessions/{session_id}/flow-state")
async def update_flow_state(
    session_id: str,
    flow_update: FlowStateUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """更新学习流程状态"""
    result = await db.execute(
        select(LearningSessionDB).where(LearningSessionDB.id == session_id)
    )
    db_session = result.scalar_one_or_none()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    
    db_session.current_step = flow_update.current_step
    
    # 合并步骤数据到会话数据中
    if flow_update.step_data:
        if db_session.session_data is None:
            db_session.session_data = {}
        db_session.session_data.update(flow_update.step_data)
    
    await db.commit()
    await db.refresh(db_session)
    
    return {"message": "Flow state updated successfully"}


@router.post("/sessions/{session_id}/jol-assessment")
async def submit_jol_assessment(
    session_id: str,
    assessment: JOLAssessmentRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """提交JOL（学习判断）评估"""
    flow_engine = FlowEngine()
    next_step = await flow_engine.process_jol_assessment(session_id, assessment.assessment, db)
    
    return {"message": "JOL assessment submitted", "next_step": next_step}


@router.post("/sessions/{session_id}/fok-assessment")
async def submit_fok_assessment(
    session_id: str,
    assessment: FOKAssessmentRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """提交FOK（知晓感判断）评估"""
    flow_engine = FlowEngine()
    next_step = await flow_engine.process_fok_assessment(session_id, assessment.assessment, db)
    
    return {"message": "FOK assessment submitted", "next_step": next_step}


@router.post("/sessions/{session_id}/confidence-assessment")
async def submit_confidence_assessment(
    session_id: str,
    assessment: ConfidenceAssessmentRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """提交信心评估"""
    flow_engine = FlowEngine()
    next_step = await flow_engine.process_confidence_assessment(session_id, assessment.confidence, db)
    
    return {"message": "Confidence assessment submitted", "next_step": next_step}


@router.post("/sessions/{session_id}/time-allocation")
async def submit_time_allocation(
    session_id: str,
    time_request: TimeAllocationRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """提交学习时间分配"""
    flow_engine = FlowEngine()
    next_step = await flow_engine.process_time_allocation(session_id, time_request.time_allocation, db)
    
    return {"message": "Time allocation submitted", "next_step": next_step}


@router.post("/sessions/{session_id}/sub-tasks", response_model=List[SubTask])
async def create_sub_tasks(
    session_id: str,
    sub_tasks: List[SubTaskCreate],
    db: AsyncSession = Depends(get_async_db)
):
    """为会话创建子任务"""
    # 验证会话存在
    result = await db.execute(
        select(LearningSessionDB).where(LearningSessionDB.id == session_id)
    )
    db_session = result.scalar_one_or_none()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    
    # 删除现有子任务
    from sqlalchemy import delete
    await db.execute(
        delete(SubTaskDB).where(SubTaskDB.session_id == session_id)
    )
    
    # 创建新子任务
    created_tasks = []
    for task_data in sub_tasks:
        db_task = SubTaskDB(
            session_id=session_id,
            name=task_data.name,
            description=task_data.description,
            order=task_data.order,
            mastery_expectation=task_data.mastery_expectation
        )
        db.add(db_task)
        created_tasks.append(db_task)
    
    await db.commit()
    
    # 刷新并返回创建的任务
    for task in created_tasks:
        await db.refresh(task)
    
    return [
        SubTask(
            id=task.id,
            name=task.name,
            description=task.description,
            order=task.order,
            mastery_expectation=task.mastery_expectation
        ) for task in created_tasks
    ]
