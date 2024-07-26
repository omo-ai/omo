import Icon from "@/components/Icon";

type DocumentProps = {
    value?: string;
};

const Document = ({ value }: DocumentProps) => (
    <div className="w-40">
        <div className="relative flex items-end h-[11.25rem] rounded-xl bg-n-2 dark:bg-n-5">
            <button className="group absolute top-4 right-4 w-8 h-8 rounded-full bg-n-1 text-0 dark:bg-n-7">
                <Icon
                    className="w-4 h-4 fill-n-4 transition-colors group-hover:fill-primary-1"
                    name="zoom-in"
                />
            </button>
            <div className="w-full p-6">
                <div className="w-[3.75rem] h-2 mb-3 rounded-full bg-n-3 dark:bg-n-4/25"></div>
                <div className="h-2 mb-3 rounded-full bg-n-3 dark:bg-n-4/25"></div>
                <div className="h-2 rounded-full bg-n-3 dark:bg-n-4/25"></div>
            </div>
        </div>
        <div className="mt-3 base1 truncate">{value}</div>
    </div>
);

export default Document;
