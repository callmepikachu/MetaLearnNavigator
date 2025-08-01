import React from 'react';
import { Box, Typography } from '@mui/material';

const TimeAllocation: React.FC = () => {
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        学习时间分配
      </Typography>
      
      <Typography variant="body1" color="text.secondary">
        请选择您的学习时间...
      </Typography>
    </Box>
  );
};

export default TimeAllocation;
