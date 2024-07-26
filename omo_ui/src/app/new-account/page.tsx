import SetPassword from "@/components/SignInForm/SetPassword"

const Account = () => {
    return (
    <div className="relative flex min-h-screen min-h-screen-ios lg:p-6 md:px-6 md:pt-16 md:pb-10">
 
        <div className="flex grow my-6 mx-6 p-10 bg-n-1 rounded-[1.25rem] lg:m-0 md:p-0 dark:bg-n-6">

            <div className="w-full max-w-[31.5rem] m-auto">
               
                <SetPassword />
  
            </div>
        </div>
    </div>

 
    )
}

export default Account;