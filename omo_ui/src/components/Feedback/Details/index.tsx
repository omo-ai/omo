import Icon from "@/components/Icon";

type DetailsProps = {};

const Details = ({}: DetailsProps) => (
    <div className="flex items-center p-5 md:block">
        <div className="flex items-center mr-auto">
            <div className="flex justify-center items-center shrink-0 w-15 h-15 rounded-xl bg-[#52BA69]/20">
                <Icon className="w-8 h-8 fill-[#52BA69]" name="codepen" />
            </div>
            <div className="grow pl-4">
                <div className="mb-1 h6">Very good!</div>
                <div className="flex items-center">
                    <div className="flex">
                        <Icon
                            className="w-5 h-5 mr-2 fill-accent-5 md:w-4 md:h-4 md:mr-1"
                            name="star-rating"
                        />
                        <Icon
                            className="w-5 h-5 mr-2 fill-accent-5 md:w-4 md:h-4 md:mr-1"
                            name="star-rating"
                        />
                        <Icon
                            className="w-5 h-5 mr-2 fill-accent-5 md:w-4 md:h-4 md:mr-1"
                            name="star-rating"
                        />
                        <Icon
                            className="w-5 h-5 mr-2 fill-accent-5 md:w-4 md:h-4 md:mr-1"
                            name="star-rating"
                        />
                        <Icon
                            className="w-5 h-5 fill-n-4 md:w-4 md:h-4"
                            name="star-rating"
                        />
                    </div>
                    <div className="ml-2 px-2 bg-n-3 rounded-lg base2 font-semibold text-n-7">
                        4.85
                    </div>
                </div>
            </div>
        </div>
        <button className="btn-dark 2xl:w-12 2xl:p-0 2xl:text-0 md:w-full md:mt-4 md:text-[0.875rem]">
            <span>Download</span>
            <Icon className="2xl:!m-0 md:!ml-3" name="download-fill" />
        </button>
    </div>
);

export default Details;
