import Image from "@/components/Image";
import { useRouter } from 'next/navigation'
import { useState } from "react";
import Modal from "@/components/Modal";

type ApplicationProps = {
    item: any;
};


const Application = ({ item }: ApplicationProps) => {
    const router = useRouter();
    const [visible, setVisible] = useState(false);
    return (
        <div className="flex flex-col w-[calc(33.333%-3.5rem)] mx-7 mt-16 2xl:w-[calc(33.333%-2rem)] 2xl:mx-4 2xl:mt-12 lg:w-[calc(50%-2rem)] md:w-full md:mx-0 md:mt-10">
            <div className="flex items-center mb-auto">
                <div className="shrink-0 w-15 mr-6">
                    <Image
                        className="w-full rounded-xl"
                        src={item.image}
                        width={60}
                        height={60}
                        alt=""
                    />
                </div>
                <div className="grow">
                    <div className="mb-1 base1 font-semibold">{item.title}</div>
                    <div className="caption1 text-n-4">{item.description}</div>
                </div>
            </div>
            {item.available ? (
            <button
                onClick={() => router.push(item.href)}
                className={`btn-stroke-light w-full mt-8 md:mt-6`}
            >
                Add
            </button>
            ) : (
            <button
                onClick={() => setVisible(true)}
                className={`btn-stroke-light w-full mt-8 md:mt-6`}
            >
                Contact Us
            </button> 
            )}
            <Modal
                className="md:!p-0"
                classWrap="max-w-[40rem] md:min-h-screen-ios md:rounded-none md:pb-8"
                classButtonClose="absolute top-6 right-6 w-10 h-10 rounded-full bg-n-2 md:right-5 dark:bg-n-4/25 dark:fill-n-4 dark:hover:fill-n-1"
                visible={visible}
                onClose={() => setVisible(false)}
            >
                <p className="m-20">This connector is only available to select users at the moment.
                    Please email us at <a className="text-indigo-400" href="mailto:founders@helloomo.ai">founders@helloomo.ai</a> to install it.
                </p>
            </Modal>
        </div>
    )
};

export default Application;
