import { SimpleCardFile } from '@/components/SimpleCardFile';

export type GDriveFile = {
  id: string;
  serviceId: string;
  name: string;
  description: string;
  type: string;
  mimetype: string;
  lastEditedUtc: number;
  url: string;
  sizeBytes: number;
  lastSyncedAt?: Date;
}

type SelectedFiles = {
  files: any[];
  setSelectedFiles: any;
}



export function FileSelectionGrid({ files, setSelectedFiles }: SelectedFiles) {

  const handleClick = (file: any) => {
    setSelectedFiles(
      files.filter(f =>
        f.id !== file.id
      )
    )
  }

  return (
    <div>
      {/* <h2 className="text-sm font-medium text-gray-500">Selected Files</h2> */}
      <ul role="list" className="mt-3 grid grid-cols-2 gap-4 sm:grid-cols-2 sm:gap-6 lg:grid-cols-4">
        {files.map((file) => (
          <li key={file.name} className="col-span-1 flex rounded-md shadow-sm">
            <SimpleCardFile file={file} handleClick={handleClick}/>
          </li>
        ))}
      </ul>
    </div>
  )
}