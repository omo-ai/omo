import Layout from "@/components/Layout";
import Main from "./Main";
import Faq from "./Faq";

const PricingPage = () => {
    return (
        <Layout smallSidebar hideRightSidebar>
            <Main />
            <Faq />
        </Layout>
    );
};

export default PricingPage;
