import { useColorMode } from "@chakra-ui/color-mode";
import Icon from "@/components/Icon";
import Image from "@/components/Image";

type UpdatesItems = {
    id: string;
    title: string;
    date: string;
    icon: string;
    imageLight: string;
    imageDark: string;
    content: string;
};

type UpdatesProps = {
    items: UpdatesItems[];
};

const Updates = ({ items }: UpdatesProps) => {
    const { colorMode } = useColorMode();
    const isDarkMode = colorMode === "dark";

    return (
        <>
            <div>
                {items.map((item) => (
                    <div
                        className="flex py-16 border-t border-n-3 lg:block md:py-8 dark:border-n-5"
                        key={item.id}
                    >
                        <div className="shrink-0 w-[21rem] pr-20 2xl:w-72 2xl:pr-12 lg:w-full lg:mb-10 lg:pr-0">
                            <div className="flex justify-center items-center w-15 h-15 mb-5 rounded-full bg-accent-1/20">
                                <Icon
                                    className="fill-accent-1"
                                    name={item.icon}
                                />
                            </div>
                            <div className="mb-5 h6">{item.title}</div>
                            <div className="base1 font-semibold text-n-4/50">
                                {item.date}
                            </div>
                        </div>
                        <div className="grow">
                            <div>
                                <Image
                                    className="w-full rounded-3xl md:rounded-xl"
                                    src={
                                        isDarkMode
                                            ? item.imageDark
                                            : item.imageLight
                                    }
                                    width={600}
                                    height={400}
                                    alt=""
                                />
                            </div>
                            <div className="mt-8 base1 text-n-4">
                                {item.content}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="text-center">
                <button className="btn-stroke-light">Load more</button>
            </div>
        </>
    );
};

export default Updates;
