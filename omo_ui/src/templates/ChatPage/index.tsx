import { useContext, useState, useRef, useEffect } from "react";
import { ChatContext } from "@/contexts/ChatContext";
import Chat from "@/components/Chat";
import ChatInput from "@/components/ChatInput";
import { buildApiUrl } from "@/utils/api";

type ChatPageProps = {
    chatId: string | string[] | undefined
}
const ChatPage = ({ chatId }: ChatPageProps) => {
    const {
        message,
        setMessage,
        setChatMessages,
    } = useContext(ChatContext)



    useEffect(() => {
        // autoscroll when answer is rendered
        if (chatId) {
            fetch(buildApiUrl('/v1/chats/' + chatId), {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }        
            }).then(
                response => response.json()
            ).then(data => {
                if(data.messages) {
                    setChatMessages(data.messages)
                }
            })
        }

        // if(newChatMessages.length > 0) {
        //     putChatMessages();
        // }

        console.log('endofmesage')
      }, [chatId]);

   
    return (
        <>
            <div className="grow overflow-y-auto scroll-smooth scrollbar-none p-10 2xl:py-12 md:px-4 md:pt-0 md:pb-6 mb-10">
                <Chat />
            </div>
            <div className="sticky bottom-0 left-0 right-0">
                <ChatInput 
                    value={message} 
                    onChange={(e: any) => setMessage(e.target.value)} /> 
            </div>
        </>
    );
};

export default ChatPage;
