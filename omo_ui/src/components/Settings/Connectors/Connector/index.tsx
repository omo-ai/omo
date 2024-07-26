import Image from "@/components/Image";

type ConnectorProps = {
    item: any;
};

const Connector = ({ item }: ConnectorProps) => (
    <div className="group flex items-center py-6 border-t border-n-3 cursor-pointer dark:border-n-6">
        <div className="w-12 shrink-0">
            <Image
                className="w-full rounded-xl"
                src={item.image}
                width={48}
                height={48}
                alt=""
            />
        </div>
        <div className="grow px-4">
            <div className="base1 font-semibold">{item.title}</div>
            <div className="caption1 text-n-4/50">{item.date}</div>
        </div>
        <button className="btn-stroke-light shrink-0 ml-4 invisible opacity-0 transition-all group-hover:visible group-hover:opacity-100 xl:visible xl:opacity-100">
            Deauthorize
        </button>
    </div>
);

export default Connector;
