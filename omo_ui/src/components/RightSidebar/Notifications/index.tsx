import { useState } from "react";
import { Menu, Transition } from "@headlessui/react";
import Icon from "@/components/Icon";
import Modal from "@/components/Modal";
import Settings from "@/components/Settings";
import Notification from "./Notification";

import { settings } from "@/constants/settings";

type NotificationsType = {
    id: string;
    avatar: string;
    content: any;
    time: string;
    category: string;
    online?: boolean;
    new?: boolean;
    url: string;
};

type NotificationsProps = {
    items: NotificationsType[];
};

const Notifications = ({ items }: NotificationsProps) => {
    const [visibleSettings, setVisibleSettings] = useState<boolean>(false);

    const handleClick = (close: any) => {
        setVisibleSettings(true);
        close();
    };

    return (
        <>
            <div className="relative z-10 mr-8 lg:mr-6">
                <Menu>
                    {({ close }) => (
                        <>
                            <Menu.Button className="group relative w-10 h-10">
                                <Icon
                                    className="fill-n-4 transition-colors group-hover:fill-primary-1 ui-open:fill-primary-1"
                                    name="notification"
                                />
                                <div className="absolute top-2.5 right-2.5 w-2 h-2 rounded-full bg-accent-1"></div>
                            </Menu.Button>
                            <Transition
                                enter="transition duration-100 ease-out"
                                enterFrom="transform scale-95 opacity-0"
                                enterTo="transform scale-100 opacity-100"
                                leave="transition duration-75 ease-out"
                                leaveFrom="transform scale-100 opacity-100"
                                leaveTo="transform scale-95 opacity-0"
                            >
                                <Menu.Items className="absolute top-full -right-2.5 w-[30.75rem] p-6 bg-n-1 rounded-[1.25rem] shadow-[0_0_1rem_0.25rem_rgba(0,0,0,0.04),0px_2rem_2rem_-1rem_rgba(0,0,0,0.1)] lg:mt-2 lg:-right-32 md:-right-56 md:w-[calc(100vw-2rem)] md:p-4 dark:bg-n-7 dark:border dark:border-n-5">
                                    <div className="flex justify-between items-center mb-3">
                                        <div className="h4 md:h5">
                                            Notifications
                                        </div>
                                        <button
                                            className="group"
                                            onClick={() => handleClick(close)}
                                        >
                                            <Icon
                                                className="fill-n-4 transition-colors group-hover:fill-primary-1"
                                                name="settings"
                                            />
                                        </button>
                                    </div>
                                    <div className="max-h-[31.75rem] -mx-6 px-6 space-y-3 overflow-y-auto scroll-smooth scrollbar-none md:max-h-[21.25rem] md:space-y-6">
                                        {items.map((notification) => (
                                            <Menu.Item
                                                key={notification.id}
                                                as="div"
                                            >
                                                <Notification
                                                    item={notification}
                                                />
                                            </Menu.Item>
                                        ))}
                                    </div>
                                </Menu.Items>
                            </Transition>
                        </>
                    )}
                </Menu>
            </div>
            <Modal
                className="md:!p-0"
                classWrap="max-w-[48rem] md:min-h-screen-ios md:rounded-none"
                classButtonClose="hidden md:block md:absolute md:top-5 md:right-5 dark:fill-n-4"
                classOverlay="md:bg-n-1"
                visible={visibleSettings}
                onClose={() => setVisibleSettings(false)}
            >
                <Settings items={settings} activeItem={2} />
            </Modal>
        </>
    );
};

export default Notifications;
