import Image from "@/components/Image";
import Icon from "@/components/Icon";

type ViewProps = {};

const View = ({}: ViewProps) => (
    <div className="relative max-w-[32.5rem] aspect-[1.6] xl:max-w-full">
        <Image
            className="rounded-xl object-cover"
            src="/images/video-pic-1.jpg"
            fill
            sizes="(max-width: 768px) 100vw, (max-width: 1499px) 50vw, 33.33vw"
            alt=""
        />
        <button className="absolute top-1/2 left-1/2 w-12 h-12 pl-0.5 -translate-x-1/2 -translate-y-1/2 rounded-full bg-n-1/90 transition-colors hover:bg-n-1 md:w-10 md:h-10">
            <Icon className="w-4 h-4" name="play" />
        </button>
    </div>
);

export default View;
