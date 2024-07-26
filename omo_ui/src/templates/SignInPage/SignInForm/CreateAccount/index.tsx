import { useState } from "react";
import Link from "next/link";
import Field from "@/components/Field";

type CreateAccountProps = {};

const CreateAccount = ({}: CreateAccountProps) => {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    return (
        <form action="" onSubmit={() => console.log("Submit")}>
            <Field
                className="mb-4"
                classInput="dark:bg-n-7 dark:border-n-7 dark:focus:bg-transparent"
                placeholder="Email"
                icon="email"
                type="email"
                value={email}
                onChange={(e: any) => setEmail(e.target.value)}
                required
            />
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
            <button className="btn-blue btn-large w-full mb-6" type="submit">
                Create Account
            </button>
            <div className="text-center caption1 text-n-4">
                By creating an account, you agree to our{" "}
                <Link
                    className="text-n-5 transition-colors hover:text-n-7 dark:text-n-3 dark:hover:text-n-1"
                    href="/"
                >
                    Terms of Service
                </Link>{" "}
                and{" "}
                <Link
                    className="text-n-5 transition-colors hover:text-n-7 dark:text-n-3 dark:hover:text-n-1"
                    href="/"
                >
                    Privacy & Cookie Statement
                </Link>
                .
            </div>
        </form>
    );
};

export default CreateAccount;
