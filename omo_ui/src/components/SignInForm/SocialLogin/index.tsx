import { signIn, auth, providerMap } from "@/auth";
// import { signIn } from "next-auth/react"
import Image from "@/components/Image";

const SocialLogin = () => {

    return (
        <>
        {Object.values(providerMap).map((provider: any, index: number) => (
                <form
                    key={index} 
                    action={async ()=> {
                        "use server"
                        await signIn(provider.id, { redirectTo: "/" })
                    }}
                >
                    <button className="btn-stroke-light btn-large w-full mb-3">
                        <Image
                            src="/images/google.svg"
                            width={24}
                            height={24}
                            alt=""
                        />
                        <span className="ml-4">Continue with {provider.name}</span>
                        </button>
                </form>
            ))}
        {/* <button className="btn-stroke-light btn-large w-full mb-3">
            <Image
                src="/images/microsoft.svg"
                width={24}
                height={24}
                alt=""
            />
            <span className="ml-4">Continue with Microsoft</span>
        </button>

        <button className="btn-stroke-light btn-large w-full mb-3">
            <Image
                src="/images/apple.svg"
                width={24}
                height={24}
                alt=""
            />
            <span className="ml-4">Continue with Apple</span>
        </button> */}

        </>
    )

}
export default SocialLogin;