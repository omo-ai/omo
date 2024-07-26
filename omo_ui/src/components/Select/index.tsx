import { Listbox, Transition } from "@headlessui/react";
import { twMerge } from "tailwind-merge";
import Icon from "@/components/Icon";

type SelectProps = {
    label?: string;
    title?: string;
    icon?: string;
    className?: string;
    classButton?: string;
    classArrow?: string;
    classOptions?: string;
    classOption?: string;
    classIcon?: string;
    placeholder?: string;
    items: any;
    value: any;
    onChange: any;
    small?: boolean;
    up?: boolean;
};

const Select = ({
    label,
    title,
    icon,
    className,
    classButton,
    classArrow,
    classOptions,
    classOption,
    classIcon,
    placeholder,
    items,
    value,
    onChange,
    small,
    up,
}: SelectProps) => (
    <div className={`relative ${className}`}>
        {label && <div className="flex mb-2 base2 font-semibold">{label}</div>}
        <Listbox value={value} onChange={onChange}>
            {({ open }) => (
                <>
                    <Listbox.Button
                        className={twMerge(
                            `flex items-center w-full h-[3.25rem] px-4 rounded-xl bg-n-1 base2 outline-none tap-highlight-color ${
                                small
                                    ? `h-9 pr-3 rounded-md shadow-[0_0.125rem_0.25rem_rgba(0,0,0,0.15)] dark:shadow-[0_0.125rem_0.25rem_rgba(0,0,0,0.15),inset_0_0_0_0.0625rem_rgba(254,254,254,.1)] dark:bg-n-6 ${
                                          open &&
                                          "shadow-[0_0.125rem_0.25rem_rgba(0,0,0,0.15)]"
                                      }`
                                    : `shadow-[inset_0_0_0_0.0625rem_#E8ECEF] dark:shadow-[inset_0_0_0_0.0625rem_#343839] dark:bg-transparent ${
                                          open &&
                                          "!shadow-[inset_0_0_0_0.125rem_#0084FF]"
                                      }`
                            } ${classButton}`
                        )}
                    >
                        {title && (
                            <div className="shrink-0 mr-2 pr-2 border-r border-n-3 text-n-4 dark:border-n-4/50">
                                {title}
                            </div>
                        )}
                        {icon && (
                            <Icon
                                className={`shrink-0 mr-2 dark:fill-n-4 ${
                                    small && "w-5 h-5 mr-1.5"
                                } ${classIcon}`}
                                name={icon}
                            />
                        )}
                        {value?.color && (
                            <div
                                className="shrink-0 w-3.5 h-3.5 ml-1 mr-4 rounded"
                                style={{ backgroundColor: value.color }}
                            ></div>
                        )}
                        {value?.icon && (
                            <Icon
                                className="w-5 h-5 mr-3 dark:fill-n-1"
                                name={value.icon}
                            />
                        )}
                        <span
                            className={`mr-auto truncate ${
                                small && "font-semibold"
                            }`}
                        >
                            {value ? (
                                value.title
                            ) : (
                                <span className="text-n-4">{placeholder}</span>
                            )}
                        </span>
                        <Icon
                            className={`shrink-0 ml-2 transition-transform dark:fill-n-1 ${
                                open && "rotate-180"
                            } ${small && "ml-1"} ${classArrow}`}
                            name="arrow-down"
                        />
                    </Listbox.Button>
                    <Transition
                        leave="transition ease-in duration-100"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <Listbox.Options
                            className={twMerge(
                                `absolute left-0 right-0 w-full mt-2 p-2 bg-n-1 rounded-lg shadow-[0_0_1rem_0.25rem_rgba(0,0,0,0.04),0_2rem_2rem_-1.5rem_rgba(0,0,0,0.1),inset_0_0_0_0.0625rem_#E8ECEF] outline-none dark:shadow-[0_0_1rem_0.25rem_rgba(0,0,0,0.04),0_2rem_2rem_-1.5rem_rgba(0,0,0,0.1),inset_0_0_0_0.0625rem_#343839] dark:bg-n-6 ${
                                    small && "right-auto mt-1 shadow-md"
                                } ${
                                    up &&
                                    `top-auto bottom-full mt-0 ${
                                        small ? "mb-1" : "mb-2"
                                    }`
                                } ${open && "z-10"} ${classOptions}`
                            )}
                        >
                            {items.map((item: any) => (
                                <Listbox.Option
                                    className={`flex items-start p-2 rounded-lg base2 text-n-4 transition-colors cursor-pointer hover:text-n-7 ui-selected:!bg-n-3/50 ui-selected:!text-n-7 tap-highlight-color dark:hover:text-n-3 dark:ui-selected:!bg-n-7 dark:ui-selected:!text-n-1 ${
                                        small && "py-1 font-semibold"
                                    } ${classOption}`}
                                    key={item.id}
                                    value={item}
                                >
                                    {item.color && (
                                        <div
                                            className="shrink-0 w-3.5 h-3.5 mt-[0.3125rem] ml-1 mr-4 rounded"
                                            style={{
                                                backgroundColor: item.color,
                                            }}
                                        ></div>
                                    )}
                                    {item.icon && (
                                        <Icon
                                            className="w-5 h-5 mt-0.5 mr-3 dark:fill-n-1"
                                            name={item.icon}
                                        />
                                    )}
                                    <div className="mr-auto">{item.title}</div>
                                    {!small && (
                                        <Icon
                                            className="hidden w-5 h-5 ml-2 mt-0.5 fill-n-7 ui-selected:inline-block dark:fill-n-1"
                                            name="check-thin"
                                        />
                                    )}
                                </Listbox.Option>
                            ))}
                        </Listbox.Options>
                    </Transition>
                </>
            )}
        </Listbox>
    </div>
);

export default Select;
