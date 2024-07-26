import type { NextPage } from "next";
import { useSession } from "next-auth/react";
import { useRouter } from "next/router";
import ConnectorsPage from "@/templates/ConnectorsPage";
import PageLoading from "@/components/PageLoading";

const Loading: NextPage = () => {
    return <PageLoading />;
};

export default Loading;
