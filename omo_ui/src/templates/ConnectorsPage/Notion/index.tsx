import qs from 'qs';
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Icon from "@/components/Icon";
import Stepper from  "@/components/Stepper"
import Field from "@/components/Field";
import { buildApiUrl } from '@/utils/api';
import NotionConnectButton from "@/components/NotionConnect";
import { signIn } from "next-auth/react";
import useSWR from 'swr';

const initialSteps = [
    {
        name: 'Connect to Notion',
        description: 'Connect to your workspace.',
        href: '#',
        status: 'current',
    },
    { 
        name: 'Review & Confirm',
        description: 'The selected pages will be indexed by our AI engine.', 
        href: '#',
        status: 'upcoming',
    },
    { 
        name: 'Start AI Analysis',
        description: "Omo will analyze your documents and make them ready for searching.",
        href: '#',
        status: 'upcoming',
    },
  ]

export const NotionConnector = () => {
    const router = useRouter();
    const [authUrl, setAuthUrl] = useState('');
    const [accessToken, setAccessToken] = useState('');
    const [steps, setSteps] = useState(initialSteps);
    const [activeStep, setActiveStep] = useState(0);
    const { code } = router.query;

    const redirectUri = process.env.NEXT_PUBLIC_NOTION_REDIRECT_URL;
    const clientId = process.env.NEXT_PUBLIC_NOTION_CLIENT_ID;
    const clientSecret = process.env.NEXT_PUBLIC_NOTION_CLIENT_SECRET;
    const scope = 'read_pages';

    useEffect(() => {
        const params = qs.stringify({
            client_id: clientId,
            redirect_uri: redirectUri,
            response_type: 'code',
            scope,
          });
      
          const authorizationUrl = `https://api.notion.com/v1/oauth/authorize?${params}`;
          setAuthUrl(authorizationUrl);
    }, []);

    const proxyRequestBody = JSON.stringify({
        grant_type: 'authorization_code',
        code,
        redirect_uri: redirectUri,
    });
    
    const proxyRequestPayload = {
        endpoint: 'https://api.notion.com/v1/oauth/token',
        body: proxyRequestBody,
        headers: {
            accept: 'application/json',
            content_type: 'application/json',
            authorization: `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
        }
    }
    
    const accessTokenFetcher = (url: string) => fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
            body: JSON.stringify(proxyRequestPayload)
        }
    ).then((res) => res.json())
     .then((data) => {
        console.log(data)
        setAccessToken(data.access_token)
    });

    const pagesFetcher = (url: string) => fetch(url,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Notion-Authorization': `Bearer ${accessToken}`
            },
            credentials: 'include',
            body: JSON.stringify(proxyRequestPayload)
        }
    ).then( (res) => res.json()).then(data => console.log(data))


    const proxyEndpoint = buildApiUrl('/v1/oauth-proxy/token');
    const { data: tokenData, error: tokenError } = useSWR(code && authUrl && !accessToken ? proxyEndpoint : null, accessTokenFetcher);

    const pagesEndpoint = buildApiUrl('/v1/notion/pages');
    const { data: pageData, error: pageError } = useSWR(accessToken ? pagesEndpoint : null, pagesFetcher);

    return (
        <div className="p-10 md:pt-5 md:px-6 md:pb-10">
            <button
                className="absolute top-6 right-6 w-10 h-10 border-2 border-n-4/25 rounded-full text-0 transition-colors hover:border-transparent hover:bg-n-4/25 md:block"
                onClick={() => router.back()}
            >
                <Icon className="fill-n-4" name="close" />
            </button>
            <div className="h3 leading-[4rem] md:mb-3 md:h3">
                Notion
            </div>
            <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                Connect to a Notion workspace
            </div>

            <div className="grid grid-cols-3">
                <div className="py-5 mr-15 sm:px-6 lg:px-8">
                    <Stepper steps={steps} activeStep={activeStep} />
                </div>
                <div className="col-span-2 relative">
                {/* <button onClick={() => signIn("notion")}>Sign in with Notion</button>; */}
                    <NotionConnectButton authUrl={authUrl}/>

        {/* <form className="" action="" onSubmit={() => console.log("Submit")}>
            <div className="mb-8 h4 md:mb-6">Integration Token</div>
            <Field
                className="mb-6"
                placeholder="Token"
                type="password"
                icon="lock"
                value={integrationToken}
                onChange={(e: any) => { setIntegrationToken(e.target.value)}}
                required
            />
            
        </form> */}
                </div>
            </div>



        </div>
    )
  }