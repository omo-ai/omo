import Link from "next/link";
import Icon from "@/components/Icon";
import { useContext } from "react";
import { ChatContext } from "@/contexts/ChatContext";
import { ChatMessage } from "../ChatInput/classes";
import { useRouter } from "next/router";


type StarterPromptType = {
    title: string;
    icon: string;
    color: string;
    url: string;
};

type StarterPromptsProps = {
    className?: string;
    items: StarterPromptType[];
    handleClick: any;
};

const StarterPrompts = ({ className, items, handleClick }: StarterPromptsProps) => {
    const { chatId, appendChatMessages } = useContext(ChatContext);

    return (
        <div className={className}>
            {items.map((item, index) => (
                <Link
                    className="group flex items-center mb-5 p-3.5 border border-n-3 rounded-xl h6 transition-all hover:border-transparent hover:shadow-[0_0_1rem_0.25rem_rgba(0,0,0,0.04),0px_2rem_1.5rem_-1rem_rgba(0,0,0,0.12)] last:mb-0 2xl:p-2.5 lg:p-3.5 dark:border-n-5 dark:hover:border-n-7 dark:hover:bg-n-7"
                    href={"/"}
                    key={index}
                    onClick={ (e) => { e.preventDefault(); handleClick(index) }}
                >
                    <div className="relative flex justify-center items-center w-15 h-15 mr-6">
                        {/* <div
                            className="absolute inset-0 opacity-20 rounded-xl"
                            style={{
                                backgroundColor: item.color,
                            }}
                        ></div>
                        <Icon
                            className="relative z-1"
                            fill={item.color}
                            name={item.icon}
                        /> */}
                    </div>
                    {item.title}
                    <Icon
                        className="ml-auto fill-n-4 transition-colors group-hover:fill-n-7 dark:group-hover:fill-n-4"
                        name="arrow-next"
                    />
                </Link>
            ))}
        </div>
    );
}

export default StarterPrompts;
