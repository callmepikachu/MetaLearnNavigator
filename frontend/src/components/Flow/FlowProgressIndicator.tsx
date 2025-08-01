import React from 'react';
import { Box, Stepper, Step, StepLabel, Typography } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../../store/store';

const FlowProgressIndicator: React.FC = () => {
  const currentSession = useSelector((state: RootState) => state.learningSession.currentSession);

  const steps = [
    { key: 'problem_input', label: '问题输入' },
    { key: 'task_decomposition', label: '任务拆解' },
    { key: 'importance_selection', label: '重要性判断' },
    { key: 'sub_task_generation', label: '子任务生成' },
    { key: 'expectation_setting', label: '预期设置' },
    { key: 'jol_fok_assessment', label: 'JOL/FOK评估' },
    { key: 'expectation_comparison', label: '预期对比' },
    { key: 'eol_difficulty_assessment', label: 'EOL评估' },
    { key: 'confidence_assessment', label: '信心评估' },
    { key: 'time_allocation', label: '时间分配' },
    { key: 'learning_in_progress', label: '学习中' },
    { key: 'strategy_selection', label: '策略选择' },
    { key: 'obstacle_assessment', label: '阻碍评估' },
    { key: 'reflection_monitoring', label: '回流监控' },
  ];

  const getCurrentStepIndex = () => {
    if (!currentSession) return 0;
    const index = steps.findIndex(step => step.key === currentSession.current_step);
    return index >= 0 ? index : 0;
  };

  const currentStepIndex = getCurrentStepIndex();

  return (
    <Box sx={{ width: '100%', mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        学习进度
      </Typography>
      
      {currentSession && (
        <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            当前问题：
          </Typography>
          <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
            {currentSession.problem_statement}
          </Typography>
        </Box>
      )}

      <Stepper activeStep={currentStepIndex} orientation="vertical">
        {steps.map((step, index) => (
          <Step key={step.key}>
            <StepLabel>
              <Typography 
                variant="body2" 
                color={index === currentStepIndex ? 'primary' : 'text.secondary'}
                sx={{ fontWeight: index === currentStepIndex ? 'bold' : 'normal' }}
              >
                {step.label}
              </Typography>
            </StepLabel>
          </Step>
        ))}
      </Stepper>

      {currentSession && (
        <Box sx={{ mt: 2, p: 1, bgcolor: 'info.light', borderRadius: 1 }}>
          <Typography variant="caption" color="info.contrastText">
            当前步骤: {steps[currentStepIndex]?.label || '未知步骤'}
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default FlowProgressIndicator;
