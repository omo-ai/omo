import Member from "./Member";

import { members } from "@/mocks/members";

type TeamProps = {};

const Team = ({}: TeamProps) => (
    <>
        <div className="flex items-center mb-8 md:mb-6">
            <div className="mr-auto h4">Members</div>
            <button className="btn-blue">Invite</button>
        </div>
        <div className="py-3 base2 text-n-4">42 members</div>
        <div className="mb-6">
            {members.map((member, index) => (
                <Member
                    item={member}
                    key={member.id}
                    style={{ zIndex: members.length - index }}
                />
            ))}
        </div>
    </>
);

export default Team;
