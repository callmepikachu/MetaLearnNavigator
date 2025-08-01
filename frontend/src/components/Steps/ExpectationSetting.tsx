import React from 'react';
import { Box, Typography } from '@mui/material';

const ExpectationSetting: React.FC = () => {
  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        预期掌握程度设置
      </Typography>
      
      <Typography variant="body1" color="text.secondary">
        请设置您对各个任务的预期掌握程度...
      </Typography>
    </Box>
  );
};

export default ExpectationSetting;
