import Image from "@/components/Image";
import Icon from "@/components/Icon";
import Details from "../Details";

type PostProps = {
    item: any;
};

const Post = ({ item }: PostProps) => (
    <div className="flex mb-4 p-5 bg-n-1 rounded-xl last:mb-0 md:block dark:bg-n-6">
        <div className="shrink-0 w-10">
            <Image
                className="w-full"
                src={item.icon}
                width={40}
                height={40}
                alt=""
            />
        </div>
        <div className="w-[calc(100%-2.5rem)] pl-4 md:w-full md:pl-0 md:pt-4">
            <div>
                {item.content}{" "}
                <a
                    className="underline text-primary-1 break-words"
                    href={item.link}
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    {item.link}
                </a>
                {item.tags.map((tag: any, index: number) => (
                    <span className="text-primary-1" key={index}>
                        {" "}
                        #{tag}
                    </span>
                ))}
            </div>
            <Details images={item.images} />
            <div className="flex flex-wrap mt-1 -ml-3 md:-mr-2">
                <button className="btn-stroke-light btn-small ml-3 mt-3">
                    <span>Share now</span>
                    <Icon name="external-link" />
                </button>
                <button className="btn-stroke-light btn-small ml-3 mt-3">
                    <span>Edit</span>
                    <Icon name="edit" />
                </button>
                <button className="btn-stroke-light btn-small ml-3 mt-3">
                    <span>New variation</span>
                    <Icon name="plus" />
                </button>
                <button className="btn-stroke-light btn-small ml-3 mt-3">
                    <span>Copy</span>
                    <Icon name="copy" />
                </button>
            </div>
        </div>
    </div>
);

export default Post;
