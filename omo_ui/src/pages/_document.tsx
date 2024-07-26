import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
    return (
        <Html lang="en">
            <Head>
                <meta
                    content="Retrieval augmented generation for company data"
                    name="OmoAI - chat with your data at scale"
                />
                <meta content="OmoAI - chat with your data at scale" property="og:title" />
                <meta
                    content="Figma UI kit designed to enhance the functionality of ChatGPT"
                    property="og:description"
                />
                <meta
                    content="%PUBLIC_URL%/fb-og-image.png"
                    property="og:image"
                />
                <meta
                    property="og:url"
                    content="https://helloomo.ai"
                />
                <meta property="og:site_name" content="OmoAI" />
                <meta
                    content="OmoAI"
                    property="twitter:title"
                />
                <meta
                    content="OmoAI - chat with your companies data at scale"
                    property="twitter:description"
                />
                <meta
                    content="%PUBLIC_URL%/twitter-card.png"
                    property="twitter:image"
                />
                <meta property="og:type" content="Article" />
                <meta content="summary" name="twitter:card" />
                <meta name="twitter:site" content="@ui8" />
                <meta name="twitter:creator" content="@ui8" />
                <meta property="fb:admins" content="132951670226590" />
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1, maximum-scale=1"
                />
                <meta name="msapplication-TileColor" content="#da532c" />
                <meta name="theme-color" content="#ffffff" />
            </Head>
            <body>
                <Main />
                <NextScript />
            </body>
        </Html>
    );
}
