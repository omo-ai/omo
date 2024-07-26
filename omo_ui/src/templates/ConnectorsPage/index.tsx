import { useState, useContext, useEffect, Suspense, act, } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { ExclamationTriangleIcon } from '@heroicons/react/20/solid'
import { Tab } from "@headlessui/react";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";
import Application from "./Application";
import { connectors } from "@/mocks/connectors";
import { AuthContext } from "@/contexts/AuthContext";
import ConnectorStatus from "@/templates/ConnectorsPage/ConnectorStatus";
import { buildApiUrl } from '@/utils/api';

const ConnectorsPage = ({ user }: any) => {
    const [search, setSearch] = useState<string>("");
    const [connectorStatus, setConnectorStatus] = useState([]);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const { omoUser, isOmoUserLoading } = useContext(AuthContext);
    const router = useRouter();

    async function fetchConnectorStatus(endpoint: string) { 
        const response = await fetch(endpoint, {
            credentials: 'include',
        }).then((response) => {
            return response.json();
        }).then((data) => {
            setConnectorStatus(data['statuses']);
        })
    }

    const tabOnChange = (activeTab:number) => {
        setSelectedIndex(activeTab);
    }

    useEffect(() => {

        if(!isOmoUserLoading && omoUser) {
            const endpoint = buildApiUrl('/v1/users/connectors');
            fetchConnectorStatus(endpoint);    
        }

    }, [omoUser, isOmoUserLoading]);
    
    return (
        <Layout hideRightSidebar user={user}>
            <div className="p-10 md:pt-5 md:px-6 md:pb-10">
                <button
                    className="hidden absolute top-6 right-6 w-10 h-10 border-2 border-n-4/25 rounded-full text-0 transition-colors hover:border-transparent hover:bg-n-4/25 md:block"
                    onClick={() => router.back()}
                >
                    <Icon className="fill-n-4" name="close" />
                </button>
                <div className="h3 leading-[4rem] md:mb-3 md:h3">
                    Connectors 
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Browse and install Connectors to start chatting with your data.
                </div>
                
                <Tab.Group selectedIndex={selectedIndex} onChange={tabOnChange}>
                    <Tab.List className="flex mb-8 p-1 bg-n-2 rounded-xl dark:bg-n-7">
                        <Tab className="basis-1/2 h-10 rounded-[0.625rem] base2 font-semibold text-n-4 transition-colors outline-none hover:text-n-7 ui-selected:bg-n-1 ui-selected:text-n-7 ui-selected:shadow-[0_0.125rem_0.125rem_rgba(0,0,0,0.07),inset_0_0.25rem_0.125rem_#FFFFFF] tap-highlight-color dark:hover:text-n-1 dark:ui-selected:bg-n-6 dark:ui-selected:text-n-1 dark:ui-selected:shadow-[0_0.125rem_0.125rem_rgba(0,0,0,0.07),inset_0_0.0625rem_0.125rem_rgba(255,255,255,0.02)]">
                            Added Connectors
                        </Tab>
                        <Tab className="basis-1/2 h-10 rounded-[0.625rem] base2 font-semibold text-n-4 transition-colors outline-none hover:text-n-7 ui-selected:bg-n-1 ui-selected:text-n-7 ui-selected:shadow-[0_0.125rem_0.125rem_rgba(0,0,0,0.07),inset_0_0.25rem_0.125rem_#FFFFFF] tap-highlight-color dark:hover:text-n-1 dark:ui-selected:bg-n-6 dark:ui-selected:text-n-1 dark:ui-selected:shadow-[0_0.125rem_0.125rem_rgba(0,0,0,0.07),inset_0_0.0625rem_0.125rem_rgba(255,255,255,0.02)]">
                            Available Connectors
                        </Tab>
                    </Tab.List>
                    <Tab.Panels>
                        <Tab.Panel>
                            {/* <form
                                className="mb-8"
                                action=""
                                onSubmit={() => console.log("Submit")}
                            >
                                <div className="relative">
                                    <button
                                        className="group absolute top-5 left-5 outline-none"
                                        type="submit"
                                    >
                                        <Icon
                                            className="fill-n-4 transition-colors group-hover:fill-n-7"
                                            name="search"
                                        />
                                    </button>
                                    <input
                                        className="w-full h-16 pl-13 pr-6 bg-n-2 border-2 border-transparent rounded-xl outline-none base1 text-n-7 transition-colors placeholder:text-n-4 focus:border-n-3 focus:bg-transparent dark:bg-n-7 dark:text-n-1 dark:focus:bg-n-6 dark:focus:border-n-7"
                                        type="text"
                                        name="search"
                                        placeholder="Search Added Connectors"
                                        value={search}
                                        onChange={(e: any) => setSearch(e.target.value)}
                                    />
                                </div>
                            </form> */}
                            {connectorStatus.length == 0 ? (
                                <div className="border-l-4 border-yellow-400 bg-yellow-50 p-4">
                                    <div className="flex">
                                    <div className="flex-shrink-0">
                                        <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400" aria-hidden="true" />
                                    </div>
                                    <div className="ml-3">
                                        <p className="text-sm text-yellow-700">
                                        No Connectors added yet. &nbsp;
                                        <Link
                                            href={{
                                                pathname: "/connectors",
                                            }}
                                            onClick={(e) => { e.preventDefault(); setSelectedIndex(1); }}
                                            className="font-medium text-yellow-700 underline hover:text-yellow-600">
                                                Get started.
                                        </Link>
                                        </p>
                                    </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="my-11">
                                    <Suspense fallback={<div>Loading...</div>}>
                                        <ConnectorStatus items={connectorStatus} />
                                    </Suspense>
                                </div>
                                )
                            }
                            
                        </Tab.Panel>
                        <Tab.Panel>
                            {/* <form
                                className="mb-8"
                                action=""
                                onSubmit={() => console.log("Submit")}
                            >
                                <div className="relative">
                                    <button
                                        className="group absolute top-5 left-5 outline-none"
                                        type="submit"
                                    >
                                        <Icon
                                            className="fill-n-4 transition-colors group-hover:fill-n-7"
                                            name="search"
                                        />
                                    </button>
                                    <input
                                        className="w-full h-16 pl-13 pr-6 bg-n-2 border-2 border-transparent rounded-xl outline-none base1 text-n-7 transition-colors placeholder:text-n-4 focus:border-n-3 focus:bg-transparent dark:bg-n-7 dark:text-n-1 dark:focus:bg-n-6 dark:focus:border-n-7"
                                        type="text"
                                        name="search"
                                        placeholder="Search Connectors"
                                        value={search}
                                        onChange={(e: any) => setSearch(e.target.value)}
                                    />
                                </div>
                            </form> */}
                            <div className="my-11">
                                <div className="mb-11 h6 text-n-4 md:mb-6">Suggested Connectors</div>
                                <div className="flex flex-wrap -mx-7 -mt-16 2xl:-mx-4 2xl:-mt-12 md:block md:mt-0 md:mx-0">
                                    {connectors.map((connector, index) => (
                                        <Application item={connector} key={index} />
                                    ))}
                                </div>
                            </div>
                        </Tab.Panel>
                    </Tab.Panels>
                </Tab.Group>
            </div>
        </Layout>
    );
};

export default ConnectorsPage;
