import { classNames } from '@/utils/common';
import { FiletypeIcon } from '@/components/FileTypeIcon'
import { bgColorForMimeType } from '@/utils/files';

type IconBackgoundType = {
    mimetype: string;
}

export const IconBackgound = ({ mimetype }: IconBackgoundType) => {
    return (
        <div
            className={classNames(
                bgColorForMimeType(mimetype),
            'flex w-16 flex-shrink-0 items-center justify-center rounded-l-md text-sm font-medium text-white'
            )}
            >
            <FiletypeIcon
            mimetype={mimetype}
            width={30}
            height={30}
            alt="Document icon" />
      </div>
    )
}