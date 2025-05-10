'use client';

import { useState, use, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatInput from '@/components/chat/ChatInput';
import ChatHistory from '@/components/chat/ChatHistory';
import ChatHistorySidebar from '@/components/chat/ChatHistorySidebar';
import ChatMessage from '@/components/chat/ChatMessage';
import DataService from "../../services/DataService";
import { uuid } from "../../services/Common";
import styles from "./styles.module.css";

export default function ChatPage({ searchParams }) {
    const params = use(searchParams);
    const chat_id = params.id;
    const model = params.model || 'llm-cnn';

    const [chatId, setChatId] = useState(chat_id);
    const [hasActiveChat, setHasActiveChat] = useState(false);
    const [chat, setChat] = useState(null);
    const [refreshKey, setRefreshKey] = useState(0);
    const [isTyping, setIsTyping] = useState(false);
    const [selectedModel, setSelectedModel] = useState(model);
    const router = useRouter();

    const fetchChat = async (id) => {
        try {
            setChat(null);
            const response = await DataService.GetChat(model, id);
            setChat(response.data);
        } catch (error) {
            console.error('Error fetching chat:', error);
            setChat(null);
        }
    };

    useEffect(() => {
        if (chat_id) {
            fetchChat(chat_id);
            setHasActiveChat(true);
        } else {
            setChat(null);
            setHasActiveChat(false);
        }
    }, [chat_id]);

    useEffect(() => {
        setSelectedModel(model);
    }, [model]);

    function tempChatMessage(message) {
        try {
            message["message_id"] = uuid();
            message["role"] = 'user';
    
            // Replace placeholder for audio upload with a user-friendly message
            if (message.content === "[AUDIO_UPLOAD]") {
                message.content = "An audio file has been uploaded";
            }
    
            const existingMessages = chat?.messages || [];
            return {
                ...chat,
                messages: [...existingMessages, message]
            };
        } catch (e) {
            console.error("Error in tempChatMessage:", e);
            return { messages: [message] };
        }
    }

    const newChat = (message) => {
        const startChat = async (message) => {
            try {
                setIsTyping(true);
                setHasActiveChat(true);

                const temp = tempChatMessage(message);
                if (temp) setChat(temp);

                const response = await DataService.StartChatWithLLM(model, message);
                setIsTyping(false);
                setChat(response.data);
                setChatId(response.data["chat_id"]);
                router.push(`/chat?model=${selectedModel}&id=${response.data["chat_id"]}`);
            } catch (error) {
                console.error('Error starting chat:', error);
                setIsTyping(false);
                setChat(null);
                setChatId(null);
                setHasActiveChat(false);
                router.push(`/chat?model=${selectedModel}`);
            }
        };
        startChat(message);
    };

    const appendChat = (message) => {
        const continueChat = async (id, message) => {
            try {
                setIsTyping(true);
                setHasActiveChat(true);

                const temp = tempChatMessage(message);
                if (temp) setChat(temp);

                const response = await DataService.ContinueChatWithLLM(model, id, message);
                setIsTyping(false);
                setChat(response.data);
                forceRefresh();
            } catch (error) {
                console.error('Error continuing chat:', error);
                setIsTyping(false);
                setChat(null);
                setHasActiveChat(false);
            }
        };
        continueChat(chatId, message);
    };

    const forceRefresh = () => {
        setRefreshKey(prevKey => prevKey + 1);
    };

    const handleModelChange = (newValue) => {
        setSelectedModel(newValue);
        let path = `/chat?model=${newValue}`;
        if (chatId) path += `&id=${chatId}`;
        router.push(path);
    };

    return (
        <div className={styles.container}>
            {!hasActiveChat && (
                <section className={styles.hero}>
                    <div className={styles.heroContent}>
                        <h1>Bird Assistant</h1>
                        <ChatInput
                            onSendMessage={newChat}
                            className={styles.heroChatInputContainer}
                            selectedModel={selectedModel}
                            onModelChange={handleModelChange}
                        />
                    </div>
                </section>
            )}

            {!hasActiveChat && <ChatHistory model={model} />}

            {hasActiveChat && <div className={styles.chatHeader}></div>}

            {hasActiveChat && (
                <div className={styles.chatInterface}>
                    <ChatHistorySidebar chat_id={chat_id} model={model} />
                    <div className={styles.mainContent}>
                        <ChatMessage
                            chat={chat}
                            key={refreshKey}
                            isTyping={isTyping}
                            model={model}
                        />
                        <ChatInput
                            onSendMessage={appendChat}
                            chat={chat}
                            selectedModel={selectedModel}
                            onModelChange={setSelectedModel}
                            disableModelSelect={true}
                        />
                    </div>
                </div>
            )}
        </div>
    );
}
