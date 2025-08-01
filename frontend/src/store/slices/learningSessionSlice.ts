import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { learningSessionAPI } from '../../services/api';

export interface SubTask {
  id: string;
  name: string;
  description?: string;
  order: number;
  mastery_expectation?: string;
}

export interface LearningSession {
  id: string;
  problem_statement: string;
  current_step: string;
  cognitive_map_id?: string;
  selected_edge_id?: string;
  sub_tasks: SubTask[];
  session_data: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

interface LearningSessionState {
  currentSession: LearningSession | null;
  loading: boolean;
  error: string | null;
}

const initialState: LearningSessionState = {
  currentSession: null,
  loading: false,
  error: null,
};

// 异步操作
export const createLearningSession = createAsyncThunk(
  'learningSession/create',
  async (problemStatement: string) => {
    const response = await learningSessionAPI.createSession({ problem_statement: problemStatement });
    return response.data;
  }
);

export const fetchLearningSession = createAsyncThunk(
  'learningSession/fetch',
  async (sessionId: string) => {
    const response = await learningSessionAPI.getSession(sessionId);
    return response.data;
  }
);

export const updateFlowState = createAsyncThunk(
  'learningSession/updateFlowState',
  async ({ sessionId, currentStep, stepData }: {
    sessionId: string;
    currentStep: string;
    stepData?: Record<string, any>;
  }) => {
    await learningSessionAPI.updateFlowState(sessionId, {
      session_id: sessionId,
      current_step: currentStep,
      step_data: stepData || {},
    });
    return { currentStep, stepData };
  }
);

export const submitJOLAssessment = createAsyncThunk(
  'learningSession/submitJOL',
  async ({ sessionId, assessment }: { sessionId: string; assessment: string }) => {
    const response = await learningSessionAPI.submitJOLAssessment(sessionId, {
      session_id: sessionId,
      assessment: assessment as any,
    });
    return response.data;
  }
);

export const submitFOKAssessment = createAsyncThunk(
  'learningSession/submitFOK',
  async ({ sessionId, assessment }: { sessionId: string; assessment: string }) => {
    const response = await learningSessionAPI.submitFOKAssessment(sessionId, {
      session_id: sessionId,
      assessment: assessment as any,
    });
    return response.data;
  }
);

export const submitConfidenceAssessment = createAsyncThunk(
  'learningSession/submitConfidence',
  async ({ sessionId, confidence }: { sessionId: string; confidence: string }) => {
    const response = await learningSessionAPI.submitConfidenceAssessment(sessionId, {
      session_id: sessionId,
      confidence: confidence as any,
    });
    return response.data;
  }
);

export const submitTimeAllocation = createAsyncThunk(
  'learningSession/submitTimeAllocation',
  async ({ sessionId, timeAllocation }: { sessionId: string; timeAllocation: string }) => {
    const response = await learningSessionAPI.submitTimeAllocation(sessionId, {
      session_id: sessionId,
      time_allocation: timeAllocation as any,
    });
    return response.data;
  }
);

const learningSessionSlice = createSlice({
  name: 'learningSession',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    updateSessionData: (state, action: PayloadAction<Record<string, any>>) => {
      if (state.currentSession) {
        state.currentSession.session_data = {
          ...state.currentSession.session_data,
          ...action.payload,
        };
      }
    },
    setCurrentStep: (state, action: PayloadAction<string>) => {
      if (state.currentSession) {
        state.currentSession.current_step = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Create session
      .addCase(createLearningSession.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createLearningSession.fulfilled, (state, action) => {
        state.loading = false;
        state.currentSession = action.payload;
      })
      .addCase(createLearningSession.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to create session';
      })
      // Fetch session
      .addCase(fetchLearningSession.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLearningSession.fulfilled, (state, action) => {
        state.loading = false;
        state.currentSession = action.payload;
      })
      .addCase(fetchLearningSession.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch session';
      })
      // Update flow state
      .addCase(updateFlowState.fulfilled, (state, action) => {
        if (state.currentSession) {
          state.currentSession.current_step = action.payload.currentStep;
          if (action.payload.stepData) {
            state.currentSession.session_data = {
              ...state.currentSession.session_data,
              ...action.payload.stepData,
            };
          }
        }
      })
      // Assessment submissions
      .addCase(submitJOLAssessment.fulfilled, (state, action) => {
        if (state.currentSession) {
          state.currentSession.current_step = action.payload.next_step;
        }
      })
      .addCase(submitFOKAssessment.fulfilled, (state, action) => {
        if (state.currentSession) {
          state.currentSession.current_step = action.payload.next_step;
        }
      })
      .addCase(submitConfidenceAssessment.fulfilled, (state, action) => {
        if (state.currentSession) {
          state.currentSession.current_step = action.payload.next_step;
        }
      })
      .addCase(submitTimeAllocation.fulfilled, (state, action) => {
        if (state.currentSession) {
          state.currentSession.current_step = action.payload.next_step;
        }
      });
  },
});

export const { clearError, updateSessionData, setCurrentStep } = learningSessionSlice.actions;
export default learningSessionSlice.reducer;
