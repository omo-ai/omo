import { useState } from "react";
import Switch from "@/components/Switch";
import Icon from "@/components/Icon";
import Select from "@/components/Select";

const typesFile = [
    {
        id: "0",
        title: "PDF",
    },
    {
        id: "1",
        title: "DOC",
    },
    {
        id: "2",
        title: "JPG",
    },
];

type ChatExportProps = {};

const ChatExport = ({}: ChatExportProps) => {
    const [exportChat, setExportChat] = useState<boolean>(false);
    const [typeFile, setTypeFile] = useState<any>(typesFile[0]);

    const [checkboxes, setCheckboxes] = useState([
        { id: "0", title: "UI8 Production", color: "#3E90F0", isChecked: true },
        { id: "1", title: "Favourite", color: "#8E55EA", isChecked: true },
        { id: "2", title: "Archived", color: "#8C6584", isChecked: false },
        { id: "3", title: "Deleted", color: "#D84C10", isChecked: false },
    ]);

    const handleCheckboxChange = (checkboxId: string) => {
        const updatedCheckboxes = [...checkboxes];
        const checkboxIndex = updatedCheckboxes.findIndex(
            (checkbox) => checkbox.id === checkboxId
        );
        updatedCheckboxes[checkboxIndex].isChecked =
            !updatedCheckboxes[checkboxIndex].isChecked;
        setCheckboxes(updatedCheckboxes);
    };

    const handleNotificationsChange = (value: boolean) => {
        setExportChat(value);
        const updatedCheckboxes = [...checkboxes];
        for (let checkbox of checkboxes) {
            checkbox.isChecked = value;
        }
        setCheckboxes(updatedCheckboxes);
    };

    return (
        <form className="" action="" onSubmit={() => console.log("Submit")}>
            <div className="mb-8 h4">Chat export</div>
            <div className="flex items-center mb-8">
                <div className="mr-auto base2 text-n-4">
                    Select chat list to export
                </div>
                <Switch
                    value={exportChat}
                    setValue={handleNotificationsChange}
                />
            </div>
            <div className="mb-6">
                {checkboxes.map((checkbox) => (
                    <label
                        className={`flex items-center h-14 mb-2 p-4 rounded-xl base2 font-semibold text-n-4 transition-colors hover:bg-n-2 cursor-pointer last:mb-0 dark:hover:bg-n-6 ${
                            checkbox.isChecked &&
                            "!bg-primary-1/5 text-n-6 dark:text-n-3"
                        }`}
                        key={checkbox.id}
                    >
                        <input
                            className="absolute top-0 left-0 opacity-0 invisible"
                            type="checkbox"
                            checked={checkbox.isChecked}
                            onChange={() => handleCheckboxChange(checkbox.id)}
                        />
                        <div className="flex justify-center items-center shrink-0 w-6 h-6 mr-3">
                            <div
                                className="w-3 h-3 rounded"
                                style={{ backgroundColor: checkbox.color }}
                            ></div>
                        </div>
                        {checkbox.title}
                        <Icon
                            className={`ml-auto fill-primary-1 opacity-0 transition-opacity ${
                                checkbox.isChecked && "opacity-100"
                            }`}
                            name="check-thin"
                        />
                    </label>
                ))}
            </div>
            <div className="inline-flex bg-primary-1 rounded-xl md:w-full">
                <button className="btn-blue pr-4 rounded-r-none md:grow">
                    Download conversation
                </button>
                <div className=" self-center w-0.25 h-8 bg-n-1/20"></div>
                <Select
                    classButton="h-12 rounded-l-none rounded-r-xl shadow-[inset_0_0_0_0.0625rem_#0084FF] bg-transparent text-n-1 font-semibold dark:bg-transparent"
                    classArrow="fill-n-1"
                    classOptions="min-w-full"
                    items={typesFile}
                    value={typeFile}
                    onChange={setTypeFile}
                    up
                />
            </div>
        </form>
    );
};

export default ChatExport;
