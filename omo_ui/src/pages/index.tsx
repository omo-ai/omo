import type { NextPage } from "next";
import HomePage from "@/templates/HomePage";
import { useSession } from "next-auth/react"
import { useRouter } from "next/router";
import { useEffect } from "react";
import PageLoading from "@/components/PageLoading";

const Home: NextPage = ( { user }: any) => {
    const { data: session, status } = useSession({
        required: true,
    }) 

    if(status == "loading") {
        return <PageLoading />
    }
    return <HomePage user={user}/>;
};

export default Home;
