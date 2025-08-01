import React from 'react';
import { Box, Typography } from '@mui/material';

const SubTaskGeneration: React.FC = () => {
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        子任务生成
      </Typography>
      
      <Typography variant="body1" color="text.secondary">
        基于您选择的重要连线，系统正在生成子任务...
      </Typography>
    </Box>
  );
};

export default SubTaskGeneration;
