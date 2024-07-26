import Layout from "@/components/Layout";
import Details from "./Details";
import Form from "./Form";

const CheckoutPage = () => {
    return (
        <Layout backUrl="/pricing" smallSidebar hideRightSidebar>
            <div className="px-15 py-12 2xl:px-10 2xl:py-14 xl:px-8 lg:pt-20 md:pt-5 md:px-6">
                <div className="max-w-[58.25rem] mx-auto">
                    <div className="mb-4 h2 md:h3 md:pr-16">
                        AI chat made affordable
                    </div>
                    <div className="body1 text-n-4 md:body2">
                        Pricing Plans for every budget - Unlock the power of AI
                    </div>
                    <div className="flex justify-between mt-10 pt-16 border-t border-n-3 lg:block lg:mt-6 lg:pt-0 lg:border-0 md:mt-10 md:border-t md:pt-4 dark:border-n-5">
                        <div className="w-full max-w-[20.375rem] lg:max-w-full lg:mb-8">
                            <Details />
                        </div>
                        <div className="w-[29.875rem] xl:w-[29rem] lg:w-full">
                            <Form />
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default CheckoutPage;
