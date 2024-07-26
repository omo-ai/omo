import { useState } from "react";
import Radio from "@/components/Radio";
import Package from "./Package";
import Features from "./Features";

import { price, featuresPrice } from "@/mocks/price";

type MainProps = {};

const Main = ({}: MainProps) => {
    const [plan, setPlan] = useState(false);

    return (
        <div className="py-32 px-15 bg-n-2 rounded-t-[1.25rem] 2xl:py-20 2xl:px-10 xl:px-8 md:rounded-none dark:bg-n-6">
            <div className="max-w-[75.25rem] mx-auto">
                <div className="mb-20 text-center 2xl:mb-16 lg:mb-10">
                    <div className="mb-4 h2 lg:h3">AI chat made affordable</div>
                    <div className="body1 text-n-4">
                        Pricing Plans for every budget
                    </div>
                </div>
                <div className="flex mb-20 py-4 2xl:block 2xl:py-0 lg:mb-0">
                    <div className="w-[14.875rem] pt-8 pr-6 2xl:w-full 2xl:mb-20 2xl:pt-0 2xl:pr-0 lg:mb-10">
                        <div className="mb-6 h4 2xl:mb-5 2xl:text-center">
                            Choose plan
                        </div>
                        <div className="2xl:flex 2xl:justify-center">
                            <Radio
                                className="mb-4 2xl:mb-0 2xl:mr-4"
                                name="plan"
                                value={plan}
                                onChange={() => setPlan(true)}
                                content="Yearly billing"
                            />
                            <Radio
                                name="plan"
                                value={!plan}
                                onChange={() => setPlan(false)}
                                content="Monthly billing"
                            />
                        </div>
                    </div>
                    <div className="flex grow lg:overflow-auto lg:scroll-smooth lg:scrollbar-none lg:py-6 lg:-mx-8 lg:before:shrink-0 lg:before:w-8 lg:after:shrink-0 lg:after:w-8">
                        {price.map((x) => (
                            <Package item={x} plan={plan} key={x.id} />
                        ))}
                    </div>
                </div>
                <Features items={featuresPrice} />
            </div>
        </div>
    );
};

export default Main;
