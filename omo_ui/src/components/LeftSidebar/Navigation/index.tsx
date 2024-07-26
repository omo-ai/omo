import { useRouter } from "next/router";
import Link from "next/link";
import { twMerge } from "tailwind-merge";
import Icon from "@/components/Icon";

type NavigationType = {
    title: string;
    icon: string;
    color: string;
    url?: string;
    onClick?: () => void;
};

type NavigationProps = {
    visible?: boolean;
    items: NavigationType[];
};

const Navigation = ({ visible, items }: NavigationProps) => {
    const router = useRouter();

    return (
        <div className={`${visible && "px-2"}`}>
            {items.map((item, index) =>
             (
                    <button
                        className={`flex items-center w-full h-12 base2 font-semibold text-n-3/75 rounded-lg transition-colors hover:text-n-1 ${
                            visible ? "px-3" : "px-5"
                        }`}
                        key={index}
                        onClick={item.onClick}
                    >
                        <Icon className={item.color} name={item.icon} />
                        {!visible && <div className="ml-5">{item.title}</div>}
                        {item.title === "Chat" && !visible && (
                            <div className="ml-auto px-2 rounded-md bg-n-4/50 caption1 font-semibold text-n-3">
                                ⌘ K
                            </div>
                        )}
                    </button>
                )
            )}
        </div>
    );
};

export default Navigation;
