import { useState } from "react";
import Link from "next/link";
import Icon from "@/components/Icon";
import Image from "@/components/Image";
import DropdownWithIcons from "@/components/DropdownWithIcons";
import { GoogleDriveIcon } from "@/components/AppIcon/GoogleDriveIcon";
import Modal from "@/components/Modal";


type StatusProps = {
    items: any;
};

const getConnectorIcon = (appSlug: string) => {
    switch(appSlug) {
        case 'googledrive':
            return <GoogleDriveIcon width={8} height={8} />
    }
}

const ConnectorStatus = ({ items }: StatusProps) => {

    return (
        <div>
            <div className="flex mb-8 h4">
                <div className="h6 text-n-4">Connector Status</div>
            </div>
            <div className="flex items-center font-bold py-3">
                    <div className="shrink-0 w-8 mr-6">
                    </div>
                    <div className="w-[14.875rem] base2 font-semibold">
                    </div>
                    <div className="flex items-center flex-1 px-8">
                        Files
                    </div>
                    <div className="flex items-center flex-1 px-8 capitalize">
                        Sync status
                    </div>
                    <div className="flex items-center flex-1 px-8">
                    </div>
                </div>
                {items ? items.map((item: any, index: number) => (
                <div
                    className="flex items-center py-3 border-t border-n-4/15"
                    key={item.connector.name + "-" + index}
                >

                    <div className="shrink-0 w-8 mr-6">
                        {getConnectorIcon(item.connector.slug)}
                    </div>
                    
                    <div className="w-[14.875rem] base2 font-semibold">
                        <Link href={{
                            pathname: "/connectors/" + item.connector.id,
                            query: { t: item.connector.slug },
                        }}
                        >
                        {item.connector.name}
                        </Link>
                    </div>
                    <div className="flex items-center flex-1 px-8">
                        <Link href={{
                            pathname: "/connectors/" + item.connector.id,
                            query: { t: item.connector.slug },
                        }}
                        >
                        {item.files_count} Files
                        </Link>
                    </div>
                    <div className="flex items-center flex-1 px-8 capitalize">
                        {item.status}
                    </div>
                    <div className="flex items-center flex-1 px-8">
                        <DropdownWithIcons />
                    </div>
                </div>
                )) : 
                    <></>
                }
            </div>
    )
};

export default ConnectorStatus;
