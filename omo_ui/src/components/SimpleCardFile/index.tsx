import { XCircleIcon } from '@heroicons/react/20/solid'
import { IconBackgound } from './IconBackground';

type SimpleCardFileType = {
  file: any;
  handleClick: any;
}

export const SimpleCardFile = ( { file, handleClick }: SimpleCardFileType ) => {

    return (
        <>
            <IconBackgound mimetype={file.mimetype} />

            <div className="flex flex-1 items-center justify-between truncate rounded-r-md border-b border-r border-t border-gray-200 bg-white">
              <div className="flex-1 truncate px-4 py-2 text-sm">
                <a href={file.href} className="font-medium text-gray-900 hover:text-gray-600">
                  {file.name}
                </a>
                <p className="text-gray-500 capitalize">{file.type}</p>
              </div>
              <div className="flex-shrink-0 pr-2">
                <button
                  type="button"
                  className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-transparent bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  <span className="sr-only">Remove document</span>
                  <XCircleIcon className="h-5 w-5" aria-hidden="true" onClick={() => handleClick(file)}/>
                </button>
              </div>
            </div>
        </>
    )

}