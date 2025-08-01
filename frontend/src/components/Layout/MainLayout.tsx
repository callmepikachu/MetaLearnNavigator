import React, { createContext, useContext, useState } from 'react';
import { Box, Container, Grid, Paper, Typography } from '@mui/material';
import SimpleCognitiveMapViewer from '../CognitiveMap/SimpleCognitiveMapViewer';

// 创建上下文来共享认知地图数据
interface CognitiveMapData {
  nodes: Array<{
    id: string;
    name: string;
    description?: string;
    x: number;
    y: number;
  }>;
  edges: Array<{
    id: string;
    source: string;
    target: string;
    relationship_type: string;
    custom_name?: string;
  }>;
}

interface AppContextType {
  cognitiveMapData: CognitiveMapData | null;
  setCognitiveMapData: (data: CognitiveMapData | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  return context;
};

interface MainLayoutProps {
  children: React.ReactNode;
}

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cognitiveMapData, setCognitiveMapData] = useState<CognitiveMapData | null>(null);

  return (
    <AppContext.Provider value={{ cognitiveMapData, setCognitiveMapData }}>
      {children}
    </AppContext.Provider>
  );
};

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { cognitiveMapData } = useAppContext();

  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        MetaLearnNavigator
      </Typography>
      <Typography variant="subtitle1" gutterBottom align="center" color="text.secondary">
        元认知学习导航器
      </Typography>

      <Grid container spacing={2} sx={{ mt: 2 }}>
        {/* 左侧：认知地图 */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '70vh' }}>
            <Typography variant="h6" gutterBottom>
              认知地图
              {cognitiveMapData && (
                <Typography component="span" variant="caption" sx={{ ml: 1, color: 'success.main' }}>
                  ({cognitiveMapData.nodes.length} 节点, {cognitiveMapData.edges.length} 连线)
                </Typography>
              )}
            </Typography>
            <Box sx={{ height: 'calc(100% - 40px)' }}>
              <SimpleCognitiveMapViewer mapData={cognitiveMapData} />
            </Box>
          </Paper>
        </Grid>

        {/* 右侧：学习流程 */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '70vh', overflow: 'auto' }}>
            <Typography variant="h6" gutterBottom>
              学习流程
            </Typography>
            <Box sx={{ mt: 2 }}>
              {children}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default MainLayout;
