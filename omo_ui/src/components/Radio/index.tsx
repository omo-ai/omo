type RadioProps = {
    className?: string;
    content: string;
    value: any;
    onChange: any;
    name: string;
};

const Radio = ({ className, content, value, name, onChange }: RadioProps) => (
    <label
        className={`group relative block select-none cursor-pointer tap-highlight-color ${className}`}
    >
        <input
            className="peer absolute top-0 left-0 opacity-0 invisible"
            type="checkbox"
            value={value}
            onChange={onChange}
            checked={value}
            name={name}
        />
        <span className="flex items-center base2 font-semibold text-n-4 transition-colors before:shrink-0 before:w-5 before:h-5 before:mr-3 before:rounded-full before:border-2 before:border-n-4/50 before:transition-all group-hover:before:border-primary-1 peer-checked:text-n-7 peer-checked:before:border-6 peer-checked:before:border-primary-1 dark:peer-checked:text-n-1">
            {content}
        </span>
    </label>
);

export default Radio;
