import { useState } from "react";
import Field from "@/components/Field";

type PasswordProps = {};

const Password = ({}: PasswordProps) => {
    const [oldPassword, setOldPassword] = useState<string>("");
    const [newPassword, setNewPassword] = useState<string>("");
    const [confirmPassword, setConfirmPassword] = useState<string>("");

    return (
        <form className="" action="" onSubmit={() => console.log("Submit")}>
            <div className="mb-8 h4 md:mb-6">Password</div>
            <Field
                className="mb-6"
                label="Password"
                placeholder="Password"
                type="password"
                icon="lock"
                value={oldPassword}
                onChange={(e: any) => setOldPassword(e.target.value)}
                required
            />
            <Field
                className="mb-6"
                label="New password"
                placeholder="New password"
                note="Minimum 8 characters"
                type="password"
                icon="lock"
                value={newPassword}
                onChange={(e: any) => setNewPassword(e.target.value)}
                required
            />
            <Field
                className="mb-6"
                label="Confirm new password"
                placeholder="Confirm new password"
                note="Minimum 8 characters"
                type="password"
                icon="lock"
                value={confirmPassword}
                onChange={(e: any) => setConfirmPassword(e.target.value)}
                required
            />
            <button className="btn-blue w-full">Change password</button>
        </form>
    );
};

export default Password;
