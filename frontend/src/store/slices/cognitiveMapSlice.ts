import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { cognitiveMapAPI } from '../../services/api';

export interface CognitiveNode {
  id: string;
  name: string;
  description?: string;
  x: number;
  y: number;
  created_at?: string;
}

export interface CognitiveEdge {
  id: string;
  source_id: string;
  target_id: string;
  relationship_type: string;
  custom_name?: string;
  created_at?: string;
}

export interface CognitiveMap {
  id: string;
  session_id: string;
  nodes: CognitiveNode[];
  edges: CognitiveEdge[];
  created_at?: string;
  updated_at?: string;
}

interface CognitiveMapState {
  currentMap: CognitiveMap | null;
  selectedEdgeId: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: CognitiveMapState = {
  currentMap: null,
  selectedEdgeId: null,
  loading: false,
  error: null,
};

// 异步操作
export const createCognitiveMap = createAsyncThunk(
  'cognitiveMap/create',
  async (mapData: {
    session_id: string;
    nodes: Array<{
      name: string;
      description?: string;
      x: number;
      y: number;
    }>;
    edges: Array<{
      source_id: string;
      target_id: string;
      relationship_type: string;
      custom_name?: string;
    }>;
  }) => {
    const response = await cognitiveMapAPI.createMap(mapData);
    return response.data;
  }
);

export const fetchCognitiveMap = createAsyncThunk(
  'cognitiveMap/fetch',
  async (mapId: string) => {
    const response = await cognitiveMapAPI.getMap(mapId);
    return response.data;
  }
);

export const updateCognitiveMap = createAsyncThunk(
  'cognitiveMap/update',
  async ({ mapId, mapData }: {
    mapId: string;
    mapData: {
      session_id: string;
      nodes: Array<{
        name: string;
        description?: string;
        x: number;
        y: number;
      }>;
      edges: Array<{
        source_id: string;
        target_id: string;
        relationship_type: string;
        custom_name?: string;
      }>;
    };
  }) => {
    const response = await cognitiveMapAPI.updateMap(mapId, mapData);
    return response.data;
  }
);

export const selectEdge = createAsyncThunk(
  'cognitiveMap/selectEdge',
  async ({ mapId, edgeId }: { mapId: string; edgeId: string }) => {
    await cognitiveMapAPI.selectEdge(mapId, edgeId);
    return edgeId;
  }
);

const cognitiveMapSlice = createSlice({
  name: 'cognitiveMap',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedEdge: (state, action: PayloadAction<string | null>) => {
      state.selectedEdgeId = action.payload;
    },
    updateNodePosition: (state, action: PayloadAction<{ nodeId: string; x: number; y: number }>) => {
      if (state.currentMap) {
        const node = state.currentMap.nodes.find(n => n.id === action.payload.nodeId);
        if (node) {
          node.x = action.payload.x;
          node.y = action.payload.y;
        }
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Create map
      .addCase(createCognitiveMap.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createCognitiveMap.fulfilled, (state, action) => {
        state.loading = false;
        state.currentMap = action.payload;
      })
      .addCase(createCognitiveMap.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to create cognitive map';
      })
      // Fetch map
      .addCase(fetchCognitiveMap.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCognitiveMap.fulfilled, (state, action) => {
        state.loading = false;
        state.currentMap = action.payload;
      })
      .addCase(fetchCognitiveMap.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch cognitive map';
      })
      // Update map
      .addCase(updateCognitiveMap.fulfilled, (state, action) => {
        state.currentMap = action.payload;
      })
      // Select edge
      .addCase(selectEdge.fulfilled, (state, action) => {
        state.selectedEdgeId = action.payload;
      });
  },
});

export const { clearError, setSelectedEdge, updateNodePosition } = cognitiveMapSlice.actions;
export default cognitiveMapSlice.reducer;
