import Link from "next/link";

const items = [
    {
        title: "Home",
        url: "/",
    },
    {
        title: "Code generation",
        url: "/code-generation",
    },
    {
        title: "Photo edition",
        url: "/photo-editing",
    },
    {
        title: "Video generation",
        url: "/video-generation",
    },
    {
        title: "Audio generation",
        url: "/audio-generation",
    },
    {
        title: "Generation socials post",
        url: "/generation-socials-post",
    },
    {
        title: "Education feedback",
        url: "/education-feedback",
    },
    {
        title: "Pricing",
        url: "/pricing",
    },
    {
        title: "Checkout",
        url: "/checkout",
    },
    {
        title: "Thank you",
        url: "/thanks",
    },
    {
        title: "Sign In",
        url: "/sign-in",
    },
    {
        title: "Updates and FAQ",
        url: "/updates-and-faq",
    },
    {
        title: "Connectors",
        url: "/connectors",
    },
];

const PageListPage = () => {
    return (
        <div className="flex flex-col items-start px-12 py-8 text-xl">
            {items.map((item, index) => (
                <Link
                    className="text-n-1 transition-colors hover:text-primary-1 md:text-n-7 dark:text-n-1"
                    href={item.url}
                    key={index}
                >
                    {item.title}
                </Link>
            ))}
        </div>
    );
};

export default PageListPage;
