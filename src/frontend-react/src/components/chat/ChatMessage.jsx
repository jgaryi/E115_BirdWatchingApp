'use client';

import { useRef, useEffect } from 'react';
import { Person, SmartToy } from '@mui/icons-material';
import ForumIcon from '@mui/icons-material/Forum';
import RemoveRedEyeIcon from '@mui/icons-material/RemoveRedEye';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import DataService from "../../services/DataService";

// Styles
import styles from './ChatMessage.module.css';

export default function ChatMessage({
    chat,
    isTyping,
    model
}) {
    const chatHistoryRef = useRef(null);

    useEffect(() => {
        if (chatHistoryRef.current) {
            chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
        }
    }, [chat, isTyping]);

    const formatTime = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <>
            {chat &&
                <div className={styles.chatTitle}>
                    <div className={styles.chatTitleIcon}>
                        <ForumIcon sx={{ fontSize: 28 }} />
                    </div>
                    <h1 className={styles.chatTitleText}>
                        {chat.title}
                    </h1>
                </div>
            }
            <div className={styles.chatHistory} ref={chatHistoryRef}>
                {chat && chat.messages.map((msg) => (
                    <div
                        key={msg.message_id}
                        className={`${styles.message} ${styles[msg.role]}`}
                    >
                        <div className={styles.messageIcon}>
                            {msg.role === 'assistant' && (
                                <SmartToy sx={{ color: '#FFD700' }} />
                            )}
                            {msg.role === 'cnn' && (
                                <RemoveRedEyeIcon sx={{ color: '#D700EE' }} />
                            )}
                            {msg.role === 'user' && (
                                <Person sx={{ color: '#FFFFFF' }} />
                            )}
                        </div>
                        <div className={styles.messageContent}>
                            {/* User-uploaded audio (from preview) */}
                            {msg.audio && (
                                <div className={styles.messageAudio}>
                                    {msg.name && (
                                        <div className={styles.audioFileName}>
                                            {msg.name}
                                        </div>
                                    )}
                                    <audio controls src={msg.audio}></audio>
                                </div>
                            )}

                            {/* Audio file saved from backend */}
                            {msg.audio_path && (
                                <div className={styles.messageAudio}>
                                    <audio controls src={DataService.GetChatAudioURL(model, msg.audio_path)} />
                                </div>
                            )}

                            {/* Additional text below audio if uploaded + question */}
                            {msg.audio && msg.role === 'user' && msg.content && (
                                <div className={styles.audioQuestion}>
                                    {msg.content}
                                </div>
                            )}

                            {/* Image preview (direct) */}
                            {msg.image && (
                                <div className={styles.messageImage}>
                                    <img
                                        src={msg.image}
                                        alt="Chat Image"
                                    />
                                </div>
                            )}

                            {/* Image preview (from saved path) */}
                            {msg.image_path && (
                                <div className={styles.messageImage}>
                                    <img
                                        src={DataService.GetChatMessageImage(model, msg.image_path)}
                                        alt="Chat Image"
                                    />
                                </div>
                            )}

                            {/* Render markdown for assistant/user content */}
                            {msg.content && (!msg.audio || msg.role === 'assistant') && (
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    rehypePlugins={[rehypeRaw]}
                                    components={{
                                        a: ({ node, ...props }) => (
                                            <a className={styles.link} {...props} target="_blank" rel="noopener noreferrer" />
                                        ),
                                        ul: ({ node, ...props }) => (
                                            <ul className={styles.list} {...props} />
                                        ),
                                        ol: ({ node, ...props }) => (
                                            <ol className={styles.list} {...props} />
                                        ),
                                        blockquote: ({ node, ...props }) => (
                                            <blockquote className={styles.blockquote} {...props} />
                                        ),
                                    }}
                                >
                                    {msg.content}
                                </ReactMarkdown>
                            )}

                            {/* Optional results (CNN model) */}
                            {msg.results && (
                                <div>{msg.results.prediction_label}&nbsp; ({msg.results.accuracy}%)</div>
                            )}
                        </div>
                        {msg.timestamp && (
                            <span className={styles.messageTime}>
                                {formatTime(msg.timestamp)}
                            </span>
                        )}
                    </div>
                ))}

                {isTyping && (
                    <div className={`${styles.message} ${styles.assistant}`}>
                        <div className={styles.messageContent}>
                            <div className={styles.typingIndicator}>
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
