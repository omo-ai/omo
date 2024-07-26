import { Disclosure, Transition } from "@headlessui/react";

type FaqItemProps = {
    item: any;
};

const FaqItem = ({ item }: FaqItemProps) => (
    <div className="border-t border-n-3 dark:border-n-6">
        <Disclosure defaultOpen={item.defaultOpen}>
            <Disclosure.Button className="flex w-full py-6 h6 transition-colors hover:text-primary-1 tap-highlight-color lg:hover:text-n-7 dark:lg:hover:text-n-1">
                <div className="relative shrink-0 w-8 h-8 mr-8 before:absolute before:top-1/2 before:l-1/2 before:w-4 before:h-0.5 before:-translate-x-1/2 before:-translate-y-1/2 before:bg-n-6 before:rounded-full after:absolute after:top-1/2 after:l-1/2 after:w-0.5 after:h-4 after:-translate-x-1/2 after:-translate-y-1/2 after:bg-n-6 after:rounded-full after:transition-transform after:ui-open:rotate-90 md:mr-6 dark:before:bg-n-3 dark:after:bg-n-3"></div>
                <div className="text-left">{item.title}</div>
            </Disclosure.Button>
            <Transition
                enter="transition duration-100 ease-out"
                enterFrom="transform scale-95 opacity-0"
                enterTo="transform scale-100 opacity-100"
                leave="transition duration-75 ease-out"
                leaveFrom="transform scale-100 opacity-100"
                leaveTo="transform scale-95 opacity-0"
            >
                <Disclosure.Panel className="-mt-4 pl-16 pb-6 base1 text-n-4 md:pl-14">
                    {item.content}
                </Disclosure.Panel>
            </Transition>
        </Disclosure>
    </div>
);

export default FaqItem;
