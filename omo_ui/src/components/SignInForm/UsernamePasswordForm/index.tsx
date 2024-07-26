"use client"
import { useState } from "react";
import Field from "@/components/Field";

type SignInProps = {
  onClick: () => void;
};

function UsernamePasswordForm () {
  const [name, setName] = useState<string>("");
  const [password, setPassword] = useState<string>("");

    return (
      //   <div className="flex flex-col gap-2">
      //   {Object.values(providerMap).map((provider: any, index) => (
      //     <form
      //       key={index} 
      //       onSubmit={async () => {
      //         await signIn(provider.id)

      //       }}
      //     >
      //       <button className="btn-blue btn-large w-full" type="submit">
      //         <span>Sign in with {provider.name}</span>
      //       </button>
      //     </form>
      //   ))}
      // </div>
        <form action="" onSubmit={() => console.log("Submit")}>
            <Field
                className="mb-4"
                classInput="dark:bg-n-7 dark:border-n-7 dark:focus:bg-transparent"
                placeholder="Username or email"
                icon="email"
                value={name}
                onChange={(e: any) => setName(e.target.value)}
                required
            />
            <Field
                className="mb-2"
                classInput="dark:bg-n-7 dark:border-n-7 dark:focus:bg-transparent"
                placeholder="Password"
                icon="lock"
                type="password"
                value={password}
                onChange={(e: any) => setPassword(e.target.value)}
                required
            />
            <button
                className="mb-6 base2 text-primary-1 transition-colors hover:text-primary-1/90"
                type="button"
                onClick={() => console.log('click')}
            >
                Forgot password?
            </button>
            <button className="btn-blue btn-large w-full" type="submit">
                Sign in
            </button>
        </form>
    );
};

export default UsernamePasswordForm;
