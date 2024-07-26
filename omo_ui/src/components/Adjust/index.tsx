import Image from "@/components/Image";
import SliderRange from "@/components/SliderRange";

type AdjustProps = {
    image: string;
};

const Adjust = ({ image }: AdjustProps) => (
    <div className="">
        <div className="relative h-48">
            <Image
                className="mb-6 rounded-md object-cover"
                src={image}
                fill
                sizes="(max-width: 768px) 100vw, 25vw"
                alt=""
            />
        </div>
        <div className="mt-6">
            <SliderRange className="mb-2" title="Exposure" />
            <SliderRange className="mb-2" title="Contrast" />
            <SliderRange className="mb-2" title="Highlights" />
            <SliderRange className="mb-2" title="Shadows" />
            <SliderRange className="mb-2" title="White" />
            <SliderRange className="" title="Blacks" />
        </div>
        <div className="flex space-x-3 mt-6">
            <button className="btn-blue w-full">Auto</button>
            <button className="btn-stroke-light w-full">Reset</button>
        </div>
    </div>
);

export default Adjust;
