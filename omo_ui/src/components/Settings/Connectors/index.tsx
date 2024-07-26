import Link from "next/link";
import Connector from "./Connector";

import { connectors } from "@/mocks/connectors";

type ConnectorsProps = {};

const Connectors = ({}: ConnectorsProps) => (
    <>
        <div className="flex items-center mb-8">
            <div className="mr-auto h4">Connectors</div>
            <Link className="btn-blue" href="/connectors">
                Add connector
            </Link>
        </div>
        <div className="py-3 base2 text-n-4">Authorized connectors</div>
        <div className="mb-6">
            {connectors
                .filter((x: any) => x.installed === true)
                .map((connector) => (
                    <Connector item={connector} key={connector.id} />
                ))}
        </div>
    </>
);

export default Connectors;
