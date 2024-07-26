import { useState } from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { srcery } from "react-syntax-highlighter/dist/cjs/styles/hljs";
import { CopyToClipboard } from "react-copy-to-clipboard";
import { twMerge } from "tailwind-merge";
import Icon from "@/components/Icon";

type CodeType = {
    id: string;
    title: string;
    language: string;
    value: string;
};

type CodeProps = {
    items: CodeType[];
};

const Code = ({ items }: CodeProps) => {
    const [value, setValue] = useState<string>("0");
    const [copied, setCopied] = useState<boolean>(false);

    const onCopy = () => {
        setCopied(true);
        setTimeout(() => {
            setCopied(false);
        }, 2000);
    };

    return (
        <div className="space-y-4">
            <div className="rounded-xl overflow-hidden">
                <div className="flex items-center pl-2 pr-4 py-1 bg-n-6">
                    <div className="flex mr-auto md:mr-0 md:w-full">
                        {items.map((item) => (
                            <button
                                className={twMerge(
                                    `min-w-[9rem] h-8 rounded-lg caption1 font-semibold text-n-4 transition-colors hover:text-n-1 2xl:min-w-[1rem] md:basis-1/3 ${
                                        value === item.id && "bg-n-5 text-n-1"
                                    }`
                                )}
                                key={item.id}
                                onClick={() => setValue(item.id)}
                            >
                                {item.title}
                            </button>
                        ))}
                    </div>
                    {copied ? (
                        <div className="flex items-center caption1 font-semibold text-n-1">
                            <Icon
                                className="w-4 h-4 mr-1 fill-n-1"
                                name="check-thin"
                            />
                            Copied!
                        </div>
                    ) : (
                        items
                            .filter((x) => x.id === value)
                            .map((item) => (
                                <CopyToClipboard
                                    key={item.id}
                                    text={item.value}
                                    onCopy={onCopy}
                                >
                                    <button className="shrink-0 ml-3 caption1 font-semibold text-n-1 transition-colors hover:text-primary-1 md:hidden">
                                        Copy code
                                    </button>
                                </CopyToClipboard>
                            ))
                    )}
                </div>
                <div className="max-h-[17.625rem] overflow-auto md:max-h-[20rem]">
                    {items
                        .filter((x) => x.id === value)
                        .map((item) => (
                            <SyntaxHighlighter
                                language={item.language}
                                showLineNumbers
                                style={srcery}
                                customStyle={{
                                    maxWidth: "100%",
                                    padding: "1rem 1rem 1.5rem",
                                }}
                                lineNumberStyle={{
                                    textAlign: "left",
                                    color: "#7A7C7C",
                                }}
                                key={item.id}
                            >
                                {item.value}
                            </SyntaxHighlighter>
                        ))}
                </div>
            </div>
            <div className="">
                Note: This is just an example of a simple HTML form. In a
                real-world scenario, you would also want to include proper
                validation and handling of the form data on the server side.
            </div>
            <div className="flex justify-between items-center pl-4 pr-1 py-1 rounded-xl bg-n-1 shadow-[0_0_1rem_0.5rem_rgba(0,0,0,0.07)] dark:bg-n-6/50">
                I have created a project in your Codepen account
                <button className="shrink-0 btn-dark btn-medium ml-4">
                    <span>View</span>
                    <Icon name="external-link" />
                </button>
            </div>
        </div>
    );
};

export default Code;
