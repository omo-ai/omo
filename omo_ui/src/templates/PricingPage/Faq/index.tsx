import FaqItem from "@/components/FaqItem";

import { faqPricing } from "@/mocks/faq";

type FaqProps = {};

const Faq = ({}: FaqProps) => (
    <div className="py-32 px-15 2xl:py-20 2xl:px-10 xl:px-8 dark:bg-n-7/25">
        <div className="max-w-[47.75rem] mx-auto">
            <div className="mb-12 text-center h3 lg:h4">
                Frequently asked questions
            </div>
            <div>
                {faqPricing.map((x) => (
                    <FaqItem item={x} key={x.id} />
                ))}
            </div>
        </div>
    </div>
);

export default Faq;
