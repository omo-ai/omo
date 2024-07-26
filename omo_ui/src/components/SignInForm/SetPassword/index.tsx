"use client"
import { useState } from "react";
import Icon from "@/components/Icon";
import Field from "@/components/Field";

type SetPasswordProps = {
    onClick: () => void;
};

const SetPassword = () => {
    const [password, setPassword] = useState<string>("");

    return (
        <>
            <button
                className="group flex items-center mb-8 h5"
            >
 
                Set a password
            </button>
            <div className="mb-10">
                Thanks for signing up! Since it&apos;s your first time here,
                please set a password for your account.
            </div>
            <form action="" onSubmit={() => console.log("Submit")}>
                <Field
                    className="mb-6"
                    classInput="dark:bg-n-7 dark:border-n-7 dark:focus:bg-transparent"
                    placeholder="Password"
                    icon="lock"
                    type="password"
                    value={password}
                    onChange={(e: any) => setPassword(e.target.value)}
                    required
                />

                <button
                    className="btn-blue btn-large w-full mb-6"
                    type="submit"
                >
                    Create Account 
                </button>
            </form>
        </>
    );
};

export default SetPassword;
