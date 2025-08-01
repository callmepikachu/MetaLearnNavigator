import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Typography,
  CircularProgress,
  Alert,
  Paper,
  Grid
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAppContext } from '../Layout/MainLayout';

const TaskDecomposition: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [decompositionResult, setDecompositionResult] = useState<any>(null);

  const location = useLocation();
  const navigate = useNavigate();
  const { setCognitiveMapData } = useAppContext();
  const problemStatement = location.state?.problemStatement || '';

  useEffect(() => {
    if (problemStatement && !decompositionResult) {
      handleTaskDecomposition();
    }
  }, [problemStatement]);

  const handleTaskDecomposition = async () => {
    if (!problemStatement) {
      setError('未找到问题描述');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 调用任务拆解API
      const response = await axios.post('http://localhost:8000/api/external/task-decomposition', {
        problem_statement: problemStatement
      });

      setDecompositionResult(response.data);
      console.log('任务拆解结果:', response.data);

      // 转换数据格式并设置到认知地图
      const nodes = response.data.nodes.map((node: any, index: number) => ({
        id: `node_${index}`,
        name: node.name,
        description: node.description,
        x: node.x || Math.random() * 400 + 100,
        y: node.y || Math.random() * 300 + 100
      }));

      const edges = response.data.edges.map((edge: any, index: number) => {
        // 简化处理：使用索引来映射源和目标节点
        const sourceIndex = Math.floor(Math.random() * nodes.length);
        let targetIndex = Math.floor(Math.random() * nodes.length);
        // 确保源和目标不同
        while (targetIndex === sourceIndex && nodes.length > 1) {
          targetIndex = Math.floor(Math.random() * nodes.length);
        }

        return {
          id: `edge_${index}`,
          source: `node_${sourceIndex}`,
          target: `node_${targetIndex}`,
          relationship_type: edge.relationship_type,
          custom_name: edge.custom_name
        };
      });

      const mapData = { nodes, edges };
      setCognitiveMapData(mapData);

    } catch (err: any) {
      setError(err.response?.data?.detail || '任务拆解失败');
      console.error('任务拆解错误:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextStep = () => {
    // 这里可以进入下一步，比如重要性选择
    alert('下一步功能开发中...');
  };

  if (!problemStatement) {
    return (
      <Alert severity="warning">
        请先输入学习问题
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        任务拆解
      </Typography>
      
      <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: 'info.light' }}>
        <Typography variant="body2" color="info.contrastText">
          <strong>学习问题：</strong>{problemStatement}
        </Typography>
      </Paper>

      <Typography variant="body1" color="text.secondary" paragraph>
        系统正在分析您的学习问题，并生成认知地图结构...
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {loading && (
        <Box display="flex" alignItems="center" sx={{ mb: 2 }}>
          <CircularProgress size={20} sx={{ mr: 1 }} />
          <Typography variant="body2">
            正在进行任务拆解...
          </Typography>
        </Box>
      )}

      {decompositionResult && (
        <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            ✅ 拆解结果
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            已生成 {decompositionResult.nodes?.length || 0} 个节点和 {decompositionResult.edges?.length || 0} 个连接关系
          </Typography>

          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                生成的节点：
              </Typography>
              {decompositionResult.nodes?.slice(0, 4).map((node: any, index: number) => (
                <Typography key={index} variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                  • {node.name}
                </Typography>
              ))}
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle2" gutterBottom>
                关系类型：
              </Typography>
              {decompositionResult.edges?.slice(0, 4).map((edge: any, index: number) => (
                <Typography key={index} variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                  • {edge.relationship_type}
                </Typography>
              ))}
            </Grid>
          </Grid>

          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            💡 认知地图将显示在左侧面板中，您可以对其进行编辑和调整。
          </Typography>
        </Paper>
      )}

      <Box sx={{ mt: 3 }}>
        <Button
          variant="contained"
          onClick={handleNextStep}
          disabled={loading || !decompositionResult}
          size="large"
        >
          进入下一步: 任务重要性判断
        </Button>
      </Box>

      <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="body2" color="text.secondary">
          💡 提示：认知地图显示了学习任务之间的关系：
        </Typography>
        <Typography variant="body2" color="text.secondary" component="div" sx={{ mt: 1 }}>
          • <strong>上级</strong>：更高层次的概念<br/>
          • <strong>下级</strong>：更具体的子概念<br/>
          • <strong>并列</strong>：同等重要的概念<br/>
          • <strong>相关</strong>：有关联的概念
        </Typography>
      </Box>
    </Box>
  );
};

export default TaskDecomposition;
