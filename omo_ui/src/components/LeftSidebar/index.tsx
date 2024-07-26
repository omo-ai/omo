import { useState, useEffect, useContext } from "react";
import { disablePageScroll, enablePageScroll } from "scroll-lock";
import Logo from "@/components/Logo";
import Icon from "@/components/Icon";
import Modal from "@/components/Modal";
import Search from "@/components/Search";
import Settings from "@/components/Settings";
import Navigation from "./Navigation";
import ChatHistory from "./ChatHistory";
import Profile from "./Profile";
import ToggleTheme from "./ToggleTheme";

import { chatList } from "@/mocks/chatList";
import { resultSearch } from "@/mocks/resultSearch";
import { settings } from "@/constants/settings";
import { twMerge } from "tailwind-merge";
import { ChatContext } from "@/contexts/ChatContext";
import { useRouter } from "next/navigation";

type LeftSidebarProps = {
    value: boolean;
    setValue?: any;
    smallSidebar?: boolean;
    visibleRightSidebar?: boolean;
};

const LeftSidebar = ({
    value,
    setValue,
    smallSidebar,
    visibleRightSidebar,
}: LeftSidebarProps) => {
    const [visibleSearch, setVisibleSearch] = useState<boolean>(false);
    const [visibleSettings, setVisibleSettings] = useState<boolean>(false);
    const { startNewChat } = useContext(ChatContext);
    const router = useRouter();

    useEffect(() => {
        window.addEventListener("keydown", handleWindowKeyDown);
        return () => {
            window.removeEventListener("keydown", handleWindowKeyDown);
        };
    }, []);

    const handleWindowKeyDown = (event: any) => {
        if (event.metaKey && event.key === "k") {
            event.preventDefault();
            startNewChat();
            router.push("/")
            // event.preventDefault();
            // setVisibleSearch(true);
        }
    };

    const navigation = [
        {
            title: "Chat",
            icon: "chat",
            color: "fill-accent-7",
            onClick: () => { startNewChat(); router.push('/')},
        },
        {
            title: "Connectors",
            icon: "dataflow",
            color: "fill-accent-7",
            onClick: () => { router.push("/connectors") }
        },
        {
            title: "Settings",
            icon: "settings",
            color: "fill-accent-7",
            onClick: () => setVisibleSettings(true),
        },
    ];

    const handleClick = () => {
        setValue(!value);
        smallSidebar && value ? disablePageScroll() : enablePageScroll();
    };

    return (
        <>
            <div
                className={twMerge(
                    `fixed z-20 top-0 left-0 bottom-0 flex flex-col pt-30 px-4 bg-n-7 md:invisible md:opacity-0 md:transition-opacity ${
                        value
                            ? "w-24 md:w-16 md:px-0 md:pb-30"
                            : "w-80"
                    } ${visibleRightSidebar && "md:visible md:opacity-100"}`
                )}
            >
                <div
                    className={`absolute top-0 right-0 left-0 flex items-center h-30 pl-7 pr-6 ${
                        value ? "justify-center md:px-4" : "justify-between"
                    }`}
                >
                    {!value && <Logo />}
                    <button
                        className="group tap-highlight-color"
                        onClick={handleClick}
                    >
                        <Icon
                            className="fill-n-4 transition-colors group-hover:fill-n-3"
                            name={value ? "toggle-on" : "toggle-off"}
                        />
                    </button>
                </div>
                <div className="grow overflow-y-auto scroll-smooth scrollbar-none">
                    <Navigation visible={value} items={navigation} />
                    <div
                        className={`my-4 h-0.25 bg-n-6 ${
                            value ? "-mx-4 md:mx-0" : "-mx-2 md:mx-0"
                        }`}
                    ></div>
                    <ChatHistory visible={value} />
                </div>
                <div className="absolute left-0 bottom-0 right-0 pb-6 px-4 bg-n-7 before:absolute before:left-0 before:right-0 before:bottom-full before:h-10 before:bg-gradient-to-t before:from-[#131617] before:to-[rgba(19,22,23,0)] before:pointer-events-none md:px-3">
                    {/* <Profile visible={value} /> */}
                    <ToggleTheme visible={value} />
                </div>
            </div>
            <Modal
                className="md:!p-0"
                classWrap="md:min-h-screen-ios md:rounded-none dark:shadow-[inset_0_0_0_0.0625rem_#232627,0_2rem_4rem_-1rem_rgba(0,0,0,0.33)] dark:md:shadow-none"
                classButtonClose="hidden md:flex md:absolute md:top-6 md:left-6 dark:fill-n-1"
                classOverlay="md:bg-n-1"
                visible={visibleSearch}
                onClose={() => setVisibleSearch(false)}
            >
                <Search items={resultSearch} />
            </Modal>
            <Modal
                className="md:!p-0"
                classWrap="max-w-[48rem] md:min-h-screen-ios md:rounded-none"
                classButtonClose="hidden md:block md:absolute md:top-5 md:right-5 dark:fill-n-4"
                classOverlay="md:bg-n-1"
                visible={visibleSettings}
                onClose={() => setVisibleSettings(false)}
            >
                <Settings items={settings} />
            </Modal>
        </>
    );
};

export default LeftSidebar;
