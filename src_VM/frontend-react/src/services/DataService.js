import { BASE_API_URL, uuid } from "./Common";
import axios from 'axios';

// Create an axios instance with base configuration
const api = axios.create({
    baseURL: BASE_API_URL
});
// Add request interceptor to include session ID in headers
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
        // Any application initialization logic comes here
    },
    Getbird_sounds: async function (limit) {
        return await api.get("/api/bird_sounds/?limit=" + limit);
    },
    Getbird_sound: async function (bird_sound_id) {
        return await api.get(BASE_API_URL + "/bird_sounds/" + bird_sound_id);
    },
    Getbird_soundAudio: function (audio_path) {
        return "/assets/" + audio_path;
    },
    Getbird_maps: async function (limit) {
        return await api.get(BASE_API_URL + "/bird_maps/?limit=" + limit);
    },
    Getbird_map: async function (bird_map_id) {
        return await api.get(BASE_API_URL + "/bird_maps/" + bird_map_id);
    },
    GetChats: async function (model, limit) {
        return await api.get(BASE_API_URL + "/" + model + "/chats/?limit=" + limit);
    },
    GetChat: async function (model, chat_id) {
        return await api.get(BASE_API_URL + "/" + model + "/chats/" + chat_id);
    },
    StartChatWithLLM: async function (model, message) {
        return await api.post(BASE_API_URL + "/" + model + "/chats/", message);
    },
    ContinueChatWithLLM: async function (model, chat_id, message) {
        return await api.post(BASE_API_URL + "/" + model + "/chats/" + chat_id, message);
    },
    GetChatMessageImage: function (model, image_path) {
        return BASE_API_URL + "/" + model + "/" + image_path;
    },
    GetChatAudioURL: function (model, audio_path) {
        return `${BASE_API_URL}/${model}/${audio_path}`;
    },
}

export default DataService;