from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import LearningSessionDB, SubTaskDB
from models.schemas import JOLLevel, FOKLevel, ConfidenceLevel, TimeAllocation, MasteryLevel, SubTaskCreate
from services.subtask_generator import SubTaskGenerator
from typing import Dict, Any, List


class FlowEngine:
    """学习流程引擎，负责处理流程状态转换和逻辑判断"""
    
    # 评估分数映射
    JOL_SCORES = {
        JOLLevel.COMPLETELY_REMEMBER: 4,
        JOLLevel.MOSTLY_REMEMBER: 3,
        JOLLevel.BARELY_REMEMBER: 2,
        JOLLevel.CANNOT_REMEMBER: 1
    }
    
    FOK_SCORES = {
        FOKLevel.MASTER_COMPLETELY: 4,
        FOKLevel.UNDERSTAND_WELL: 3,
        FOKLevel.UNDERSTAND_LITTLE: 2,
        FOKLevel.CANNOT_HANDLE: 1
    }
    
    MASTERY_SCORES = {
        MasteryLevel.SEMANTIC_DERIVATION: 4,
        MasteryLevel.INTUITIVE_UNDERSTANDING: 2
    }
    
    async def process_jol_assessment(
        self, 
        session_id: str, 
        jol_level: JOLLevel, 
        db: AsyncSession
    ) -> str:
        """处理JOL评估，返回下一步"""
        # 获取会话
        result = await db.execute(
            select(LearningSessionDB).where(LearningSessionDB.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise ValueError("Session not found")
        
        # 计算JOL分数
        jol_score = self.JOL_SCORES[jol_level]
        
        # 更新会话数据
        session_data = session.session_data or {}
        session_data['jol_assessment'] = jol_level.value
        session_data['jol_score'] = jol_score
        
        # 进行预期对比
        next_step = await self._compare_with_expectation(session, jol_score, db)
        
        # 更新会话
        await db.execute(
            update(LearningSessionDB)
            .where(LearningSessionDB.id == session_id)
            .values(
                current_step=next_step,
                session_data=session_data
            )
        )
        await db.commit()
        
        return next_step
    
    async def process_fok_assessment(
        self, 
        session_id: str, 
        fok_level: FOKLevel, 
        db: AsyncSession
    ) -> str:
        """处理FOK评估，返回下一步"""
        # 获取会话
        result = await db.execute(
            select(LearningSessionDB).where(LearningSessionDB.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise ValueError("Session not found")
        
        # 计算FOK分数
        fok_score = self.FOK_SCORES[fok_level]
        
        # 更新会话数据
        session_data = session.session_data or {}
        session_data['fok_assessment'] = fok_level.value
        session_data['fok_score'] = fok_score
        
        # 进行预期对比
        next_step = await self._compare_with_expectation(session, fok_score, db)
        
        # 更新会话
        await db.execute(
            update(LearningSessionDB)
            .where(LearningSessionDB.id == session_id)
            .values(
                current_step=next_step,
                session_data=session_data
            )
        )
        await db.commit()
        
        return next_step
    
    async def _compare_with_expectation(
        self, 
        session: LearningSessionDB, 
        actual_score: int, 
        db: AsyncSession
    ) -> str:
        """比较实际分数与预期分数，决定下一步"""
        session_data = session.session_data or {}
        
        # 获取预期掌握程度分数
        expected_mastery = session_data.get('expected_mastery_level')
        if expected_mastery:
            expected_score = self.MASTERY_SCORES.get(MasteryLevel(expected_mastery), 2)
        else:
            expected_score = 2  # 默认预期分数
        
        # 比较分数
        if actual_score >= expected_score:
            # 实际高于预期，学习目标达成
            session_data['comparison_result'] = 'above_expectation'
            return "learning_completed"
        else:
            # 实际低于预期，进入EOL判断
            session_data['comparison_result'] = 'below_expectation'
            return "eol_difficulty_assessment"
    
    async def process_confidence_assessment(
        self, 
        session_id: str, 
        confidence: ConfidenceLevel, 
        db: AsyncSession
    ) -> str:
        """处理信心评估，返回下一步"""
        # 获取会话
        result = await db.execute(
            select(LearningSessionDB).where(LearningSessionDB.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise ValueError("Session not found")
        
        # 更新会话数据
        session_data = session.session_data or {}
        session_data['confidence_assessment'] = confidence.value
        
        # 根据信心评估决定下一步
        if confidence == ConfidenceLevel.CONFIDENT:
            next_step = "time_allocation"
        elif confidence == ConfidenceLevel.NO_CONFIDENCE_WITH_MATERIALS:
            next_step = "external_guidance"
        else:  # NO_CONFIDENCE_NO_MATERIALS
            next_step = "task_switching"
        
        # 更新会话
        await db.execute(
            update(LearningSessionDB)
            .where(LearningSessionDB.id == session_id)
            .values(
                current_step=next_step,
                session_data=session_data
            )
        )
        await db.commit()
        
        return next_step
    
    async def process_time_allocation(
        self, 
        session_id: str, 
        time_allocation: TimeAllocation, 
        db: AsyncSession
    ) -> str:
        """处理时间分配，返回下一步"""
        # 获取会话
        result = await db.execute(
            select(LearningSessionDB).where(LearningSessionDB.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise ValueError("Session not found")
        
        # 更新会话数据
        session_data = session.session_data or {}
        session_data['time_allocation'] = time_allocation.value
        
        # 计算倒计时时间（分钟）
        time_minutes = {
            TimeAllocation.TWENTY_MIN: 20,
            TimeAllocation.THIRTY_MIN: 30,
            TimeAllocation.ONE_HOUR: 60,
            TimeAllocation.LONGER: 120  # 默认2小时
        }
        
        session_data['allocated_minutes'] = time_minutes[time_allocation]
        next_step = "learning_in_progress"
        
        # 更新会话
        await db.execute(
            update(LearningSessionDB)
            .where(LearningSessionDB.id == session_id)
            .values(
                current_step=next_step,
                session_data=session_data
            )
        )
        await db.commit()
        
        return next_step
    
    async def process_obstacle_assessment(
        self, 
        session_id: str, 
        has_obstacle: bool, 
        db: AsyncSession
    ) -> str:
        """处理学习阻碍评估"""
        # 获取会话
        result = await db.execute(
            select(LearningSessionDB).where(LearningSessionDB.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise ValueError("Session not found")
        
        # 更新会话数据
        session_data = session.session_data or {}
        session_data['has_obstacle'] = has_obstacle
        
        if has_obstacle:
            next_step = "eol_difficulty_assessment"
        else:
            next_step = "strategy_selection"
        
        # 更新会话
        await db.execute(
            update(LearningSessionDB)
            .where(LearningSessionDB.id == session_id)
            .values(
                current_step=next_step,
                session_data=session_data
            )
        )
        await db.commit()
        
        return next_step

    async def generate_subtasks_from_edge(
        self,
        session_id: str,
        source_node_name: str,
        target_node_name: str,
        relationship_type: str,
        db: AsyncSession
    ) -> List[SubTaskCreate]:
        """根据选择的连线生成子任务"""

        # 获取会话信息
        result = await db.execute(
            select(LearningSessionDB).where(LearningSessionDB.id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            raise ValueError("Session not found")

        # 使用子任务生成器
        generator = SubTaskGenerator()
        subtasks = generator.generate_subtasks(
            source_node_name=source_node_name,
            target_node_name=target_node_name,
            relationship_type=relationship_type,
            problem_context=session.problem_statement
        )

        # 删除现有子任务
        from sqlalchemy import delete
        await db.execute(
            delete(SubTaskDB).where(SubTaskDB.session_id == session_id)
        )

        # 创建新子任务
        created_tasks = []
        for task_data in subtasks:
            db_task = SubTaskDB(
                session_id=session_id,
                name=task_data.name,
                description=task_data.description,
                order=task_data.order,
                mastery_expectation=task_data.mastery_expectation.value if task_data.mastery_expectation else None
            )
            db.add(db_task)
            created_tasks.append(task_data)

        await db.commit()

        # 更新会话状态
        await db.execute(
            update(LearningSessionDB)
            .where(LearningSessionDB.id == session_id)
            .values(current_step="expectation_setting")
        )
        await db.commit()

        return created_tasks
