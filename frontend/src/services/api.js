import axios from 'axios';

// Create axios instance
const API = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
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
                        'http://127.0.0.1:8000/api/auth/refresh/',
                        { refresh: refreshToken }
                    );
                    const newAccessToken = response.data.access;
                    localStorage.setItem('access_token', newAccessToken);
                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return API(originalRequest);
                } catch (refreshError) {
                    // Refresh failed, clear tokens
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