import { createContext, useState, useEffect } from "react"
import { buildApiUrl } from "@/utils/api";
import useChatHistory  from '@/hooks/useChatHistory';
import { Chat, ChatMessage } from "@/components/ChatInput/classes";
import { Dispatch, SetStateAction } from 'react';
import { Puritan } from "next/font/google";

type ChatHistoryContextType = {
    chatHistory: Chat[],
    setChatHistory: Dispatch<SetStateAction<Chat[]>>,
    fetchChatHistory: any,
}

const defaultChatHistoryContext = {
    chatHistory: [],
    setChatHistory: Object,
    fetchChatHistory: Object,
}

export const ChatHistoryContext = createContext<ChatHistoryContextType>(defaultChatHistoryContext);

export const ChatHistoryProvider = ({ children }: any) => {
    const { chatHistory, setChatHistory } = useChatHistory();

    async function fetchChatHistory() {
        fetch(buildApiUrl('/v1/chats/'), {
            'method': 'GET',
            'headers': {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }).then((response) => {
            return response.json();
        }).then((data) => {
            setChatHistory(data);
        })
    }




    return (
        <ChatHistoryContext.Provider value={{ 
            chatHistory,
            setChatHistory,
            fetchChatHistory,
        }}>
            { children }
        </ChatHistoryContext.Provider>
    )
}
