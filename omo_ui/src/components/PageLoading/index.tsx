import Image from "next/image";
import Logo from "../Logo";

const PageLoading = () => {
    return (
        <div className="animate-pulse flex items-center justify-center h-screen">
            <Image
                className="rounded-xl object-cover"
                src="images/OmoLogoMark.png"
                alt="Loading Omo Logo"
                width={100}
                height={100}
            />
        </div> 
    )
}
export default PageLoading;