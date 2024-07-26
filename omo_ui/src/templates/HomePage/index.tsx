"use client"
import { useState, useEffect, useContext } from "react";
import Layout from "@/components/Layout";
import Main from "./Main";
import { ChatContext } from "@/contexts/ChatContext";
import { nanoid } from "nanoid";



const HomePage = ({ user }: any) => {
    const { chatId, startNewChat, setChatId } = useContext(ChatContext)
    useEffect(() => {
        if(chatId === ''){
            setChatId((prev) => {
                const newId = nanoid();
                return newId;
            })
        }
    }, [chatId]);
    return (
        <Layout hideRightSidebar user={user}>
            <Main />
        </Layout>
    );
};

export default HomePage;
