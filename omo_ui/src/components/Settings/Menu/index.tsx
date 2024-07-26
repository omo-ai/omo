import { twMerge } from "tailwind-merge";
import Icon from "@/components/Icon";
import { useRouter } from 'next/navigation'
import { signOut } from "next-auth/react";

type MenuProps = {
    buttons: any;
    value: any;
    setValue: any;
};

const Menu = ({ buttons, value, setValue }: MenuProps) => {
    const router = useRouter();
    const handleClick = (value: any) => {
        setValue(value);
    };

    return buttons.map((button: any, index: number) => (
        <div className="mb-1" key={index}>
            {button.id === "logout" && (
                <div className="h-0.25 my-3 bg-n-3 dark:bg-n-6"></div>
            )}
            <button
                className={`group flex items-center w-full px-3.5 py-1.5 rounded-full border-2 border-transparent base2 font-semibold transition-colors hover:bg-n-2 tap-highlight-color dark:hover:bg-n-6 dark:hover:text-n-1 ${
                    button.id === "logout"
                        ? `!text-accent-1 ${
                              value === button &&
                              "!border-accent-1 !bg-n-1 dark:!bg-transparent"
                          }`
                        : `text-n-4 ${
                              value === button &&
                              "!border-primary-1 text-n-7 !bg-n-1 dark:!bg-transparent dark:text-n-1"
                          }`
                }`}
                onClick={button.id === "logout" ? () => { 
                    signOut({redirect: true, callbackUrl: '/'});
                } : () => handleClick(button)}
            >
                <Icon
                    className={`w-4 h-4 mr-3 transition-colors ${
                        button.id === "logout"
                            ? `!fill-accent-1`
                            : `fill-n-4 ${
                                  value === button &&
                                  "fill-n-7 dark:fill-n-1 dark:group-hover:fill-n-1"
                              }`
                    }`}
                    name={button.icon}
                />
                {button.title}
            </button>
        </div>
    ));
};

export default Menu;
