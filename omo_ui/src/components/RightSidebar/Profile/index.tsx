import { useState } from "react";
import { Menu, Transition } from "@headlessui/react";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import Modal from "@/components/Modal";
import Settings from "@/components/Settings";

import { settings } from "@/constants/settings";

type ProfileProps = {};

const Profile = ({}: ProfileProps) => {
    const [visibleSettings, setVisibleSettings] = useState<boolean>(false);

    const menu = [
        {
            title: "New version available",
            icon: "arrow-down-circle",
            onClick: () => console.log("New version available"),
        },
        {
            title: "Settings",
            icon: "settings-fill",
            onClick: () => setVisibleSettings(true),
        },
        {
            title: "Log out",
            icon: "logout",
            onClick: () => console.log("Log out"),
        },
    ];

    return (
        <>
            <div className="relative z-10 mr-8 lg:mr-6 md:static">
                <Menu>
                    <Menu.Button className="group relative w-10 h-10 rounded-full transition-shadow ui-open:shadow-[0_0_0_0.25rem_#0084FF]">
                        <Image
                            className="rounded-full object-cover"
                            src="/images/avatar.jpg"
                            fill
                            alt="Avatar"
                        />
                        <div className="absolute -right-0.75 -bottom-0.75 w-4.5 h-4.5 bg-primary-2 rounded-full border-4 border-n-1 dark:border-n-6"></div>
                    </Menu.Button>
                    <Transition
                        enter="transition duration-100 ease-out"
                        enterFrom="transform scale-95 opacity-0"
                        enterTo="transform scale-100 opacity-100"
                        leave="transition duration-75 ease-out"
                        leaveFrom="transform scale-100 opacity-100"
                        leaveTo="transform scale-95 opacity-0"
                    >
                        <Menu.Items className="absolute top-full -right-5 w-[19.88rem] mt-[0.9375rem] p-4 bg-n-1 border border-n-2 rounded-2xl shadow-[0px_48px_64px_-16px_rgba(0,0,0,0.25)] md:-right-38 md:w-[calc(100vw-4rem)] dark:bg-n-7 dark:border-n-5">
                            <div className="flex items-center mb-3">
                                <div className="relative w-15 h-15">
                                    <Image
                                        className="rounded-full object-cover"
                                        src="/images/avatar.jpg"
                                        fill
                                        alt="Avatar"
                                    />
                                    <div className="absolute right-0 bottom-0 w-4.5 h-4.5 bg-primary-2 rounded-full border-4 border-n-1 dark:border-n-7"></div>
                                </div>
                                <div className="pl-4">
                                    <div className="h6">Tran Mau Tri Tam</div>
                                    <div className="caption1 text-n-4">
                                        Lead visual designer at UI8
                                    </div>
                                </div>
                            </div>
                            <div className="px-4 bg-n-2 rounded-xl dark:bg-n-6">
                                {menu.map((item, index) => (
                                    <Menu.Item key={index}>
                                        <button
                                            className="group flex items-center w-full h-12 base2 font-semibold transition-colors hover:text-primary-1"
                                            onClick={item.onClick}
                                        >
                                            <Icon
                                                className="mr-4 fill-n-4 transition-colors group-hover:fill-primary-1"
                                                name={item.icon}
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

export default Profile;
