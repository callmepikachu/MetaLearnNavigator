import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { store } from './store/store';
import MainLayout, { AppProvider } from './components/Layout/MainLayout';
import ProblemInput from './components/Steps/ProblemInput';
import TaskDecomposition from './components/Steps/TaskDecomposition';
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
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AppProvider>
          <Router>
            <MainLayout>
              <Routes>
                <Route path="/" element={<ProblemInput />} />
                <Route path="/task-decomposition" element={<TaskDecomposition />} />
              </Routes>
            </MainLayout>
          </Router>
        </AppProvider>
      </ThemeProvider>
    </Provider>
  );
}

export default App;
