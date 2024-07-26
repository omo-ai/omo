import { useContext, useState, useRef, useEffect } from "react";
import ChatInput from "@/components/ChatInput";
import StarterPrompts from "@/components/StarterPrompts";
import { starterPrompts } from "@/constants/starterPrompts";
import { ChatContext } from "@/contexts/ChatContext";
import { ChatHistoryContext } from "@/contexts/ChatHistoryContext";
import { nanoid } from "nanoid";
import { ChatMessage } from "@/components/ChatInput/classes";
import { useRouter } from "next/router";
import { usePathname } from "next/navigation";

type MainProps = {
};

const Main = ({}: MainProps) => {
    const pathname = usePathname()
    const router = useRouter();

    const {
        chatId,
        message,
        setMessage,
        handleMessage,
        appendChatMessages,
    } = useContext(ChatContext);

    // const handleStarterPrompt = (prompt: string) => {
    //     handleMessage(prompt);
    // }


    const handleStarterPromptItem = (index: number) => {
        console.log('being called')
        switch(index) {
            case 0:
                appendChatMessages([
                    new ChatMessage("What is OmoAI?", "human"),
                    new ChatMessage(`Omo allows users to chat and search their data by connecting a variety of data sources, also known as Connectors. 
                    Users can use our hosted SaaS version, or deploy our platform on their own infrastructure.  Use the built in chat UI or leverage our APIs to integrate it within your own product.`, "assistant"),
                ]);
                break;
            case 1:
                appendChatMessages([
                    new ChatMessage("How do I get started?", "human"),
                    new ChatMessage("To get started, click on the Connectors link in the left sidebar and connect a data source." +
                    "If you need a specific Connector that's not listed, please email us at founders@helloomo.ai", "assistant"),
                ]);
                break;
            case 2:
                appendChatMessages([
                    new ChatMessage("How do I get support?", "human"),
                    new ChatMessage("If you need help, feel free to email us at founders@helloomo.ai! Someone should get back to you within a day.", "assistant"),
                ]);
                break;
        }

        if(pathname && !pathname.startsWith('/c')) {
            router.push(`/c/${chatId}`);
        }
    };
    const endOfMessagesRef = useRef<null | HTMLDivElement>(null);

    return (
        <>
            <div className="grow px-10 py-20 overflow-y-auto scroll-smooth scrollbar-none 2xl:py-12 md:px-4 md:pt-0 md:pb-6">
                <div className="mb-10 text-center">
                    {/* <div className="h3 leading-[4rem] 2xl:mb-2 2xl:h4">
                        Hi, Chris 👋
                    </div> */}
                    <div className="body1 text-n-4 2xl:body1S">
                        Try one of the prompts below.
                    </div>
                </div>
                <StarterPrompts 
                    className="max-w-[30.75rem] mx-auto" 
                    items={starterPrompts}
                    handleClick={handleStarterPromptItem}
                />
            </div>
                   
            <div className="sticky bottom-0 left-0 right-0">
                <ChatInput value={message} onChange={(e: any) => setMessage(e.target.value)}/> 
            </div>
            <div ref={endOfMessagesRef} /> 
        </>
    );
};

export default Main;
