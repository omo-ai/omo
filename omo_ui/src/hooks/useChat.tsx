import { useState } from "react";
import { Chat, ChatMessage } from "@/components/ChatInput/classes";
import { nanoid } from "nanoid";
import { useRouter } from "next/navigation";

const useChat = () => {
    const [chatId, setChatId] = useState("");
    const [message, setMessage] = useState<string>("");     // human message
    const [chatTitle, setChatTitle] = useState<string>("");
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]); // all chats

    return {
        chatId,
        setChatId,
        message,
        setMessage,
        chatTitle,
        setChatTitle,
        chatMessages,
        setChatMessages,
    }

};
export default useChat;