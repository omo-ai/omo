import Image from "@/components/Image";
import { AppIconProps } from "@/components/AppIcon";

export const GoogleDriveIcon = ({width, height}: AppIconProps) => {
    return (
        <Image
            className="w-full rounded-xl"
            src="/images/GoogleDriveMark.png"
            width={width}
            height={height}
            alt="Google Drive Icon"
        />
    )
}
