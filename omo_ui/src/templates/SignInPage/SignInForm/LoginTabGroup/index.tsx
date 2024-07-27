"use client"
import { Tab } from "@headlessui/react";
import CreateAccount from "@/components/SignInForm/CreateAccount";
import SocialLogin from "@/components/SignInForm/SocialLogin";
import UsernamePasswordForm from "@/components/SignInForm/UsernamePasswordForm";

const tabNav = ["Sign in", "Create account"];

const LoginTabGroup = () => {
    return (
        <Tab.Group defaultIndex={0}>
            <Tab.List className="flex mb-8 p-1 bg-n-2 rounded-xl dark:bg-n-7">
                {tabNav.map((button, index) => (
                    <Tab
                        className="basis-1/2 h-10 rounded-[0.625rem] base2 font-semibold text-n-4 transition-colors outline-none hover:text-n-7 ui-selected:bg-n-1 ui-selected:text-n-7 ui-selected:shadow-[0_0.125rem_0.125rem_rgba(0,0,0,0.07),inset_0_0.25rem_0.125rem_#FFFFFF] tap-highlight-color dark:hover:text-n-1 dark:ui-selected:bg-n-6 dark:ui-selected:text-n-1 dark:ui-selected:shadow-[0_0.125rem_0.125rem_rgba(0,0,0,0.07),inset_0_0.0625rem_0.125rem_rgba(255,255,255,0.02)]"
                        key={index}
                    >
                        {button}
                    </Tab>
                ))}
            </Tab.List>
                
            <SocialLogin />

            <div className="flex items-center my-8 md:my-4">
                <span className="grow h-0.25 bg-n-4/50"></span>
                <span className="shrink-0 mx-5 text-n-4/50">
                    OR
                </span>
                <span className="grow h-0.25 bg-n-4/50"></span>
            </div>
            <Tab.Panels>
                <Tab.Panel>
                    <UsernamePasswordForm />
                </Tab.Panel>
                <Tab.Panel>
                    <CreateAccount /> 
                </Tab.Panel>
            </Tab.Panels>
        </Tab.Group> 
    )
}

export default LoginTabGroup;