import Link from "next/link";
import Image from "@/components/Image";
import useChat from "@/hooks/useChat";
import { useContext } from "react";
import { ChatContext } from "@/contexts/ChatContext";

type LogoProps = {
    className?: string;
    dark?: boolean;
};

const Logo = ({ className, dark }: LogoProps) => {
    const { startNewChat } = useContext(ChatContext)
    
    return (
        <Link className={`flex w-[10.5rem] ${className}`} href="/">
            <Image
                className="w-full h-auto"
                src={dark ? "/images/OmoLogoDark.png" : "/images/OmoLogo-White.png"}
                width={100}
                height={30}
                onClick={startNewChat}
                priority
                alt="Omo"
            />
        </Link>
    );
};

export default Logo;
