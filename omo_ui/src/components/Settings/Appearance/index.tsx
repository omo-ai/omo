import { useState } from "react";
import { useColorMode } from "@chakra-ui/color-mode";
import { twMerge } from "tailwind-merge";
import Image from "@/components/Image";
import Select from "@/components/Select";

const languages = [
    {
        id: "0",
        title: "English (United States)",
    },
    // {
    //     id: "1",
    //     title: "French",
    // },
    // {
    //     id: "2",
    //     title: "Ukrainian",
    // },
];

type AppearanceProps = {};

const Appearance = ({}: AppearanceProps) => {
    const { colorMode, setColorMode } = useColorMode();
    const [language, setLanguage] = useState<any>(languages[0]);

    const items = [
        {
            title: "Light mode",
            image: "/images/theme-light.svg",
            active: colorMode === "light",
            onClick: () => setColorMode("light"),
        },
        {
            title: "Dark mode",
            image: "/images/theme-dark.svg",
            active: colorMode === "dark",
            onClick: () => setColorMode("dark"),
        },
    ];

    return (
        <>
            <div className="mb-8 h4">Appearance</div>
            <div className="mb-5 base1 font-semibold">Appearance</div>
            <div className="flex mb-8 pr-12 space-x-8 md:pr-0">
                {items.map((item, index) => (
                    <button
                        className={twMerge(
                            `basis-1/2 p-3 border-4 border-transparent bg-n-2 rounded-2xl text-left transition-colors dark:bg-n-6 dark:text-n-3/50 ${
                                item.active &&
                                "bg-transparent border-primary-1 text-n-6/50 dark:text-n-1 dark:bg-transparent"
                            }`
                        )}
                        key={index}
                        onClick={item.onClick}
                    >
                        <div className="mb-3">
                            <Image
                                className="w-full rounded-xl"
                                src={item.image}
                                width={128}
                                height={80}
                                alt=""
                            />
                        </div>
                        {item.title}
                    </button>
                ))}
            </div>
            <div className="flex items-center md:block">
                <div className="mr-auto base1 font-semibold md:mb-4">
                    Primary language
                </div>
                <Select
                    className="min-w-[13.125rem]"
                    classButton="bg-n-3/75 dark:bg-n-6 dark:shadow-[inset_0_0_0_0.0625rem_#232627]"
                    items={languages}
                    value={language}
                    onChange={setLanguage}
                    up
                />
            </div>
        </>
    );
};

export default Appearance;
