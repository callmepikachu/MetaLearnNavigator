from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List

from database.database import get_async_db
from database.models import (
    CognitiveMapDB, CognitiveNodeDB, CognitiveEdgeDB, LearningSessionDB
)
from models.schemas import (
    CognitiveMap, CognitiveMapCreate, CognitiveNode, CognitiveNodeCreate,
    CognitiveEdge, CognitiveEdgeCreate, RelationshipType
)

router = APIRouter()


@router.post("/", response_model=CognitiveMap)
async def create_cognitive_map(
    map_data: CognitiveMapCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """创建认知地图"""
    # 验证会话存在
    result = await db.execute(
        select(LearningSessionDB).where(LearningSessionDB.id == map_data.session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")
    
    # 创建认知地图
    db_map = CognitiveMapDB(session_id=map_data.session_id)
    db.add(db_map)
    await db.flush()  # 获取map的ID
    
    # 创建节点
    created_nodes = []
    for node_data in map_data.nodes:
        db_node = CognitiveNodeDB(
            cognitive_map_id=db_map.id,
            name=node_data.name,
            description=node_data.description,
            x=node_data.x,
            y=node_data.y
        )
        db.add(db_node)
        created_nodes.append(db_node)
    
    await db.flush()  # 获取节点ID
    
    # 创建连线
    created_edges = []
    for edge_data in map_data.edges:
        # 验证关系类型约束
        if edge_data.relationship_type == RelationshipType.RELATED and not edge_data.custom_name:
            raise HTTPException(
                status_code=400, 
                detail="Custom name is required for 'related' relationship type"
            )
        
        db_edge = CognitiveEdgeDB(
            cognitive_map_id=db_map.id,
            source_id=edge_data.source_id,
            target_id=edge_data.target_id,
            relationship_type=edge_data.relationship_type.value,
            custom_name=edge_data.custom_name
        )
        db.add(db_edge)
        created_edges.append(db_edge)
    
    await db.commit()
    
    # 刷新所有对象
    await db.refresh(db_map)
    for node in created_nodes:
        await db.refresh(node)
    for edge in created_edges:
        await db.refresh(edge)
    
    # 更新学习会话的认知地图ID
    session.cognitive_map_id = db_map.id
    await db.commit()
    
    return CognitiveMap(
        id=db_map.id,
        session_id=db_map.session_id,
        nodes=[
            CognitiveNode(
                id=node.id,
                name=node.name,
                description=node.description,
                x=node.x,
                y=node.y,
                created_at=node.created_at
            ) for node in created_nodes
        ],
        edges=[
            CognitiveEdge(
                id=edge.id,
                source_id=edge.source_id,
                target_id=edge.target_id,
                relationship_type=RelationshipType(edge.relationship_type),
                custom_name=edge.custom_name,
                created_at=edge.created_at
            ) for edge in created_edges
        ],
        created_at=db_map.created_at,
        updated_at=db_map.updated_at
    )


@router.get("/{map_id}", response_model=CognitiveMap)
async def get_cognitive_map(
    map_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """获取认知地图详情"""
    # 获取地图
    result = await db.execute(
        select(CognitiveMapDB).where(CognitiveMapDB.id == map_id)
    )
    db_map = result.scalar_one_or_none()
    
    if not db_map:
        raise HTTPException(status_code=404, detail="Cognitive map not found")
    
    # 获取节点
    nodes_result = await db.execute(
        select(CognitiveNodeDB).where(CognitiveNodeDB.cognitive_map_id == map_id)
    )
    nodes = nodes_result.scalars().all()
    
    # 获取连线
    edges_result = await db.execute(
        select(CognitiveEdgeDB).where(CognitiveEdgeDB.cognitive_map_id == map_id)
    )
    edges = edges_result.scalars().all()
    
    return CognitiveMap(
        id=db_map.id,
        session_id=db_map.session_id,
        nodes=[
            CognitiveNode(
                id=node.id,
                name=node.name,
                description=node.description,
                x=node.x,
                y=node.y,
                created_at=node.created_at
            ) for node in nodes
        ],
        edges=[
            CognitiveEdge(
                id=edge.id,
                source_id=edge.source_id,
                target_id=edge.target_id,
                relationship_type=RelationshipType(edge.relationship_type),
                custom_name=edge.custom_name,
                created_at=edge.created_at
            ) for edge in edges
        ],
        created_at=db_map.created_at,
        updated_at=db_map.updated_at
    )


@router.put("/{map_id}", response_model=CognitiveMap)
async def update_cognitive_map(
    map_id: str,
    map_data: CognitiveMapCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """更新认知地图"""
    # 验证地图存在
    result = await db.execute(
        select(CognitiveMapDB).where(CognitiveMapDB.id == map_id)
    )
    db_map = result.scalar_one_or_none()
    
    if not db_map:
        raise HTTPException(status_code=404, detail="Cognitive map not found")
    
    # 删除现有节点和连线
    await db.execute(
        delete(CognitiveEdgeDB).where(CognitiveEdgeDB.cognitive_map_id == map_id)
    )
    await db.execute(
        delete(CognitiveNodeDB).where(CognitiveNodeDB.cognitive_map_id == map_id)
    )
    
    # 创建新节点
    created_nodes = []
    for node_data in map_data.nodes:
        db_node = CognitiveNodeDB(
            cognitive_map_id=map_id,
            name=node_data.name,
            description=node_data.description,
            x=node_data.x,
            y=node_data.y
        )
        db.add(db_node)
        created_nodes.append(db_node)
    
    await db.flush()
    
    # 创建新连线
    created_edges = []
    for edge_data in map_data.edges:
        # 验证关系类型约束
        if edge_data.relationship_type == RelationshipType.RELATED and not edge_data.custom_name:
            raise HTTPException(
                status_code=400, 
                detail="Custom name is required for 'related' relationship type"
            )
        
        db_edge = CognitiveEdgeDB(
            cognitive_map_id=map_id,
            source_id=edge_data.source_id,
            target_id=edge_data.target_id,
            relationship_type=edge_data.relationship_type.value,
            custom_name=edge_data.custom_name
        )
        db.add(db_edge)
        created_edges.append(db_edge)
    
    await db.commit()
    
    # 刷新所有对象
    await db.refresh(db_map)
    for node in created_nodes:
        await db.refresh(node)
    for edge in created_edges:
        await db.refresh(edge)
    
    return CognitiveMap(
        id=db_map.id,
        session_id=db_map.session_id,
        nodes=[
            CognitiveNode(
                id=node.id,
                name=node.name,
                description=node.description,
                x=node.x,
                y=node.y,
                created_at=node.created_at
            ) for node in created_nodes
        ],
        edges=[
            CognitiveEdge(
                id=edge.id,
                source_id=edge.source_id,
                target_id=edge.target_id,
                relationship_type=RelationshipType(edge.relationship_type),
                custom_name=edge.custom_name,
                created_at=edge.created_at
            ) for edge in created_edges
        ],
        created_at=db_map.created_at,
        updated_at=db_map.updated_at
    )


@router.post("/{map_id}/select-edge")
async def select_important_edge(
    map_id: str,
    edge_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """选择重要的连线"""
    # 验证连线存在
    result = await db.execute(
        select(CognitiveEdgeDB).where(
            CognitiveEdgeDB.id == edge_id,
            CognitiveEdgeDB.cognitive_map_id == map_id
        )
    )
    edge = result.scalar_one_or_none()
    
    if not edge:
        raise HTTPException(status_code=404, detail="Edge not found")
    
    # 获取认知地图对应的学习会话
    map_result = await db.execute(
        select(CognitiveMapDB).where(CognitiveMapDB.id == map_id)
    )
    cognitive_map = map_result.scalar_one_or_none()
    
    if not cognitive_map:
        raise HTTPException(status_code=404, detail="Cognitive map not found")
    
    # 更新学习会话的选中连线
    session_result = await db.execute(
        select(LearningSessionDB).where(LearningSessionDB.id == cognitive_map.session_id)
    )
    session = session_result.scalar_one_or_none()
    
    if session:
        session.selected_edge_id = edge_id
        session.current_step = "sub_task_generation"
        await db.commit()
    
    return {"message": "Edge selected successfully", "edge_id": edge_id}
