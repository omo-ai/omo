import { ChangeEventHandler, KeyboardEventHandler, useContext, useEffect, useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import Icon from "@/components/Icon";
import AddFile from "./AddFile";
import Files from "./Files";
import useSWR from 'swr';
import { buildApiUrl } from '@/utils/api';
import { AuthContext } from "@/contexts/AuthContext";
import { ChatContext } from "@/contexts/ChatContext";
import { ChatHistoryContext } from "@/contexts/ChatHistoryContext";
import { ChatMessage } from "./classes";
import { getCsrfToken } from "next-auth/react";

type ChatInputProps = {
    value: any;
    onChange: ChangeEventHandler<HTMLTextAreaElement>;
    placeholder?: string;
    image?: string;
    document?: any;
};

const ChatInput = ({
    value,
    onChange,
    placeholder,
    image,
    document,
}: ChatInputProps) => {

    const { omoUser, isOmoUserLoading } = useContext(AuthContext);
    const {
        chatId,
        setMessage,
        setChatMessages,
        shouldFetchAnswer,
        setShouldFetchAnswer,
        handleMessage,
        isRendering,
        setIsRendering,
    } = useContext(ChatContext)


    const stylesButton = "group absolute right-3 bottom-2 w-10 h-10 rounded-xl";


    function handleStreamChunk(message: any) {
        if ('answer' in message) {
            let chunk = message['answer'];
            if(!chunk) {
                // server may send empty string or null
                return
            }
            setChatMessages((messages: any) => {
                const lastMessageIndex = messages.length - 1;

                // this runtime of this is too slow since we have to iterate
                // through all the tokens each time we receive a new token
                const updatedMessages = messages.map((message: ChatMessage, index: number) =>
                    index === lastMessageIndex
                    ? { ...message, content: message.content + chunk, isLoading: false}
                    : message
                ); 
                return updatedMessages;
            })
        }
        if ('sources' in message) {
            let sources = message['sources'];
            setChatMessages((messages: any) => {
                const lastMessageIndex = messages.length - 1;

                const updateSource = messages.map((message: ChatMessage, index: number) =>
                    index === lastMessageIndex
                    ? { ...message, sources: sources }
                    : message
                ); 
                return updateSource;
            })
        }
    };

    const chatEndpoint = buildApiUrl('/v1/chat/');

    const { data, error } = useSWR(
        shouldFetchAnswer && !isRendering ? [chatEndpoint, value] : null, ([url, message]) => fetcher(url, message),
        {
            // don't continuosly hit the endpoint
            // (only send the request after user presses Send button)
            shouldRetryOnError: false,
            revalidateIfStale: false,
            revalidateOnFocus: false,
            revalidateOnReconnect: false
        }
    );

    const fetcher = async (url: string,  message: string) => {
        const csrfToken = await getCsrfToken();
        const msgPayload = { 
            "chat_id": chatId,
            "content": message, 
            "role": "human" 
        }
        await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-XSRF-Token": csrfToken,
            },
            credentials: 'include',
            body: JSON.stringify(msgPayload)
        }).then((response) => {

            function closeStream() {
                setShouldFetchAnswer(false);
                setIsRendering(false);
                setMessage("");
            }

            if(response.body == null) {
                closeStream();
                return;
            }
            const reader = response.body.getReader()

            async function readStream() {
                setIsRendering(true);
                while (true) {
                    try {
                        const { done, value } = await reader.read();
                        if (done) {
                            closeStream();
                            break;
                        }
                        // Process the received chunk of data
                        const dc = new TextDecoder('utf-8')
                        const chunks = dc.decode(value).split('\n')
                        for (const chunk of chunks) {
                            if(!chunk) continue;

                            var chunk_json = JSON.parse(chunk);
                            handleStreamChunk(chunk_json);
                        }
                    }
                    catch(error) {
                        console.log('error', error);
                        closeStream();
                        break;
                    }
                }
            }
            readStream();

        })
    };

    const onEnterKeypress = (e: any) => {
        if (!e.shiftKey && e.key === 'Enter') {
            e.preventDefault();
            handleMessage(value);
          }
    }
    
    return (
        <div className="relative z-5 px-10 py-6 be 2xl:px-6 2xl:pb-5 md:px-4 md:py-4 dark:bg-n-6 bg-n-1 rounded-[1.25rem]">
            <div className="relative z-2 border-2 border-n-3 rounded-[1.25rem] dark:border-n-5">
                {(image || document) && (
                    <Files image={image} document={document} />
                )}
                <div className="relative flex items-center min-h-[3.5rem] px-16 text-0">
                    <AddFile />
                    <TextareaAutosize
                        className="w-full py-3 bg-transparent body2 text-n-7 outline-none resize-none placeholder:text-n-4/75 dark:text-n-1 dark:placeholder:text-n-4"
                        maxRows={5}
                        autoFocus
                        value={isRendering? "" : value}
                        onChange={onChange}
                        onKeyDown={onEnterKeypress}
                        placeholder={placeholder || "Ask Omo a question"}
                    />
                    { isRendering ? (
                        <button
                           className={`${stylesButton} bg-purple-400 disabled` }
                        >
                            <svg className="w-10 h-5 text-gray-300 animate-spin" viewBox="0 0 64 64" fill="none"
                                xmlns="http://www.w3.org/2000/svg" width="24" height="24">
                                <path
                                    d="M32 3C35.8083 3 39.5794 3.75011 43.0978 5.20749C46.6163 6.66488 49.8132 8.80101 52.5061 11.4939C55.199 14.1868 57.3351 17.3837 58.7925 20.9022C60.2499 24.4206 61 28.1917 61 32C61 35.8083 60.2499 39.5794 58.7925 43.0978C57.3351 46.6163 55.199 49.8132 52.5061 52.5061C49.8132 55.199 46.6163 57.3351 43.0978 58.7925C39.5794 60.2499 35.8083 61 32 61C28.1917 61 24.4206 60.2499 20.9022 58.7925C17.3837 57.3351 14.1868 55.199 11.4939 52.5061C8.801 49.8132 6.66487 46.6163 5.20749 43.0978C3.7501 39.5794 3 35.8083 3 32C3 28.1917 3.75011 24.4206 5.2075 20.9022C6.66489 17.3837 8.80101 14.1868 11.4939 11.4939C14.1868 8.80099 17.3838 6.66487 20.9022 5.20749C24.4206 3.7501 28.1917 3 32 3L32 3Z"
                                    stroke="currentColor" stroke-width="5" strokeLinecap="round" strokeLinejoin="round"></path>
                                <path
                                    d="M32 3C36.5778 3 41.0906 4.08374 45.1692 6.16256C49.2477 8.24138 52.7762 11.2562 55.466 14.9605C58.1558 18.6647 59.9304 22.9531 60.6448 27.4748C61.3591 31.9965 60.9928 36.6232 59.5759 40.9762"
                                    stroke="currentColor" stroke-width="5" strokeLinecap="round" strokeLinejoin="round" className="text-gray-900">
                                </path>
                            </svg>
                        </button>

                    ) : (
                        <button
                            className={`${stylesButton} bg-primary-1 rounded-xl transition-colors hover:bg-primary-1/90`}
                            onClick={() => handleMessage(value) }
                        >
                            <Icon className="fill-n-1" name="arrow-up" />
                        </button>
                    )}
                </div>

            </div>
        </div>
    );
};

export default ChatInput;
