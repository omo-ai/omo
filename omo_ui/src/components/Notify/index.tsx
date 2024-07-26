import Icon from "@/components/Icon";

type NotifyProps = {
    className?: string;
    iconCheck?: boolean;
    iconDelete?: boolean;
    children: React.ReactNode;
};

const Notify = ({
    className,
    iconCheck,
    iconDelete,
    children,
}: NotifyProps) => (
    <div
        className={`flex items-center p-4 rounded-2xl bg-n-7 text-n-1 md:-mb-5 ${className}`}
    >
        {iconCheck && (
            <div className="flex justify-center items-center shrink-0 w-10 h-10 rounded-full bg-primary-2">
                <Icon className="fill-n-7" name="check-thin" />
            </div>
        )}
        {iconDelete && (
            <div className="flex justify-center items-center shrink-0 w-10 h-10 rounded-full bg-accent-1">
                <Icon className="fill-n-1" name="trash" />
            </div>
        )}
        {children}
    </div>
);

export default Notify;
