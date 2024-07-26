import { useState, useEffect } from "react";
import MediaQuery from "react-responsive";

type BurgerProps = {
    className?: string;
    onClick: () => void;
    visibleRightSidebar: boolean;
};

const Burger = ({ className, onClick, visibleRightSidebar }: BurgerProps) => {
    const [mounted, setMounted] = useState<boolean>(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    return mounted ? (
        <MediaQuery maxWidth={1023}>
            <button
                className={`relative z-[25] shrink-0 flex flex-col items-center justify-center w-8 h-8 my-5 ml-auto mr-6 tap-highlight-color md:absolute md:top-5 md:right-4 md:m-0 ${
                    visibleRightSidebar && "md:!fixed"
                } ${className}`}
                onClick={onClick}
            >
                <span
                    className={`w-5 h-0.5 my-0.5 bg-n-7 rounded-full transition-all dark:bg-n-4 ${
                        visibleRightSidebar && "translate-y-0.75 rotate-45"
                    }`}
                ></span>
                <span
                    className={`w-5 h-0.5 my-0.5 bg-n-7 rounded-full transition-all dark:bg-n-4 ${
                        visibleRightSidebar && "-translate-y-0.75 -rotate-45"
                    }`}
                ></span>
            </button>
        </MediaQuery>
    ) : null;
};

export default Burger;
