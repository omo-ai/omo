import type { NextPage } from "next";
import { useSession } from "next-auth/react";
import { useRouter } from "next/router";
import ConnectorsPage from "@/templates/ConnectorsPage";
import PageLoading from "@/components/PageLoading";

const Connectors: NextPage = ({ user }: any) => {
    const { data: session, status } = useSession({
        required: true,
    }) 
    if(status == "loading") {
        return <PageLoading />
    }
    return <ConnectorsPage user={user}/>;
};

export default Connectors;
