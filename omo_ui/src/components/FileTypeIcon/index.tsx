import Image from "@/components/Image";
import { iconForMimeType } from "@/utils/files";

type FiletypeIconType = {
    mimetype: string,
    width: number,
    height: number,
    alt: string,
    className?: string
}

export const FiletypeIcon = (icon : FiletypeIconType) => {

    return (
        <Image
            src={iconForMimeType(icon.mimetype)}
            height={icon.width}
            width={icon.height}
            className={icon.className ? icon.className : ""}
            alt={icon.alt}
    />
    )
}