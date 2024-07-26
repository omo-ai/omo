import { useState } from "react";
import { Chat } from "@/components/ChatInput/classes"
import { ChatMessage } from "@/components/ChatInput/classes"

const useChatHistory = () => {
    const [chatHistory, setChatHistory] = useState<Chat[]>([]); // messages of a single chat}

    return {
        chatHistory,
        setChatHistory,
    }
}

export default useChatHistory;