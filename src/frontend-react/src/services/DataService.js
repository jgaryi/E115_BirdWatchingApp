import { BASE_API_URL, uuid } from "./Common";
import axios from 'axios';

// Create an axios instance with the base URL.
const api = axios.create({
    baseURL: BASE_API_URL
});

// Add request interceptor to include session ID in headers.
api.interceptors.request.use((config) => {
    const sessionId = localStorage.getItem('userSessionId');
    if (sessionId) {
        config.headers['X-Session-ID'] = sessionId;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

const DataService = {
    Init: function () {
        // Any application initialization logic comes here.
    },
    // Podcasts endpoints.
    GetPodcasts: async function (limit) {
        return await api.get("/podcasts?limit=" + limit);
    },
    GetPodcast: async function (podcast_id) {
        return await api.get("/podcasts/" + podcast_id);
    },
    GetPodcastAudio: function (audio_path) {
        return BASE_API_URL + "/podcasts/audio/" + audio_path;
    },
    // Newsletters endpoints.
    GetNewsletters: async function (limit) {
        return await api.get("/newsletters?limit=" + limit);
    },
    GetNewsletter: async function (newsletter_id) {
        return await api.get("/newsletters/" + newsletter_id);
    },
    GetNewsletterImage: function (image_path) {
        return BASE_API_URL + "/newsletters/image/" + image_path;
    },
    // Chat endpoints – include the model as a prefix. For example, "llm-cnn".
    GetChats: async function (model, limit) {
        // Calls URL: BASE_API_URL + "/" + model + "/chats?limit=..."
        return await api.get("/" + model + "/chats?limit=" + limit);
    },
    GetChat: async function (model, chat_id) {
        // Calls URL: BASE_API_URL + "/" + model + "/chats/" + chat_id
        return await api.get("/" + model + "/chats/" + chat_id);
    },
    StartChatWithLLM: async function (model, message) {
        // Build a FormData object since the backend expects form data.
        const formData = new FormData();
        if (message.content) {
            formData.append('content', message.content);
        }
        if (message.file) {
            formData.append('file', message.file);
        }
        // Calls URL: BASE_API_URL + "/" + model + "/chats"
        return await api.post("/" + model + "/chats", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });
    },
    ContinueChatWithLLM: async function (model, chat_id, message) {
        const formData = new FormData();
        if (message.content) {
            formData.append('content', message.content);
        }
        if (message.file) {
            formData.append('file', message.file);
        }
        // Calls URL: BASE_API_URL + "/" + model + "/chats/" + chat_id
        return await api.post("/" + model + "/chats/" + chat_id, formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });
    },
    GetChatMessageImage: function (model, audio_path) {
        return BASE_API_URL + "/" + model + "/chat/message/audio/" + audio_path;
    },
};

export default DataService;
