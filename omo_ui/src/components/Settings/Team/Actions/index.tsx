import { useState } from "react";
import { Menu, Transition } from "@headlessui/react";
import Icon from "@/components/Icon";

type ActionsProps = {
    className: string;
};

const Actions = ({ className }: ActionsProps) => {
    const [open, setOpen] = useState<boolean>(false);

    const menu = [
        {
            id: "0",
            title: "Make admin",
            icon: "star",
            onClick: () => console.log("Make admin"),
        },
        {
            id: "1",
            title: "Delete member",
            icon: "trash",
            onClick: () => console.log("Delete member"),
        },
    ];

    return (
        <div className={className}>
            <Menu>
                {({ open, close }) => (
                    <div onMouseLeave={close}>
                        <Menu.Button className="group/menu relative w-6 h-8 py-1">
                            <Icon
                                className={`fill-n-4/50 rotate-90 transition-colors group-hover/menu:fill-n-7 dark:group-hover/menu:fill-n-3 ${
                                    open && "!fill-primary-1"
                                }`}
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
                            <Menu.Items className="absolute top-full -right-2 w-[13.75rem] p-3 bg-n-1 rounded-[1.25rem] shadow-[0_0_1rem_0.25rem_rgba(0,0,0,0.04),0_2rem_2rem_-1rem_rgba(0,0,0,0.1)] dark:bg-n-6">
                                <div className="space-y-1">
                                    {menu.map((item, index) => (
                                        <Menu.Item key={index}>
                                            <button
                                                className="group flex items-center w-full h-10 px-3 rounded-lg base2 font-semibold transition-colors text-n-4 hover:bg-n-2 hover:text-n-7 dark:hover:bg-n-5 dark:hover:text-n-1"
                                                onClick={item.onClick}
                                            >
                                                <Icon
                                                    className={`shrink-0 w-5 h-5 mr-3 !fill-n-4 transition-colors group-hover:fill-n-7 dark:fill-n-2`}
                                                    name={item.icon}
                                                />
                                                {item.title}
                                            </button>
                                        </Menu.Item>
                                    ))}
                                </div>
                            </Menu.Items>
                        </Transition>
                    </div>
                )}
            </Menu>
        </div>
    );
};

export default Actions;
