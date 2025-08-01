from sqlalchemy import Column, String, Text, DateTime, Float, Integer, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class LearningSessionDB(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    problem_statement = Column(Text, nullable=False)
    current_step = Column(String, default="problem_input")
    cognitive_map_id = Column(String, ForeignKey("cognitive_maps.id"), nullable=True)
    selected_edge_id = Column(String, nullable=True)
    session_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    cognitive_map = relationship("CognitiveMapDB", back_populates="session")
    sub_tasks = relationship("SubTaskDB", back_populates="session")


class CognitiveMapDB(Base):
    __tablename__ = "cognitive_maps"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey("learning_sessions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    session = relationship("LearningSessionDB", back_populates="cognitive_map")
    nodes = relationship("CognitiveNodeDB", back_populates="cognitive_map")
    edges = relationship("CognitiveEdgeDB", back_populates="cognitive_map")


class CognitiveNodeDB(Base):
    __tablename__ = "cognitive_nodes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    cognitive_map_id = Column(String, ForeignKey("cognitive_maps.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    cognitive_map = relationship("CognitiveMapDB", back_populates="nodes")


class CognitiveEdgeDB(Base):
    __tablename__ = "cognitive_edges"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    cognitive_map_id = Column(String, ForeignKey("cognitive_maps.id"), nullable=False)
    source_id = Column(String, ForeignKey("cognitive_nodes.id"), nullable=False)
    target_id = Column(String, ForeignKey("cognitive_nodes.id"), nullable=False)
    relationship_type = Column(String, nullable=False)  # 上级、下级、并列、相关
    custom_name = Column(String, nullable=True)  # 仅当relationship_type为"相关"时使用
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    cognitive_map = relationship("CognitiveMapDB", back_populates="edges")


class SubTaskDB(Base):
    __tablename__ = "sub_tasks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey("learning_sessions.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    mastery_expectation = Column(String, nullable=True)  # 语义级别的公式推导 or 建立表象的直觉理解
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    session = relationship("LearningSessionDB", back_populates="sub_tasks")


class KnowledgeCardDB(Base):
    __tablename__ = "knowledge_cards"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    keywords = Column(JSON, default=list)  # 存储关键词列表
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LearningResourceDB(Base):
    __tablename__ = "learning_resources"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    url = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    resource_type = Column(String, nullable=False)  # article, video, book, etc.
    keywords = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
