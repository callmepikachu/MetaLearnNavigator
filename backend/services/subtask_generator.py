"""
子任务生成服务
根据选择的认知地图连线生成具体的学习子任务
"""

from typing import List, Dict, Any
from models.schemas import SubTaskCreate, MasteryLevel


class SubTaskGenerator:
    """子任务生成器"""
    
    def generate_subtasks(
        self, 
        source_node_name: str, 
        target_node_name: str, 
        relationship_type: str,
        problem_context: str = ""
    ) -> List[SubTaskCreate]:
        """
        根据选择的连线生成子任务
        
        Args:
            source_node_name: 源节点名称
            target_node_name: 目标节点名称  
            relationship_type: 关系类型
            problem_context: 问题上下文
        """
        
        # 根据关系类型生成不同的子任务序列
        if relationship_type == "下级":
            return self._generate_hierarchical_subtasks(source_node_name, target_node_name, problem_context)
        elif relationship_type == "上级":
            return self._generate_bottom_up_subtasks(source_node_name, target_node_name, problem_context)
        elif relationship_type == "并列":
            return self._generate_parallel_subtasks(source_node_name, target_node_name, problem_context)
        else:  # 相关
            return self._generate_related_subtasks(source_node_name, target_node_name, problem_context)
    
    def _generate_hierarchical_subtasks(self, source: str, target: str, context: str) -> List[SubTaskCreate]:
        """生成层次化学习子任务（从上级到下级）"""
        return [
            SubTaskCreate(
                name=f"理解 {target} 的整体框架",
                description=f"建立对 {target} 的宏观认识，了解其在 {source} 中的位置和作用",
                order=1,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            ),
            SubTaskCreate(
                name=f"学习 {target} 的核心概念",
                description=f"深入学习 {target} 的关键概念、定义和基本原理",
                order=2,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name=f"掌握 {target} 的具体应用",
                description=f"通过实例和练习，掌握 {target} 的具体应用方法",
                order=3,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            )
        ]
    
    def _generate_bottom_up_subtasks(self, source: str, target: str, context: str) -> List[SubTaskCreate]:
        """生成自底向上学习子任务（从下级到上级）"""
        return [
            SubTaskCreate(
                name=f"巩固 {source} 的基础知识",
                description=f"确保对 {source} 的基础概念有扎实的理解",
                order=1,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name=f"探索 {source} 与 {target} 的联系",
                description=f"理解 {source} 如何支撑和构成 {target}",
                order=2,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            ),
            SubTaskCreate(
                name=f"整合理解 {target}",
                description=f"基于 {source} 的理解，形成对 {target} 的完整认知",
                order=3,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            )
        ]
    
    def _generate_parallel_subtasks(self, source: str, target: str, context: str) -> List[SubTaskCreate]:
        """生成并列学习子任务（同等重要的概念）"""
        return [
            SubTaskCreate(
                name=f"对比学习 {source} 和 {target}",
                description=f"比较 {source} 和 {target} 的异同点，理解各自特点",
                order=1,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            ),
            SubTaskCreate(
                name=f"分别掌握 {source} 和 {target}",
                description=f"独立深入学习 {source} 和 {target} 的具体内容",
                order=2,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name=f"综合应用 {source} 和 {target}",
                description=f"在实际场景中综合运用 {source} 和 {target}",
                order=3,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            )
        ]
    
    def _generate_related_subtasks(self, source: str, target: str, context: str) -> List[SubTaskCreate]:
        """生成相关概念学习子任务"""
        return [
            SubTaskCreate(
                name=f"理解 {source} 的核心内容",
                description=f"深入理解 {source} 的主要内容和特点",
                order=1,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name=f"探索 {source} 与 {target} 的关联",
                description=f"发现和理解 {source} 与 {target} 之间的相关性",
                order=2,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            ),
            SubTaskCreate(
                name=f"建立知识网络",
                description=f"将 {source} 和 {target} 整合到完整的知识体系中",
                order=3,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            )
        ]
    
    def generate_contextual_subtasks(self, problem_statement: str, selected_path: List[str]) -> List[SubTaskCreate]:
        """
        根据问题上下文和选择路径生成更精准的子任务
        
        Args:
            problem_statement: 原始问题描述
            selected_path: 选择的学习路径节点列表
        """
        
        # 分析问题类型
        problem_type = self._analyze_problem_type(problem_statement)
        
        # 根据问题类型和路径生成子任务
        if problem_type == "programming":
            return self._generate_programming_subtasks(selected_path)
        elif problem_type == "mathematics":
            return self._generate_math_subtasks(selected_path)
        elif problem_type == "language":
            return self._generate_language_subtasks(selected_path)
        else:
            return self._generate_general_subtasks(selected_path)
    
    def _analyze_problem_type(self, problem_statement: str) -> str:
        """分析问题类型"""
        statement_lower = problem_statement.lower()
        
        if any(word in statement_lower for word in ['编程', 'python', 'java', 'javascript', '代码']):
            return "programming"
        elif any(word in statement_lower for word in ['数学', '算法', '公式', '计算']):
            return "mathematics"
        elif any(word in statement_lower for word in ['英语', '语言', '单词', '语法']):
            return "language"
        else:
            return "general"
    
    def _generate_programming_subtasks(self, path: List[str]) -> List[SubTaskCreate]:
        """生成编程相关的子任务"""
        return [
            SubTaskCreate(
                name="环境搭建和基础配置",
                description="设置开发环境，安装必要的工具和库",
                order=1,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            ),
            SubTaskCreate(
                name="核心概念理解和语法学习",
                description="学习基础语法和核心编程概念",
                order=2,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name="实践项目和代码练习",
                description="通过实际编程项目巩固所学知识",
                order=3,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            )
        ]
    
    def _generate_math_subtasks(self, path: List[str]) -> List[SubTaskCreate]:
        """生成数学相关的子任务"""
        return [
            SubTaskCreate(
                name="基础概念和定义理解",
                description="理解相关的数学概念、定义和基本原理",
                order=1,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name="公式推导和证明过程",
                description="掌握重要公式的推导过程和证明方法",
                order=2,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name="例题练习和应用实践",
                description="通过典型例题和实际应用巩固理解",
                order=3,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            )
        ]
    
    def _generate_language_subtasks(self, path: List[str]) -> List[SubTaskCreate]:
        """生成语言学习相关的子任务"""
        return [
            SubTaskCreate(
                name="词汇积累和基础语法",
                description="学习核心词汇和基本语法规则",
                order=1,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            ),
            SubTaskCreate(
                name="听说读写综合训练",
                description="通过多种方式训练语言技能",
                order=2,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name="实际交流和应用练习",
                description="在真实场景中应用所学语言知识",
                order=3,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            )
        ]
    
    def _generate_general_subtasks(self, path: List[str]) -> List[SubTaskCreate]:
        """生成通用的子任务"""
        return [
            SubTaskCreate(
                name="基础知识学习",
                description="学习相关的基础知识和核心概念",
                order=1,
                mastery_expectation=MasteryLevel.INTUITIVE_UNDERSTANDING
            ),
            SubTaskCreate(
                name="深入理解和分析",
                description="深入分析和理解关键内容",
                order=2,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            ),
            SubTaskCreate(
                name="实践应用和总结",
                description="通过实践应用巩固学习成果",
                order=3,
                mastery_expectation=MasteryLevel.SEMANTIC_DERIVATION
            )
        ]
