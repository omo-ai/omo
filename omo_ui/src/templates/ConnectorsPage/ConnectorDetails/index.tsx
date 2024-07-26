import { useState, useEffect } from "react";
import { useRouter, } from "next/router";
import Icon from "@/components/Icon";
import { buildApiUrl } from "@/utils/api";

export type ConnectorDetailType = {
    id: number,
    files: any,
    created_at: string,
    updated_at: string,
    team_id: number
    delegate_email: string,
}

type ConnectorDetailProps = {
   type: string, 
   id: string,
}
export const ConnectorDetails = ({type, id} : ConnectorDetailProps) => {
    const router = useRouter()
    const [connDetails, setConnDetails] = useState<ConnectorDetailType>({
        id: 0,
        files: [],
        created_at: '',
        updated_at: '',
        team_id: 0,
        delegate_email: '',
    });

    useEffect(() => {
        if (!type|| !id) {
            return
        }
        const endpoint = buildApiUrl('/v1/connectors/' + type + '/' + id)

        fetch(endpoint, {
            credentials: 'include',
        }).then((response) => {
            return response.json();
        }).then((data) => {
            setConnDetails((prevData: ConnectorDetailType) => {
                return {...data}
            })
        })
    }, [type, id])

    return (
        <div className="p-10 md:pt-5 md:px-6 md:pb-10">
            <button
                className="absolute top-6 right-6 w-10 h-10 border-2 border-n-4/25 rounded-full text-0 transition-colors hover:border-transparent hover:bg-n-4/25 md:block"
                onClick={() => router.back()}
            >
                <Icon className="fill-n-4" name="close" />
            </button>
            <div className="h3 leading-[4rem] md:mb-3 md:h3">
                Google Drive 
            </div>
            <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                Connection Details
            </div>
                <div className="mt-8 flow-root">
                    <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                        <table className="min-w-full divide-y divide-gray-300 dark:divide-n-5">
                        <thead>
                            <tr>
                            <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-md font-semibold text-gray-900 sm:pl-3 dark:text-white">
                                File name
                            </th>
                            <th scope="col" className="px-3 py-3.5 text-left text-md font-semibold text-gray-900 dark:text-white">
                                Type 
                            </th>
                            </tr>
                        </thead>
                        <tbody className="bg-white dark:bg-n-6">
                            {connDetails.files.map((file: any, index: number) => (
                            <tr key={index} className="even:bg-gray-50 dark:even:bg-n-7">
                                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-3 dark:text-white">
                                <a target="_blank" href={file.url} rel="noopener noreferrer">
                                    {file.name}
                                </a>
                                </td>
                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-white">{file.type}</td>
                                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-3 dark:text-white">
                                {/* <a href="#" className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-300 dark:hover:text-indigo-500">
                                    View 
                                </a> */}
                                </td>
                            </tr>
                            ))}
                        </tbody>
                        </table>
                    </div>
                    </div>
                </div>

                <div className="absolute bottom-5 right-8">
                    <p className="mt-5 text-sm">Connector ID: {connDetails.id}</p>
                </div>
        </div>
    )
}