import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// 学习会话相关API
export const learningSessionAPI = {
  createSession: (data: { problem_statement: string }) =>
    apiClient.post('/learning-flow/sessions', data),
  
  getSession: (sessionId: string) =>
    apiClient.get(`/learning-flow/sessions/${sessionId}`),
  
  updateFlowState: (sessionId: string, data: {
    session_id: string;
    current_step: string;
    step_data: Record<string, any>;
  }) =>
    apiClient.put(`/learning-flow/sessions/${sessionId}/flow-state`, data),
  
  submitJOLAssessment: (sessionId: string, data: {
    session_id: string;
    assessment: string;
  }) =>
    apiClient.post(`/learning-flow/sessions/${sessionId}/jol-assessment`, data),
  
  submitFOKAssessment: (sessionId: string, data: {
    session_id: string;
    assessment: string;
  }) =>
    apiClient.post(`/learning-flow/sessions/${sessionId}/fok-assessment`, data),
  
  submitConfidenceAssessment: (sessionId: string, data: {
    session_id: string;
    confidence: string;
  }) =>
    apiClient.post(`/learning-flow/sessions/${sessionId}/confidence-assessment`, data),
  
  submitTimeAllocation: (sessionId: string, data: {
    session_id: string;
    time_allocation: string;
  }) =>
    apiClient.post(`/learning-flow/sessions/${sessionId}/time-allocation`, data),
  
  createSubTasks: (sessionId: string, data: Array<{
    name: string;
    description?: string;
    order: number;
    mastery_expectation?: string;
  }>) =>
    apiClient.post(`/learning-flow/sessions/${sessionId}/sub-tasks`, data),
};

// 认知地图相关API
export const cognitiveMapAPI = {
  createMap: (data: {
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
  }) =>
    apiClient.post('/cognitive-map/', data),
  
  getMap: (mapId: string) =>
    apiClient.get(`/cognitive-map/${mapId}`),
  
  updateMap: (mapId: string, data: {
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
  }) =>
    apiClient.put(`/cognitive-map/${mapId}`, data),
  
  selectEdge: (mapId: string, edgeId: string) =>
    apiClient.post(`/cognitive-map/${mapId}/select-edge`, { edge_id: edgeId }),
};

// 知识卡片相关API
export const knowledgeCardsAPI = {
  createCard: (data: {
    title: string;
    content: string;
    keywords: string[];
  }) =>
    apiClient.post('/knowledge-cards/', data),
  
  getCards: (params?: { skip?: number; limit?: number }) =>
    apiClient.get('/knowledge-cards/', { params }),
  
  getCard: (cardId: string) =>
    apiClient.get(`/knowledge-cards/${cardId}`),
  
  updateCard: (cardId: string, data: {
    title: string;
    content: string;
    keywords: string[];
  }) =>
    apiClient.put(`/knowledge-cards/${cardId}`, data),
  
  deleteCard: (cardId: string) =>
    apiClient.delete(`/knowledge-cards/${cardId}`),
  
  searchCards: (query: string, limit?: number) =>
    apiClient.get('/knowledge-cards/search/', { params: { query, limit } }),
  
  searchByKeywords: (keywords: string[], limit?: number) =>
    apiClient.post('/knowledge-cards/search/by-keywords', keywords, { params: { limit } }),
};

// 外部API集成
export const externalAPI = {
  decomposeTask: (data: { problem_statement: string }) =>
    apiClient.post('/external/task-decomposition', data),
  
  searchResources: (data: { query: string; task_context?: string }) =>
    apiClient.post('/external/resource-search', data),
  
  openaiTaskDecomposition: (data: { problem_statement: string }) =>
    apiClient.post('/external/openai-task-decomposition', data),
};

export default apiClient;
