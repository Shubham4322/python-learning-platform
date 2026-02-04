import axios from 'axios';

// API URL - Use environment variable or fallback
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://pylearn-backend.onrender.com/api';

console.log('API URL:', API_BASE_URL); // For debugging

// Create axios instance
const API = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests if it exists
API.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle token refresh on 401 errors
API.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const response = await axios.post(
                        `${API_BASE_URL}/auth/refresh/`,
                        { refresh: refreshToken }
                    );
                    const newAccessToken = response.data.access;
                    localStorage.setItem('access_token', newAccessToken);
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return API(originalRequest);
                } catch (refreshError) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);

// ==================== AUTH API ====================

export const registerUser = async (userData) => {
    const response = await API.post('/auth/register/', userData);
    return response.data;
};

export const loginUser = async (credentials) => {
    const response = await API.post('/auth/login/', credentials);
    return response.data;
};

export const getUser = async () => {
    const response = await API.get('/auth/user/');
    return response.data;
};

// ==================== DASHBOARD API ====================

export const getDashboard = async () => {
    const response = await API.get('/dashboard/');
    return response.data;
};

// ==================== TOPICS API ====================

export const getTopics = async () => {
    const response = await API.get('/topics/');
    return response.data;
};

export const getTopic = async (topicId) => {
    const response = await API.get(`/topics/${topicId}/`);
    return response.data;
};

// ==================== QUESTIONS API ====================

export const getQuestion = async (questionId) => {
    const response = await API.get(`/questions/${questionId}/`);
    return response.data;
};

export const runCode = async (code) => {
    const response = await API.post('/run-code/', { code });
    return response.data;
};

export const submitCode = async (questionId, code) => {
    const response = await API.post(`/submit/${questionId}/`, { code });
    return response.data;
};

export default API;