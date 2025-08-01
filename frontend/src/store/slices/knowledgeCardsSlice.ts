import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { knowledgeCardsAPI } from '../../services/api';

export interface KnowledgeCard {
  id: string;
  title: string;
  content: string;
  keywords: string[];
  created_at?: string;
  updated_at?: string;
}

interface KnowledgeCardsState {
  cards: KnowledgeCard[];
  searchResults: KnowledgeCard[];
  loading: boolean;
  error: string | null;
}

const initialState: KnowledgeCardsState = {
  cards: [],
  searchResults: [],
  loading: false,
  error: null,
};

// 异步操作
export const fetchKnowledgeCards = createAsyncThunk(
  'knowledgeCards/fetchCards',
  async (params?: { skip?: number; limit?: number }) => {
    const response = await knowledgeCardsAPI.getCards(params);
    return response.data;
  }
);

export const searchKnowledgeCards = createAsyncThunk(
  'knowledgeCards/search',
  async ({ query, limit }: { query: string; limit?: number }) => {
    const response = await knowledgeCardsAPI.searchCards(query, limit);
    return response.data;
  }
);

export const searchByKeywords = createAsyncThunk(
  'knowledgeCards/searchByKeywords',
  async ({ keywords, limit }: { keywords: string[]; limit?: number }) => {
    const response = await knowledgeCardsAPI.searchByKeywords(keywords, limit);
    return response.data;
  }
);

export const createKnowledgeCard = createAsyncThunk(
  'knowledgeCards/create',
  async (cardData: {
    title: string;
    content: string;
    keywords: string[];
  }) => {
    const response = await knowledgeCardsAPI.createCard(cardData);
    return response.data;
  }
);

const knowledgeCardsSlice = createSlice({
  name: 'knowledgeCards',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearSearchResults: (state) => {
      state.searchResults = [];
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch cards
      .addCase(fetchKnowledgeCards.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchKnowledgeCards.fulfilled, (state, action) => {
        state.loading = false;
        state.cards = action.payload;
      })
      .addCase(fetchKnowledgeCards.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch knowledge cards';
      })
      // Search cards
      .addCase(searchKnowledgeCards.fulfilled, (state, action) => {
        state.searchResults = action.payload;
      })
      .addCase(searchByKeywords.fulfilled, (state, action) => {
        state.searchResults = action.payload;
      })
      // Create card
      .addCase(createKnowledgeCard.fulfilled, (state, action) => {
        state.cards.unshift(action.payload);
      });
  },
});

export const { clearError, clearSearchResults } = knowledgeCardsSlice.actions;
export default knowledgeCardsSlice.reducer;
