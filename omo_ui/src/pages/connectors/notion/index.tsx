import type { NextPage } from "next";
import { useSession } from "next-auth/react";
import PageLoading from "@/components/PageLoading";
import { NotionConnector } from "@/templates/ConnectorsPage/Notion";
import Layout from "@/components/Layout";

const NotionConnectorPage: NextPage = ({ user }: any) => {
    const { data: session, status } = useSession({
        required: true,
    }) 

    if(status == "loading") {
        return <PageLoading />
    }

    /* TODO the <Layout> object is in this component. Factor out and put here */

    return (
        <Layout hideRightSidebar>
            <NotionConnector />
        </Layout>
    )
};

export default NotionConnectorPage;
