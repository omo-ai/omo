import { useState } from "react";
import { toast } from "react-hot-toast";
import Link from "next/link";
import { twMerge } from "tailwind-merge";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import Users from "@/components/Users";
import Notify from "@/components/Notify";

type ChatItemProps = {
    item: any;
};

const ChatItem = ({ item }: ChatItemProps) => {
    const [active, setActive] = useState<boolean>(false);

    const handleClick = () => {
        setActive(true);
        toast((t) => (
            <Notify iconCheck>
                <div className="mr-6 ml-3 h6">1 chat archived</div>
                <button
                    className="btn-blue btn-medium ml-3"
                    onClick={() => toast.dismiss(t.id)}
                >
                    Undo
                </button>
            </Notify>
        ));
    };

    return (
        <div className="relative mt-2">
            {/* <button
                className={`absolute z-1 top-3 left-3 flex justify-center items-center border-2 border-n-4/50 w-5.5 h-5.5 rounded-md transition-colors ${
                    active && "border-primary-1 bg-primary-1"
                }`}
                onClick={handleClick}
            >
                <Icon
                    className={`w-4 h-4 fill-n-1 opacity-0 transition-opacity ${
                        active && "opacity-100"
                    }`}
                    name="check"
                />
            </button> */}
            <Link className="block" href={item.url}>
                <div
                    className={`group py-3 pl-3 pr-3 rounded-xl transition-colors hover:bg-n-3/75 dark:hover:bg-n-5 ${
                        active && "bg-n-3/75 dark:bg-n-5"
                    }`}
                >
                    <div className="base1 font-semibold dark:text-n-1">
                        {item.title}
                    </div>
                    <div className="mt-1 truncate caption1 text-n-4">
                        {item.content}
                    </div>
                    {item.image && (
                        <div className="relative mt-4 mb-4 aspect-[1.5]">
                            <Image
                                className="rounded-lg object-cover"
                                src={item.image}
                                fill
                                sizes="(max-width: 768px) 100vw, (max-width: 1023px) 50vw, 20vw"
                                alt=""
                            />
                        </div>
                    )}
                    <div className="flex justify-between items-center mt-2">
                        {/* <Users
                            items={item.users}
                            borderColor={twMerge(
                                `border-n-1 transition-colors group-hover:border-n-3/75 dark:border-n-6 dark:group-hover:border-n-5 ${
                                    active && "border-n-3/75 dark:border-n-5"
                                }`
                            )}
                        /> */}
                        <div className="caption2 text-n-4/75">{item.time}</div>
                    </div>
                </div>
            </Link>
        </div>
    );
};

export default ChatItem;
