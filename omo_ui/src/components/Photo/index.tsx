import Image from "@/components/Image";
import Actions from "@/components/Actions";
import Icon from "@/components/Icon";
import Export from "@/components/Export";
import Adjust from "@/components/Adjust";

type PhotoProps = {
    content: string;
    image: string;
    colorPicker?: boolean;
};

const Photo = ({ content, image, colorPicker }: PhotoProps) => (
    <div className="">
        <div>{content}</div>
        <div className="relative max-w-[34.75rem] h-[23.75rem] mt-5 xl:max-w-full">
            <Image
                className="rounded-xl object-cover"
                src={image}
                fill
                sizes="(max-width: 768px) 100vw, (max-width: 1499px) 50vw, 33.33vw"
                alt=""
            />
            {colorPicker && (
                <button className="absolute top-4 right-4 z-1 flex justify-center items-center w-9 h-9 bg-n-1 rounded-lg shadow-[0_0.3125rem_0.75rem_-0.25rem_#C3CAD2]">
                    <div
                        className="w-5 h-5 rounded"
                        style={{ backgroundColor: "#4667BC" }}
                    ></div>
                </button>
            )}
        </div>
        <div className="flex flex-wrap mt-1 2xl:-mx-2">
            <Actions
                className="mr-4 mt-4 2xl:w-[calc(50%-1rem)] 2xl:mx-2"
                classButton="btn-dark 2xl:w-full"
                classTitle="pl-3"
                title="Exporting 1 photo"
                buttonInner={
                    <>
                        <span>Export</span>
                        <Icon name="share" />
                    </>
                }
            >
                <Export typeImage />
            </Actions>
            <button className="btn-white btn-small mr-4 mt-4 2xl:w-[calc(50%-1rem)] 2xl:mx-2 md:capitalize">
                <span>
                    <span className="md:hidden">Create</span> variation
                </span>
                <Icon name="plus-circle-stroke" />
            </button>
            <Actions
                className="mr-4 mt-4 2xl:w-[calc(50%-1rem)] 2xl:mx-2"
                classButton="btn-white ui-open:bg-n-4/50 2xl:w-full dark:ui-open:bg-n-1/20"
                title="Adjust"
                buttonInner={
                    <>
                        <span>Adjust</span>
                        <Icon name="share" />
                    </>
                }
            >
                <Adjust image={image} />
            </Actions>
            <button className="btn-white btn-small mt-4 2xl:w-[calc(50%-1rem)] 2xl:mx-2">
                <span>Enhance</span>
                <Icon name="scale" />
            </button>
        </div>
    </div>
);

export default Photo;
