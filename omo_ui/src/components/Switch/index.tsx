import { Switch as SwitchReact } from "@headlessui/react";
import { twMerge } from "tailwind-merge";

type SwitchProps = {
    className?: string;
    value: boolean;
    setValue: any;
};

const Switch = ({ className, value, setValue }: SwitchProps) => (
    <div className={`inline-flex shrink-0 ${className}`}>
        <SwitchReact
            checked={value}
            onChange={setValue}
            className={`relative inline-flex w-12 h-6 cursor-pointer rounded-full border-2 border-transparent transition-colors outline-none ${
                value ? "bg-primary-1" : "bg-n-3 dark:bg-n-5"
            }`}
        >
            <span
                aria-hidden="true"
                className={twMerge(
                    `pointer-events-none inline-block w-5 h-5 rounded-full bg-n-1 transition-all dark:bg-n-7 ${
                        value ? "translate-x-6 dark:bg-n-1" : "translate-x-0"
                    }`
                )}
            />
        </SwitchReact>
    </div>
);

export default Switch;
