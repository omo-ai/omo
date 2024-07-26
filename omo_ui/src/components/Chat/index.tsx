import { useState, useContext, useRef, useEffect } from "react";
import ModalShareChat from "@/components/ModalShareChat";
import Question from "@/components/Question";
import Answer from "@/components/Answer";
import Sources from "@/components/Answer/Sources";
import AIMessage from "@/components/Answer/AIMessage";
import { ChatContext } from "@/contexts/ChatContext";
import { ChatScrollAnchor } from "../ChatScrollAnchor";

type ChatProps = {
    title?: string;
    // children: React.ReactNode;
};

const Chat = ({ title }: ChatProps) => {
    const [visibleModal, setVisibleModal] = useState<boolean>(false);
    const { chatMessages } = useContext(ChatContext)

    return (
        <>
            {chatMessages && chatMessages.map((message, index) => (
                message.role === "human" ? (
                    <Question key={index} content={message.content} />
                ) : (
                    <Answer key={index} loading={message.isLoading} content={message.content} >
                        <AIMessage content={message.content} />
                        {'sources' in message ? ( 
                            <Sources sources={message.sources} />
                        ) : <></>
                        }
                    </Answer>
                )         
            ))}
            <ChatScrollAnchor trackVisibility={true} />
            <ModalShareChat
                visible={visibleModal}
                onClose={() => setVisibleModal(false)}
            />

        </>
    );
};

export default Chat;
