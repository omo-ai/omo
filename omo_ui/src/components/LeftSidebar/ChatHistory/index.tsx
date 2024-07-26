import { useContext, useEffect, useState } from "react";
import { Disclosure, Transition } from "@headlessui/react";
import Link from "next/link";
import { twMerge } from "tailwind-merge";
import Icon from "@/components/Icon";
import { ChatContext } from "@/contexts/ChatContext";
import { ChatHistoryContext } from "@/contexts/ChatHistoryContext";

type ChatHistoryItem = {
    id: string;
    title: string;
    counter: number;
    color: string;
    url: string;
    chat_id: string;
    messages: Object;
};

type ChatHistoryProps = {
    visible?: boolean;
};

const ChatHistory = ({ visible }: ChatHistoryProps) => {
    const [visibleModal, setVisibleModal] = useState<boolean>(false);
    const { chatId } = useContext(ChatContext);
    const { chatHistory, fetchChatHistory } = useContext(ChatHistoryContext);

    useEffect(() => {
        fetchChatHistory();
    }, [])

    return (
        <>
            <div className="mb-auto pb-6">
                {!visible && 
                <>
                    <Disclosure defaultOpen={true}>
                        <Disclosure.Button
                            className={`flex items-center w-full h-12 text-left base2 text-n-4/75 transition-colors hover:text-n-3 ${
                                visible ? "justify-center px-3" : "px-5"
                            }`}
                        >

                                <Icon
                                    className="fill-n-4 transition-transform ui-open:rotate-180"
                                    name="arrow-down"
                                />
                            
                            {!visible && <div className="ml-5">Chat history</div>}
                        </Disclosure.Button>
     
                        <Transition
                            enter="transition duration-100 ease-out"
                            enterFrom="transform scale-95 opacity-0"
                            enterTo="transform scale-100 opacity-100"
                            leave="transition duration-75 ease-out"
                            leaveFrom="transform scale-100 opacity-100"
                            leaveTo="transform scale-95 opacity-0"
                        >
                            <Disclosure.Panel className={`${visible && "px-2"}`}>
                                {chatHistory.length > 0 ?
                                (
                                    chatHistory.map((item, index) => (
                                        <Link
                                            className={twMerge(
                                                `flex items-center w-full h-12 rounded-lg text-n-3/75 base2 font-semibold transition-colors hover:text-n-1 ${
                                                    visible ? "px-3" : "px-7"
                                                } ${
                                                    item.chat_id === chatId &&
                                                    "text-n-1 bg-gradient-to-l from-[#323337] to-[rgba(80,62,110,0.29)]"
                                                }`
                                            )}
                                            key={index}
                                            //onClick={() => setChatHistory([])} // clear it out so we can load new one
                                            href={"/c/" + item.chat_id}
                                        >
                                            {!visible && (
                                                <>
                                                    <div className="m-2">
                                                        {item.title}
                                                    </div>
                                                </>
                                            )}
                                        </Link>
                                    ))
                                ) : (
                                    <div className="pl-16">No history yet.</div>
                                )}
                            </Disclosure.Panel>
                        </Transition>
                    </Disclosure>
                </>
                }
            </div>
                        
        </>
    );
};

export default ChatHistory;
