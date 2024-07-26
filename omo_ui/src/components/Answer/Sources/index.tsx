import Link from "next/link";
import { FiletypeIcon } from "@/components/FileTypeIcon";
import { useContext } from "react";
import Chat from "@/components/Chat";
import { ChatContext } from "@/contexts/ChatContext";

type SourcesProps = {
    sources: any[];
}
type SourceProps = {
    file_name: string;
    file_path: string;
    file_type: string;
    page_labels: any[];
};

const Sources = ({ sources }: SourcesProps) => {
    const { chatId } = useContext(ChatContext);
    
    const sourceItems = sources.map((source: SourceProps, index: number) => (
        <li key={index}>
            <FiletypeIcon
                className={"mr-3"}
                mimetype={source.file_type}
                height={20}
                width={20}
                alt="Document icon"
            />
            <Link href={source.file_path}>{source.file_name}
                {source.page_labels.length > 0 ?  ( 
                    <span className="text-xs">&nbsp;(pages: {source.page_labels.join(', ')})</span>
                ) : (
                    <></>
                )}
            </Link>
        </li>
    ))

    return (
        <div className="mt-5">
            { sources.length > 0 ? (
                <>
                    <p className="mb-3">Sources:</p>
                    <ul>
                        {sourceItems}        
                    </ul>
                </>
            ) : (
                <></>
            ) }
        </div>
    )
}

export default Sources;