import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, Typography, Paper, Box } from '@mui/material';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", "Microsoft YaHei", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 2 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          MetaLearnNavigator
        </Typography>
        <Typography variant="subtitle1" gutterBottom align="center" color="text.secondary">
          元认知学习导航器
        </Typography>
        
        <Box sx={{ mt: 4 }}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              🎉 系统启动成功！
            </Typography>
            <Typography variant="body1" paragraph>
              前端和后端服务都已正常启动。
            </Typography>
            <Typography variant="body2" color="text.secondary">
              • 后端API: http://localhost:8000<br/>
              • API文档: http://localhost:8000/docs<br/>
              • 前端应用: http://localhost:3000
            </Typography>
          </Paper>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
