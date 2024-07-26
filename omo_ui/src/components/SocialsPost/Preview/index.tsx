import Image from "@/components/Image";
import Icon from "@/components/Icon";

type PreviewProps = {
    item: any;
};

const Preview = ({ item }: PreviewProps) => (
    <div className="relative shrink-0 w-[12.5rem] h-[9.375rem] mr-3">
        <Image
            className="rounded-xl object-cover"
            src={item.src}
            fill
            sizes="(max-width: 768px) 100vw, 33vw"
            alt=""
        />
        <button
            className="group absolute top-2 right-2 w-6 h-6 rounded-full bg-n-7 text-0"
            name="close-fat"
        >
            <Icon
                className="w-4 h-4 fill-n-4 transition-colors group-hover:fill-n-1"
                name="close-fat"
            />
        </button>
    </div>
);

export default Preview;
