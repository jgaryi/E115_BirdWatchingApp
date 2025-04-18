'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Mic } from '@mui/icons-material';
import IconButton from '@mui/material/IconButton';

// Styles
import styles from './ChatInput.module.css';

export default function ChatInput({
    onSendMessage,
    selectedModel,
    onModelChange,
    disableModelSelect = false
}) {
    // Component States
    const [message, setMessage] = useState('');
    const [selectedAudio, setSelectedAudio] = useState(null);
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

    // Handlers
    const handleMessageChange = (e) => {
        setMessage(e.target.value);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            if (e.shiftKey) return;
            e.preventDefault();
            handleSubmit();
        }
    };

    const handleSubmit = () => {
        if (message.trim() || selectedAudio) {
            console.log('Submitting message:', message);
            const newMessage = {
                content: message.trim(),
                // Change the key from 'audio' to 'file' to match your backend expectations
                file: selectedAudio?.file || null
            };

            // Send the message
            onSendMessage(newMessage);

            // Reset
            setMessage('');
            setSelectedAudio(null);
            if (textAreaRef.current) {
                textAreaRef.current.style.height = 'auto';
            }
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    const handleAudioClick = () => {
        fileInputRef.current?.click();
    };

    const handleAudioChange = (e) => {
        const file = e.target.files?.[0];
        if (file) {
            if (file.size > 5000000) { // 5MB limit
                alert('File size should be less than 5MB');
                return;
            }
            // For audio, display the file name
            setSelectedAudio({
                file: file,
                preview: file.name
            });
        }
    };

    const handleModelChange = (event) => {
        onModelChange(event.target.value);
    };

    const removeAudio = () => {
        setSelectedAudio(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className={styles.chatInputContainer}>
            {selectedAudio && (
                <div className={styles.audioPreview}>
                    <div className={styles.audioInfo}>
                        <span>{selectedAudio.preview}</span>
                    </div>
                    <button
                        className={styles.removeAudioBtn}
                        onClick={removeAudio}
                    >
                        ×
                    </button>
                </div>
            )}
            <div className={styles.textareaWrapper}>
                <textarea
                    ref={textAreaRef}
                    className={styles.chatInput}
                    placeholder="Upload a bird sound or ask — Bird Assistant helps you ID the species and learn more."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyPress}
                    rows={1}
                />
                <button
                    className={`${styles.submitButton} ${message.trim() ? styles.active : ''}`}
                    onClick={handleSubmit}
                    disabled={!message.trim() && !selectedAudio}
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
                        onChange={handleAudioChange}
                    />
                    <IconButton
                        aria-label="microphone"
                        className={styles.iconButton}
                        onClick={handleAudioClick}
                    >
                        <Mic />
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
