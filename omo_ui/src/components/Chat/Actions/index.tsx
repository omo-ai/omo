import { useState } from "react";
import { Menu, Transition } from "@headlessui/react";
import Icon from "@/components/Icon";
import ModalShareChat from "@/components/ModalShareChat";

type ActionsProps = {};

const Actions = ({}: ActionsProps) => {
    const [favorite, setFavorite] = useState<boolean>(false);
    const [visibleModal, setVisibleModal] = useState<boolean>(false);

    const menu = [
        {
            id: "0",
            title: "Add to favorite list",
            icon: "star",
            onClick: () => setFavorite(!favorite),
        },
        {
            id: "1",
            title: "Share",
            icon: "share",
            onClick: () => setVisibleModal(true),
        },
        {
            id: "2",
            title: "Duplicate chat",
            icon: "duplicate",
            onClick: () => console.log("Duplicate chat"),
        },
        {
            id: "3",
            title: "Delete chat",
            icon: "delete-chat",
            onClick: () => console.log("Delete chat"),
        },
    ];

    return (
        <>
            <div className="relative z-10 ml-6 md:ml-4">
                <Menu>
                    <Menu.Button className="group relative w-8 h-8">
                        <Icon
                            className="fill-n-4 transition-colors group-hover:fill-primary-1 ui-open:!fill-primary-1"
                            name="dots"
                        />
                    </Menu.Button>
                    <Transition
                        enter="transition duration-100 ease-out"
                        enterFrom="transform scale-95 opacity-0"
                        enterTo="transform scale-100 opacity-100"
                        leave="transition duration-75 ease-out"
                        leaveFrom="transform scale-100 opacity-100"
                        leaveTo="transform scale-95 opacity-0"
                    >
                        <Menu.Items className="absolute top-full -left-2 w-[13.75rem] mt-1 p-3 bg-n-1 rounded-[1.25rem] shadow-[0_0_1rem_0.25rem_rgba(0,0,0,0.04),0_2rem_2rem_-1rem_rgba(0,0,0,0.1)] outline-none lg:left-auto lg:-right-6 dark:bg-n-7 dark:border dark:border-n-5">
                            <div className="space-y-2">
                                {menu.map((item, index) => (
                                    <Menu.Item key={index}>
                                        <button
                                            className="group flex items-center w-full h-12 px-3 rounded-lg base1 font-semibold transition-colors text-n-4 hover:bg-n-2 hover:text-n-7 dark:hover:bg-n-6 dark:hover:text-n-1"
                                            onClick={item.onClick}
                                        >
                                            <Icon
                                                className={`shrink-0 mr-3 fill-n-4 transition-colors group-hover:fill-n-7 dark:group-hover:fill-n-1 ${
                                                    item.id === "0" &&
                                                    favorite &&
                                                    "!fill-accent-5"
                                                }`}
                                                name={
                                                    item.id === "0"
                                                        ? favorite
                                                            ? "star-fill"
                                                            : item.icon
                                                        : item.icon
                                                }
                                            />
                                            {item.title}
                                        </button>
                                    </Menu.Item>
                                ))}
                            </div>
                        </Menu.Items>
                    </Transition>
                </Menu>
            </div>
            <ModalShareChat
                visible={visibleModal}
                onClose={() => setVisibleModal(false)}
            />
        </>
    );
};

export default Actions;
