import Image from "@/components/Image";
import Icon from "@/components/Icon";
import Post from "./Post";

type ImageType = {
    id: string;
    src: string;
};

type SocialsPostType = {
    id: string;
    icon: string;
    content: string;
    link: string;
    tags: Array<string>;
    images: ImageType[];
};

type SocialsPostProps = {
    items: SocialsPostType[];
};

const SocialsPost = ({ items }: SocialsPostProps) => (
    <div className="">
        <div>
            Here&apos;s an example of promotional content optimized for Twitter
            and Facebook:
        </div>
        <div className="mt-5">
            {items.map((x) => (
                <Post item={x} key={x.id} />
            ))}
        </div>
        <div className="mt-5">
            <div className="flex items-center mb-3">
                <div>Share with</div>
                <div className="ml-3 text-0">
                    <svg
                        className="fill-n-7 dark:fill-n-1"
                        xmlns="http://www.w3.org/2000/svg"
                        width="80"
                        height="20"
                        viewBox="0 0 80 20"
                    >
                        <g clip-path="url(#A)">
                            <path
                                fill-rule="evenodd"
                                d="M.225 4.581L8.79.145l8.657 4.437L8.79 9.033.225 4.581zm51.419 2.157v-.106c0-1.464.861-1.931 2.31-1.826V2.136c-3.473-.211-5.119 1.524-5.119 4.496v.106h-1.571v2.671h1.571v8.087h2.809V9.409h1.661.649.921v8.087h2.809V9.409h2.311V6.738h-2.311v-.106c0-1.464.846-1.931 2.311-1.826V2.136c-3.473-.211-5.119 1.524-5.119 4.496v.106h-.921-.649-1.661zM32.011 9.665c.891-.709 1.435-1.72 1.435-3.018 0-2.52-2.054-4.24-4.636-4.24h-5.995v15.058h6.479c2.643 0 4.757-1.781 4.757-4.361-.03-1.554-.815-2.746-2.039-3.44zm-3.186-4.466c.966 0 1.631.709 1.631 1.66s-.695 1.66-1.631 1.66h-3.005V5.199h3.005zm.453 9.506h-3.458v-3.546h3.458a1.71 1.71 0 0 1 1.767 1.765c0 1.026-.74 1.78-1.767 1.78zm13.531-7.982v5.809c0 1.871-1.027 2.671-2.401 2.671-1.269 0-2.16-.754-2.16-2.218V6.723h-2.809v6.609c0 2.867 1.797 4.451 4.123 4.451 1.465 0 2.598-.543 3.232-1.509v1.207h2.809V6.723h-2.794zm28.83 6.518h-8.216c.408 1.418 1.586 2.022 3.051 2.022 1.102 0 1.978-.453 2.447-1.071l2.265 1.282c-1.012 1.464-2.643 2.308-4.742 2.308-3.655 0-5.966-2.474-5.966-5.688s2.326-5.688 5.754-5.688c3.217 0 5.512 2.52 5.512 5.688 0 .422-.046.785-.106 1.147zm-5.407-4.315c-1.51 0-2.537.8-2.854 2.173h5.558c-.347-1.554-1.526-2.173-2.703-2.173zm9.574-.347V6.723h-2.809v10.758h2.809v-5.145c0-2.263 1.843-2.912 3.308-2.731V6.512c-1.374 0-2.749.604-3.308 2.067zM8.79 16.647l-5.843-3.169-2.722 1.471 8.565 4.64 8.657-4.64-2.752-1.471-5.905 3.169zM2.946 8.478l5.843 2.874 5.905-2.874 2.752 1.341-8.657 4.215L.225 9.819l2.722-1.341z"
                                fill="inherit"
                            />
                        </g>
                        <defs>
                            <clipPath id="A">
                                <path fill="#fff" d="M0 0h79.444v20H0z" />
                            </clipPath>
                        </defs>
                    </svg>
                </div>
            </div>
            <div className="flex flex-wrap -mt-4 -ml-4 md:block md:ml-0">
                <button className="btn-dark btn-medium ml-4 mt-4 px-4 rounded-md md:w-full md:ml-0">
                    <span>Add to Queue</span>
                    <Icon name="share" />
                </button>
                <button className="btn-white btn-medium ml-4 mt-4 px-4 rounded-md md:w-full md:ml-0">
                    <span>Share now</span>
                    <Icon name="share-1" />
                </button>
                <button className="btn-white btn-medium ml-4 mt-4 px-4 rounded-md md:w-full md:ml-0">
                    <span>Schedule post</span>
                    <Icon name="calendar-check" />
                </button>
            </div>
        </div>
    </div>
);

export default SocialsPost;
