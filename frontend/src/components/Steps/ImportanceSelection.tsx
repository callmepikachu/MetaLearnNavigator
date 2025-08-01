import React from 'react';
import { Box, Typography, Alert } from '@mui/material';

const ImportanceSelection: React.FC = () => {
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        任务重要性判断
      </Typography>
      
      <Alert severity="info" sx={{ mb: 2 }}>
        选择重要的，而不是简单的
      </Alert>
      
      <Typography variant="body1" color="text.secondary">
        请在左侧的认知地图上选择最重要的连线。点击连线后，系统将生成相应的子任务。
      </Typography>
    </Box>
  );
};

export default ImportanceSelection;
