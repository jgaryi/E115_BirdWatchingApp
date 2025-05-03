'use client';

import { useState, useRef, useEffect } from 'react';
import { Send } from '@mui/icons-material';
import IconButton from '@mui/material/IconButton';
import { LibraryMusicOutlined } from '@mui/icons-material';
import styles from './ChatInput.module.css';

export default function ChatInput({
    onSendMessage,
    selectedModel,
    onModelChange,
    disableModelSelect = false
}) {
    const [message, setMessage] = useState('');
    const [selectedMedia, setSelectedMedia] = useState(null);
    const textAreaRef = useRef(null);
    const fileInputRef = useRef(null);

    const adjustTextAreaHeight = () => {
        const textarea = textAreaRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    };

    useEffect(() => {
        adjustTextAreaHeight();
    }, [message]);

    const handleSubmit = () => {
        if (message.trim() || selectedMedia) {
            const newMessage = {
                content: message.trim() || "[AUDIO_UPLOAD]",
                audio: selectedMedia?.preview || null,
                type: selectedMedia?.type || null,
                name: selectedMedia?.file?.name || "bird_audio.mp3" // ✅ Ensured filename is passed
            };

            onSendMessage(newMessage);

            setMessage('');
            setSelectedMedia(null);
            if (textAreaRef.current) textAreaRef.current.style.height = 'auto';
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files?.[0];
        if (file) {
            if (file.size > 10_000_000) {
                alert('File size should be less than 10MB');
                return;
            }

            const reader = new FileReader();
            reader.onloadend = () => {
                setSelectedMedia({
                    file: file,
                    preview: reader.result,
                    type: file.type.startsWith('audio') ? 'audio' : 'image'
                });
            };
            reader.readAsDataURL(file);
        }
    };

    const handleModelChange = (event) => {
        onModelChange(event.target.value);
    };

    const removeMedia = () => {
        setSelectedMedia(null);
        if (fileInputRef.current) fileInputRef.current.value = '';
    };

    return (
        <div className={styles.chatInputContainer}>
            {selectedMedia && (
                <div className={styles.imagePreview}>
                    {selectedMedia.file?.name && (
                        <div className={styles.audioFileName}>
                            🎵 Uploaded audio: <strong>{selectedMedia.file.name}</strong>
                        </div>
                    )}
                    {selectedMedia.type === 'audio' && (
                        <audio controls src={selectedMedia.preview}></audio>
                    )}
                    <button className={styles.removeImageBtn} onClick={removeMedia}>×</button>
                </div>
            )}

            <div className={styles.textareaWrapper}>
                <textarea
                    ref={textAreaRef}
                    className={styles.chatInput}
                    placeholder="Upload a bird sound or ask — Bird Assistant helps you ID the species and learn more."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit();
                        }
                    }}
                    rows={1}
                />
                <button
                    className={`${styles.submitButton} ${message.trim() || selectedMedia ? styles.active : ''}`}
                    onClick={handleSubmit}
                    disabled={!message.trim() && !selectedMedia}
                >
                    <Send />
                </button>
            </div>

            <div className={styles.inputControls}>
                <div className={styles.leftControls}>
                    <input
                        type="file"
                        ref={fileInputRef}
                        className={styles.hiddenFileInput}
                        accept="audio/*"
                        onChange={handleFileChange}
                    />
                    <IconButton aria-label="upload-audio" className={styles.iconButton} onClick={() => fileInputRef.current?.click()}>
                        <LibraryMusicOutlined style={{ color: 'white', fontSize: '1.8rem' }} />
                    </IconButton>
                </div>
                <div className={styles.rightControls}>
                    <span className={styles.inputTip}>Use shift + return for new line</span>
                    <select
                        className={styles.modelSelect}
                        value={selectedModel}
                        onChange={handleModelChange}
                        disabled={disableModelSelect}
                    >
                        <option value="llm-cnn">Powered by an Agent-based LLM and an Acoustic CNN model</option>
                    </select>
                </div>
            </div>
        </div>
    );
}
