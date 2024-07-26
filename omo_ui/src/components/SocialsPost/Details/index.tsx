import Icon from "@/components/Icon";
import Preview from "../Preview";

type DetailsProps = {
    images: any;
};

const Details = ({ images }: DetailsProps) => (
    <div className="mt-4 p-5 border-2 border-n-3 rounded-xl dark:border-n-5">
        <div className="flex justify-between mb-2">
            <div className="">
                <div className="caption1 font-semibold text-n-6 dark:text-n-3">
                    Suggested media
                </div>
                <div className="caption2 text-n-4/75">
                    Make sure you have the rights to use the suggested media.
                </div>
            </div>
            <button className="group shrink-0 w-6.5 h-6.5 ml-6 md:-mt-1">
                <Icon
                    className="w-5 h-5 fill-n-4 transition-colors group-hover:fill-accent-1"
                    name="close"
                />
            </button>
        </div>
        <div className="flex overflow-x-auto scrollbar-none -mx-5 before:shrink-0 before:w-5 after:shrink-0 after:w-5">
            {images.map((image: any) => (
                <Preview item={image} key={image.id} />
            ))}
            <div className="relative flex flex-col justify-center items-center shrink-0 w-[12.5rem] h-[9.375rem] bg-n-2 rounded-xl dark:bg-n-7">
                <input
                    className="absolute top-0 left-0 w-full h-full opacity-0 cursor-pointer"
                    type="file"
                />
                <Icon className="dark:fill-n-1" name="image-up" />
                <div className="mt-2 caption1 font-semibold text-n-6 dark:text-n-3">
                    Upload media
                </div>
            </div>
        </div>
    </div>
);

export default Details;
