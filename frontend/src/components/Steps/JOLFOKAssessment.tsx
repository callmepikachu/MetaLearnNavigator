import React from 'react';
import { Box, Typography } from '@mui/material';

const JOLFOKAssessment: React.FC = () => {
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        JOL/FOK评估
      </Typography>
      
      <Typography variant="body1" color="text.secondary">
        请评估您的学习能力...
      </Typography>
    </Box>
  );
};

export default JOLFOKAssessment;
