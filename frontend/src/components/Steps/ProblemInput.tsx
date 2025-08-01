import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Alert,
  CircularProgress
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { AppDispatch, RootState } from '../../store/store';
import { createLearningSession } from '../../store/slices/learningSessionSlice';

const ProblemInput: React.FC = () => {
  const [problemStatement, setProblemStatement] = useState('');
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state: RootState) => state.learningSession);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!problemStatement.trim()) {
      return;
    }

    try {
      // 直接跳转到任务拆解页面，传递问题描述
      navigate('/task-decomposition', {
        state: { problemStatement: problemStatement.trim() }
      });
    } catch (error) {
      console.error('Failed to navigate:', error);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          开始你的学习之旅
        </Typography>
        <Typography variant="body1" gutterBottom align="center" color="text.secondary">
          请输入你想要学习的问题或主题
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            label="学习问题"
            placeholder="例如：我想学习机器学习的基础知识..."
            value={problemStatement}
            onChange={(e) => setProblemStatement(e.target.value)}
            sx={{ mb: 3 }}
            disabled={loading}
          />

          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              disabled={!problemStatement.trim() || loading}
              sx={{ minWidth: 200 }}
            >
              {loading ? (
                <>
                  <CircularProgress size={20} sx={{ mr: 1 }} />
                  创建学习会话...
                </>
              ) : (
                '开始学习'
              )}
            </Button>
          </Box>
        </form>

        <Box sx={{ mt: 4, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="h6" gutterBottom>
            💡 提示
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • 尽量具体描述你想学习的内容<br/>
            • 可以包含你的背景知识水平<br/>
            • 说明你希望达到的学习目标<br/>
            • 例如："我是编程初学者，想学习Python数据分析，希望能够处理Excel文件并制作图表"
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};

export default ProblemInput;
