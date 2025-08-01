from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import List, Optional

from database.database import get_async_db
from database.models import KnowledgeCardDB
from models.schemas import KnowledgeCard, KnowledgeCardCreate

router = APIRouter()


@router.post("/", response_model=KnowledgeCard)
async def create_knowledge_card(
    card_data: KnowledgeCardCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """创建知识卡片"""
    db_card = KnowledgeCardDB(
        title=card_data.title,
        content=card_data.content,
        keywords=card_data.keywords
    )
    db.add(db_card)
    await db.commit()
    await db.refresh(db_card)
    
    return KnowledgeCard(
        id=db_card.id,
        title=db_card.title,
        content=db_card.content,
        keywords=db_card.keywords,
        created_at=db_card.created_at,
        updated_at=db_card.updated_at
    )


@router.get("/", response_model=List[KnowledgeCard])
async def get_knowledge_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db)
):
    """获取知识卡片列表"""
    result = await db.execute(
        select(KnowledgeCardDB)
        .order_by(KnowledgeCardDB.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    cards = result.scalars().all()
    
    return [
        KnowledgeCard(
            id=card.id,
            title=card.title,
            content=card.content,
            keywords=card.keywords,
            created_at=card.created_at,
            updated_at=card.updated_at
        ) for card in cards
    ]


@router.get("/{card_id}", response_model=KnowledgeCard)
async def get_knowledge_card(
    card_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """获取单个知识卡片"""
    result = await db.execute(
        select(KnowledgeCardDB).where(KnowledgeCardDB.id == card_id)
    )
    card = result.scalar_one_or_none()
    
    if not card:
        raise HTTPException(status_code=404, detail="Knowledge card not found")
    
    return KnowledgeCard(
        id=card.id,
        title=card.title,
        content=card.content,
        keywords=card.keywords,
        created_at=card.created_at,
        updated_at=card.updated_at
    )


@router.put("/{card_id}", response_model=KnowledgeCard)
async def update_knowledge_card(
    card_id: str,
    card_data: KnowledgeCardCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """更新知识卡片"""
    result = await db.execute(
        select(KnowledgeCardDB).where(KnowledgeCardDB.id == card_id)
    )
    card = result.scalar_one_or_none()
    
    if not card:
        raise HTTPException(status_code=404, detail="Knowledge card not found")
    
    card.title = card_data.title
    card.content = card_data.content
    card.keywords = card_data.keywords
    
    await db.commit()
    await db.refresh(card)
    
    return KnowledgeCard(
        id=card.id,
        title=card.title,
        content=card.content,
        keywords=card.keywords,
        created_at=card.created_at,
        updated_at=card.updated_at
    )


@router.delete("/{card_id}")
async def delete_knowledge_card(
    card_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """删除知识卡片"""
    result = await db.execute(
        select(KnowledgeCardDB).where(KnowledgeCardDB.id == card_id)
    )
    card = result.scalar_one_or_none()
    
    if not card:
        raise HTTPException(status_code=404, detail="Knowledge card not found")
    
    await db.delete(card)
    await db.commit()
    
    return {"message": "Knowledge card deleted successfully"}


@router.get("/search/", response_model=List[KnowledgeCard])
async def search_knowledge_cards(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_async_db)
):
    """搜索知识卡片"""
    # 构建搜索条件
    search_conditions = []
    
    # 在标题中搜索
    search_conditions.append(
        KnowledgeCardDB.title.ilike(f"%{query}%")
    )
    
    # 在内容中搜索
    search_conditions.append(
        KnowledgeCardDB.content.ilike(f"%{query}%")
    )
    
    # 在关键词中搜索（JSON字段搜索）
    # 注意：这里的实现可能需要根据具体的数据库类型调整
    search_conditions.append(
        func.json_extract(KnowledgeCardDB.keywords, '$').ilike(f"%{query}%")
    )
    
    # 执行搜索
    result = await db.execute(
        select(KnowledgeCardDB)
        .where(or_(*search_conditions))
        .order_by(KnowledgeCardDB.updated_at.desc())
        .limit(limit)
    )
    cards = result.scalars().all()
    
    return [
        KnowledgeCard(
            id=card.id,
            title=card.title,
            content=card.content,
            keywords=card.keywords,
            created_at=card.created_at,
            updated_at=card.updated_at
        ) for card in cards
    ]


@router.post("/search/by-keywords", response_model=List[KnowledgeCard])
async def search_by_keywords(
    keywords: List[str],
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_async_db)
):
    """根据关键词搜索知识卡片"""
    if not keywords:
        return []
    
    # 构建关键词搜索条件
    search_conditions = []
    
    for keyword in keywords:
        # 在标题、内容和关键词中搜索每个关键词
        keyword_conditions = [
            KnowledgeCardDB.title.ilike(f"%{keyword}%"),
            KnowledgeCardDB.content.ilike(f"%{keyword}%"),
            func.json_extract(KnowledgeCardDB.keywords, '$').ilike(f"%{keyword}%")
        ]
        search_conditions.append(or_(*keyword_conditions))
    
    # 执行搜索（任意关键词匹配）
    result = await db.execute(
        select(KnowledgeCardDB)
        .where(or_(*search_conditions))
        .order_by(KnowledgeCardDB.updated_at.desc())
        .limit(limit)
    )
    cards = result.scalars().all()
    
    return [
        KnowledgeCard(
            id=card.id,
            title=card.title,
            content=card.content,
            keywords=card.keywords,
            created_at=card.created_at,
            updated_at=card.updated_at
        ) for card in cards
    ]
