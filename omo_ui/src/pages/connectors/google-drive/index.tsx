import type { NextPage } from "next";
import { useSession } from "next-auth/react";
import GoogleDriveConnectorPage from "@/templates/ConnectorsPage/GoogleDrive";
import PageLoading from "@/components/PageLoading";

const GoogleDriveConnector: NextPage = ({ user }: any) => {
    const { data: session, status } = useSession({
        required: true,
    }) 

    if(status == "loading") {
        return <PageLoading />
    }

    /* TODO the <Layout> object is in this component. Factor out and put here */
    return <GoogleDriveConnectorPage user={user}/>;
};

export default GoogleDriveConnector;
