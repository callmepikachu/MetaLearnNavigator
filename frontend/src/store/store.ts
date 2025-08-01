import { configureStore } from '@reduxjs/toolkit';
import learningSessionReducer from './slices/learningSessionSlice';
import cognitiveMapReducer from './slices/cognitiveMapSlice';
import knowledgeCardsReducer from './slices/knowledgeCardsSlice';

export const store = configureStore({
  reducer: {
    learningSession: learningSessionReducer,
    cognitiveMap: cognitiveMapReducer,
    knowledgeCards: knowledgeCardsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
