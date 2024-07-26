import { NextPage } from "next";
import { useRouter } from "next/router";
import PageLoading from "@/components/PageLoading";
import ChatPage from "@/templates/ChatPage";
import Layout from "@/components/Layout";
import { ChatContext } from "@/contexts/ChatContext";
import { ChatHistoryContext } from "@/contexts/ChatHistoryContext";
import { useContext, useEffect, useState } from "react";
import { ChatMessage } from "@/components/ChatInput/classes";

const ChatSession: NextPage = () => {
    const router = useRouter()
    const { chatId:routeChatId } = router.query
    const { setChatId } = useContext(ChatContext);


    useEffect(() => {
        setChatId(routeChatId as string);
    }, [routeChatId])

    return (
        <Layout hideRightSidebar>
            <ChatPage chatId={routeChatId}/>
        </Layout>
    )
}

export default ChatSession;