import { useColorMode } from "@chakra-ui/color-mode";
import Logo from "@/components/Logo";
import SignIn from "./SignIn";

const tabNav = ["Sign in", "Create account"];

type FormProps = {};

const SigninForm = ({}: FormProps) => {
    const { colorMode } = useColorMode();
    const isLightMode = colorMode === "light";

    return (
        <div className="w-full max-w-[31.5rem] m-auto">
            <Logo
                className="max-w-[11.875rem] mx-auto mb-8"
                dark={isLightMode}
            />
            <SignIn />
        </div>
    );
};

export default SigninForm;
