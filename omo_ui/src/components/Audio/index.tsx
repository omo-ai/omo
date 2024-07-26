import { useState } from "react";
import AudioPlayer from "@/components/AudioPlayer";
import Actions from "@/components/Actions";
import Export from "@/components/Export";
import Select from "@/components/Select";
import Icon from "@/components/Icon";

const languages = [
    {
        id: "0",
        title: "English (US)",
    },
    {
        id: "1",
        title: "French",
    },
    {
        id: "2",
        title: "Ukrainian",
    },
];

const speeds = [
    {
        id: "0",
        title: "Normal",
    },
    {
        id: "1",
        title: "1.25x",
    },
    {
        id: "2",
        title: "1.5x",
    },
];

const genders = [
    {
        id: "0",
        title: "Female",
    },
    {
        id: "1",
        title: "Man",
    },
];

const voices = [
    {
        id: "0",
        title: "Jenny",
    },
    {
        id: "1",
        title: "Mark",
    },
    {
        id: "2",
        title: "Jack",
    },
];

const smiles = [
    {
        id: "0",
        title: "😀 Friendly",
    },
    {
        id: "1",
        title: "😐 Neutral",
    },
    {
        id: "2",
        title: "😚 Kissing",
    },
];

type AudioProps = {};

const Audio = ({}: AudioProps) => {
    const [edit, setEdit] = useState<boolean>(false);
    const [language, setLanguage] = useState<any>(languages[0]);
    const [speed, setSpeed] = useState<any>(speeds[0]);
    const [gender, setGender] = useState<any>(genders[0]);
    const [voice, setVoice] = useState<any>(voices[0]);
    const [smile, setSmile] = useState<any>(smiles[0]);

    return (
        <div className="">
            <div className="mb-4">
                Your audio has been successfully generated. You may further
                customize it or simply download it for use.
            </div>
            <AudioPlayer edit={edit} onSave={() => setEdit(false)} />
            <div className="flex flex-wrap">
                <Actions
                    className="mr-4 mt-4 md:w-[calc(50%-0.5rem)] md:mr-2"
                    title="Exporting 1 audio"
                    classButton="btn-dark md:w-full"
                    classTitle="pl-3"
                    buttonInner={
                        <>
                            <span>Export</span>
                            <Icon name="share" />
                        </>
                    }
                >
                    <Export />
                </Actions>
                <button
                    className="btn-white btn-small mr-4 mt-4 md:w-[calc(50%-0.5rem)] md:mr-0 md:ml-2"
                    onClick={() => setEdit(true)}
                >
                    <span>Edit</span>
                    <Icon name="edit" />
                </button>
                <Select
                    className="mr-4 mt-4 md:w-full md:mr-0"
                    items={languages}
                    value={language}
                    onChange={setLanguage}
                    small
                    up
                />
                <Select
                    className="mr-4 mt-4 md:w-full md:mr-0"
                    title="Speed"
                    items={speeds}
                    value={speed}
                    onChange={setSpeed}
                    small
                    up
                />
                <div className="flex mr-4 mt-4 rounded-md shadow-[0_0.125rem_0.25rem_rgba(0,0,0,0.15)] bg-n-1 md:w-full md:mr-0 dark:bg-n-6 dark:shadow-[0_0.125rem_0.25rem_rgba(0,0,0,0.15),inset_0_0_0_0.0625rem_rgba(254,254,254,.1)]">
                    <Select
                        classButton="shadow-none bg-transparent ui-open:shadow-none dark:bg-transparent dark:shadow-none"
                        title="Voice"
                        items={genders}
                        value={gender}
                        onChange={setGender}
                        small
                        up
                    />
                    <div className="self-center w-0.25 h-6 bg-n-3 dark:bg-n-4/50"></div>
                    <Select
                        classButton="shadow-none bg-transparent ui-open:shadow-none dark:bg-transparent dark:shadow-none"
                        icon="volume"
                        className=""
                        items={voices}
                        value={voice}
                        onChange={setVoice}
                        small
                        up
                    />
                </div>
                <Select
                    className="mr-4 mt-4 md:w-full md:mr-0"
                    items={smiles}
                    value={smile}
                    onChange={setSmile}
                    small
                    up
                />
            </div>
        </div>
    );
};

export default Audio;
