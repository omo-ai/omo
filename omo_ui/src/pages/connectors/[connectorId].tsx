import { NextPage } from "next";
import { useRouter } from "next/router";
import Layout from "@/components/Layout";
import { ChatMessage } from "@/components/ChatInput/classes";
import { ConnectorDetails } from "@/templates/ConnectorsPage/ConnectorDetails";
import { buildApiUrl } from "@/utils/api";
import { useEffect } from "react";



const ConnectorDetail: NextPage = () => {
    const router = useRouter()
    const { connectorId } = router.query
    const { t:connectorSlug } = router.query

    if(!connectorId || !connectorSlug) {
        return null;
    }

    const type = Array.isArray(connectorSlug) ? connectorSlug[0] : connectorSlug;
    const id = Array.isArray(connectorId) ? connectorId[0] : connectorId;

    return (
        <Layout hideRightSidebar>
            <ConnectorDetails type={type} id={id}/>
        </Layout>
    )
}

export default ConnectorDetail;