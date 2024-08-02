// import Link from "next/link"; 
// import Logo from "@/components/Logo";
import Link from "next/link"
import Icon from "@/components/Icon"
// import SigninForm from "@/components/SignInForm";

// import { Tab } from "@headlessui/react";
// import CreateAccount from "@/components/SignInForm/CreateAccount";
// import ForgotPassword from "@/components/SignInForm/ForgotPassword";
// import UsernamePasswordForm from "@/components/SignInForm/UsernamePasswordForm";
// import LoginTabGroup from "@/templates/SignInPage/SignInForm/LoginTabGroup";

import SocialLogin from "@/components/SignInForm/SocialLogin"
import Image from "@/components/Image"

export default function LoginPage() {

  return (
    <div className="relative flex min-h-screen min-h-screen-ios lg:p-6 md:px-6 md:pt-16 md:pb-10">
        <div className="relative shrink-0 w-[40rem] p-20 overflow-hidden 2xl:w-[37.5rem] xl:w-[30rem] xl:p-10 lg:hidden">
            
            <div className="max-w-[25.4rem]">
                <Image
                    className="mb-15"
                    src="/images/OmoLogo-White.png"
                    alt="Omo"
                    width={200}
                    height={200}
                    priority
                />
                <div className="mb-4 h2 text-n-1">
                    All your data, chattable.
                </div>
                <div className="body1 text-n-3">
                    AI-powered search and chat for private data.
                </div>
            </div>
            <div className="absolute top-52 left-5 right-5 h-[50rem] xl:top-24">
            </div>
        </div>
        <div className="flex grow my-6 mr-6 p-10 bg-n-1 rounded-[1.25rem] lg:m-0 md:p-0 dark:bg-n-6">


            <div className="w-full max-w-[24.5rem] m-auto">
                <div className="mb-10 text-center">
            
                    <h2 className="text-2xl font-bold leading-9 tracking-tight">
                        Sign in to your account
                    </h2>
                    <p className="mt-2 mb-15 text-md leading-6 font-semibold text-indigo-600">
                        Try it free for 14 days. No credit card required.
                    </p>
                    </div>
                {/* <LoginTabGroup/> */}
                {/* The social login page needs to be at the server component level 
                    If we try to have the social logins with a client component,
                    as is the case with LoginTabGroup, an exception will be thrown.
                    More about the issue with tabs are here: https://github.com/tailwindlabs/headlessui/issues/2021
                */}


                            <SocialLogin /> 
  

                            {/* <div className="flex items-center my-8 md:my-4">
                                <span className="grow h-0.25 bg-n-4/50"></span>
                                <span className="shrink-0 mx-5 text-n-4/50">
                                    OR
                                </span>
                                <span className="grow h-0.25 bg-n-4/50"></span>
                            </div> */}
                            {/* <UsernamePasswordForm /> */}
                            {/* <CreateAccount /> */}
            </div>
        </div>
    </div>

  )
}