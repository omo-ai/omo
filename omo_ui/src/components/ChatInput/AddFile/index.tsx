import { useState, useContext } from "react";
import Icon from "@/components/Icon";
import { nanoid } from "nanoid";
import { ChatContext } from "@/contexts/ChatContext";
import { useRouter } from "next/navigation";


type AddFileProps = {};

const AddFile = ({}: AddFileProps) => {
    const { setChatId, startNewChat } = useContext(ChatContext);
    const router = useRouter();
    return (
        <>
        <div className="group z-10">
            <button
                className="group absolute left-3 bottom-2 w-10 h-10 outline-none"
                onClick={() => { startNewChat(); router.push("/")}}
            >
                <Icon
                    className="w-7 h-7 fill-[#7F8689] transition-colors group-hover:fill-primary-1 dark:fill-n-4"
                    name="plus-circle"
                />
            </button>
            <span className="absolute scale-0 bottom-13 -left-7 transition delay-700 duration-100 rounded-lg all bg-black py-2 px-4 text-sm text-white group-hover:scale-100">Start new chat</span>
            </div>
        </>
    );
};

export default AddFile;
