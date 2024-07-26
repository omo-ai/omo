import { createContext, useContext, useState, useEffect, useMemo } from 'react';
import { Dispatch, SetStateAction } from 'react';
import { Chat, ChatMessage } from '@/components/ChatInput/classes';
import { usePathname, useRouter } from "next/navigation";
import { nanoid } from "nanoid";
import { buildApiUrl } from '@/utils/api';
import useChat from '@/hooks/useChat';
import { getCsrfToken } from "next-auth/react";

type ChatContextType = {
    chatId: string,
    setChatId: Dispatch<SetStateAction<string>>,
    message: string,
    setMessage: Dispatch<SetStateAction<string>>
    chatTitle: string,
    setChatTitle: Dispatch<SetStateAction<string>>,
    chatMessages: ChatMessage[],
    setChatMessages: Dispatch<SetStateAction<ChatMessage[]>>,
    isRendering: boolean,
    setIsRendering: Dispatch<SetStateAction<boolean>>,
    shouldFetchAnswer: boolean,
    setShouldFetchAnswer: Dispatch<SetStateAction<boolean>>,
    appendChatMessages: (messages: ChatMessage[]) => void,
    handleMessage: (message: any) => void,
    startNewChat: () => void,
    putChatMessages: () => void,
}

export const ChatContext = createContext<ChatContextType> ({
    chatId: '',
    setChatId: Object,
    message: '',
    setMessage: Object,
    chatTitle: '',
    setChatTitle: Object,
    chatMessages: [],
    setChatMessages: Object,
    isRendering: false,
    setIsRendering: Object,
    shouldFetchAnswer: false,
    setShouldFetchAnswer: Object,
    appendChatMessages: Object,
    handleMessage: Object,
    startNewChat: Object,
    putChatMessages: Object,
});

export const ChatProvider = ({ children }: any) => {

    const {
        chatId,
        setChatId,
        message,
        setMessage,
        chatTitle,
        setChatTitle,
        chatMessages,
        setChatMessages,
    } = useChat();

    const pathname = usePathname()



    const [shouldFetchAnswer, setShouldFetchAnswer] = useState(false)
    const [isRendering, setIsRendering] = useState(false);
    const router = useRouter();

    const appendChatMessages = (messages: ChatMessage[]) => {
        setChatMessages(currentMessages => {
                const updatedMessages = [...currentMessages, ...messages];
                return updatedMessages;
        })
    }

    const startNewChat = () => {
        // setChatSession((prevSession: any) => {
        //     const newSession = {
        //         ...prevSession,
        //         id: nanoid(),
        //         title: '',
        //         chatMessages: []
        //     }
        //     console.log('beginNewChat (post)', chatSession)
        //     return newSession;
        // })
        setChatId((prevId) => {
            const newId = nanoid(); // Generate a new unique ID
            return newId;
        });
        setChatTitle((prevTitle) => {
            const title = '';
            return title;
        })
        setChatMessages((prevMessages) => {
            const messages = [] as ChatMessage[];
            return messages;
        })

    };

    const handleMessage = (message: string) => {

        // add the message and placeholder message to the chat history
        const humanMessage = new ChatMessage(message, "human")
        const aiMessage = new ChatMessage("", "assistant", true);
        appendChatMessages([humanMessage, aiMessage]); 

        // triggers the call to /chat endpoint in ChatInput
        setShouldFetchAnswer(true);
        setMessage(message);

        if(pathname && !pathname.startsWith('/c')) {
            router.push(`/c/${chatId}`);
        }

    }

    async function putChatMessages() {
        const csrfToken = await getCsrfToken();
        fetch(buildApiUrl('/v1/chats/' + chatId), {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'X-XSRF-Token': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ "chat_id": chatId,
                                   "messages": chatMessages })
        })
    
    }

    return (
        <ChatContext.Provider value={{
            message,
            setMessage,
            chatTitle,
            setChatTitle,
            chatId,
            setChatId,
            isRendering,
            setIsRendering,
            shouldFetchAnswer,
            setShouldFetchAnswer,
            chatMessages,
            setChatMessages,
            appendChatMessages,
            handleMessage,
            startNewChat,
            putChatMessages,
        }}>
            { children }
        </ChatContext.Provider>
    )

}
