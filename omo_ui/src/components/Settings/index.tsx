import { useState } from "react";
import { useMediaQuery } from "react-responsive";
import Select from "@/components/Select";
import Menu from "./Menu";
import EditProfile from "./EditProfile";
import Password from "./Password";
import Notifications from "./Notifications";
import ChatExport from "./ChatExport";
import Sessions from "./Sessions";
import Connectors from "./Connectors";
import Team from "./Team";
import Appearance from "./Appearance";
import DeleteAccount from "./DeleteAccount";

type SettingsType = {
    id: string;
    title: string;
    icon: string;
};

type SettingsProps = {
    items: SettingsType[];
    activeItem?: number;
};

const Settings = ({ items, activeItem }: SettingsProps) => {
    const [active, setActive] = useState<any>(items[activeItem || 0]);

    const isMobile = useMediaQuery({
        query: "(max-width: 767px)",
    });

    return (
        <div className="p-12 lg:px-8 md:pt-16 md:px-5 md:pb-8">
            <div className="flex md:block">
                {isMobile ? (
                    <Select
                        className="mb-6"
                        classButton="dark:bg-transparent"
                        classArrow="dark:fill-n-4"
                        items={items}
                        value={active}
                        onChange={setActive}
                    />
                ) : (
                    <div className="shrink-0 w-[13.25rem]">
                        <Menu
                            value={active}
                            setValue={setActive}
                            buttons={items}
                        />
                    </div>
                )}
                <div className="grow pl-12 md:pl-0">
                    {active.id === "edit-profile" && <EditProfile />}
                    {active.id === "password" && <Password />}
                    {active.id === "notifications" && <Notifications />}
                    {active.id === "chat-export" && <ChatExport />}
                    {active.id === "sessions" && <Sessions />}
                    {active.id === "connectors" && <Connectors />}
                    {active.id === "team" && <Team />}
                    {active.id === "appearance" && <Appearance />}
                    {active.id === "delete-account" && <DeleteAccount />}
                </div>
            </div>
        </div>
    );
};

export default Settings;
