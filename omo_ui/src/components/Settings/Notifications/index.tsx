import { useState } from "react";
import Switch from "@/components/Switch";
import Checkbox from "@/components/Checkbox";

type NotificationsProps = {};

const Notifications = ({}: NotificationsProps) => {
    const [notifications, setNotifications] = useState<boolean>(true);

    const [checkboxes, setCheckboxes] = useState([
        {
            id: "0",
            title: "UI8 Platform",
            checkboxs: [
                { id: "0", title: "New notifications", isChecked: true },
                {
                    id: "1",
                    title: "Someone invite you to new chat",
                    isChecked: true,
                },
                { id: "2", title: "Mentioned", isChecked: true },
            ],
        },
        {
            id: "1",
            title: "From team",
            checkboxs: [
                { id: "0", title: "New notifications", isChecked: false },
                {
                    id: "1",
                    title: "Someone invite you to new chat",
                    isChecked: false,
                },
                { id: "2", title: "Mentioned", isChecked: true },
            ],
        },
        {
            id: "2",
            title: "From Brainwave app",
            checkboxs: [{ id: "0", title: "Mentioned", isChecked: true }],
        },
    ]);

    const handleCheckboxChange = (groupId: string, checkboxId: string) => {
        const updatedCheckboxes = [...checkboxes];
        const groupIndex = updatedCheckboxes.findIndex(
            (group) => group.id === groupId
        );
        const checkboxIndex = updatedCheckboxes[groupIndex].checkboxs.findIndex(
            (checkbox) => checkbox.id === checkboxId
        );
        updatedCheckboxes[groupIndex].checkboxs[checkboxIndex].isChecked =
            !updatedCheckboxes[groupIndex].checkboxs[checkboxIndex].isChecked;
        setCheckboxes(updatedCheckboxes);
    };

    const handleNotificationsChange = (value: boolean) => {
        setNotifications(value);
        const updatedCheckboxes = [...checkboxes];
        for (let group of updatedCheckboxes) {
            for (let checkbox of group.checkboxs) {
                checkbox.isChecked = value;
            }
        }
        setCheckboxes(updatedCheckboxes);
    };

    return (
        <form className="" action="" onSubmit={() => console.log("Submit")}>
            <div className="flex items-center mb-8">
                <div className="mr-auto h4">Notifications</div>
                <Switch
                    value={notifications}
                    setValue={handleNotificationsChange}
                />
            </div>
            <div>
                {checkboxes.map((group) => (
                    <div
                        className="mb-8 border-t border-n-3 py-6 last:mb-0 dark:border-n-6"
                        key={group.id}
                    >
                        <div className="mb-4 h6">{group.title}</div>
                        {group.checkboxs.map((checkbox) => (
                            <Checkbox
                                className="mb-4 last:mb-0"
                                label={checkbox.title}
                                key={checkbox.id}
                                value={checkbox.isChecked}
                                onChange={() =>
                                    handleCheckboxChange(group.id, checkbox.id)
                                }
                                reverse
                            />
                        ))}
                    </div>
                ))}
            </div>
        </form>
    );
};

export default Notifications;
