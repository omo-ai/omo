import "@/styles/globals.css";
import type { AppProps } from "next/app";
import { Toaster, resolveValue } from "react-hot-toast";
import { Inter, Karla } from "next/font/google";
import { ColorModeScript, ColorModeProvider } from "@chakra-ui/color-mode";
import { SessionProvider } from "next-auth/react";
import { AuthProvider } from "@/contexts/AuthContext";
import { ChatProvider } from "@/contexts/ChatContext";
import { ChatHistoryProvider } from "@/contexts/ChatHistoryContext";

const inter = Inter({
    weight: ["500", "600", "700"],
    subsets: ["latin"],
    display: "block",
    variable: "--font-inter",
});

const karla = Karla({
    weight: ["400", "700"],
    subsets: ["latin"],
    display: "block",
    variable: "--font-karla",
});


export default function App(
    { Component,
        pageProps: { session, ...pageProps }, 
    }: AppProps) {
    return (
        <main className={`${karla.variable} ${inter.variable} font-sans`}>
            <style jsx global>{`
                html {
                    font-family: ${karla.style.fontFamily};
                }
                #headlessui-portal-root {
                    font-family: ${inter.style.fontFamily};
                }
            `}</style>
            <SessionProvider session={session}>
                <AuthProvider>
                    <ChatProvider>
                        <ChatHistoryProvider>
                        <ColorModeProvider>
                            <ColorModeScript
                                initialColorMode="system"
                                key="chakra-ui-no-flash"
                                storageKey="chakra-ui-color-mode"
                            />
                            <Component {...pageProps} />
                            <Toaster
                                containerStyle={{
                                    bottom: 40,
                                    left: 20,
                                    right: 20,
                                }}
                                position="bottom-center"
                                gutter={10}
                                toastOptions={{
                                    duration: 2000,
                                }}
                            >
                                {(t) => (
                                    <div
                                        style={{
                                            opacity: t.visible ? 1 : 0,
                                            transform: t.visible
                                                ? "translatey(0)"
                                                : "translatey(0.75rem)",
                                            transition: "all .2s",
                                        }}
                                    >
                                        {resolveValue(t.message, t)}
                                    </div>
                                )}
                            </Toaster>
                        </ColorModeProvider>
                        </ChatHistoryProvider>
                    </ChatProvider>
                </AuthProvider>
            </SessionProvider>
        </main>
    );
}
