import { useState } from "react";
import Select from "@/components/Select";
import Icon from "@/components/Icon";
import View from "./View";

const languages = [
    {
        id: "0",
        title: "English (United States)",
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

type VideoProps = {};

const Video = ({}: VideoProps) => {
    const [language, setLanguage] = useState<any>(languages[0]);
    const [voice, setVoice] = useState<any>(voices[0]);

    return (
        <div className="">
            <View />
            <div className="mt-4">
                Based on the gender identified in the uploaded image, the video
                has been automatically generated with a male voice. However, you
                have the option to customize your video by selecting from the
                available options below.
            </div>
            <div className="flex flex-wrap">
                <button className="btn-dark btn-small mr-4 mt-4">
                    <span>Download</span>
                    <Icon name="download" />
                </button>
                <Select
                    className="mr-4 mt-4"
                    classOptions="min-w-[12rem]"
                    items={languages}
                    value={language}
                    onChange={setLanguage}
                    small
                    up
                />
                <Select
                    title="Voice"
                    icon="volume"
                    className="mr-4 mt-4"
                    items={voices}
                    value={voice}
                    onChange={setVoice}
                    small
                    up
                />
            </div>
        </div>
    );
};

export default Video;
