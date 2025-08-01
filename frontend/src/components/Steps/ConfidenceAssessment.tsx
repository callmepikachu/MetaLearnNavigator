import React from 'react';
import { Box, Typography } from '@mui/material';

const ConfidenceAssessment: React.FC = () => {
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        信心评估
      </Typography>
      
      <Typography variant="body1" color="text.secondary">
        请评估您完成任务的信心...
      </Typography>
    </Box>
  );
};

export default ConfidenceAssessment;
