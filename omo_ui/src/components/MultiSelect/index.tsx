import Select, { components } from "react-select";
import Image from "@/components/Image";
import Icon from "@/components/Icon";

const { Option, MultiValueRemove } = components;

const DetailsOption = (props: any) => (
    <Option {...props}>
        <div className="relative w-10 h-10 mr-3">
            <Image
                className="rounded-full object-fill"
                src={props.data.avatar}
                fill
                alt={props.data.name}
            />
        </div>
        <div className="grow">
            <div className="base2 font-semibold text-n-5 dark:text-n-1">
                {props.data.name}
            </div>
            <div className="caption1 text-n-4/50 dark:text-n-3/50">
                {props.data.email}
            </div>
        </div>
    </Option>
);

const CustomMultiValueRemove = (props: any) => (
    <MultiValueRemove {...props}>
        <Icon
            className="w-4 h-4 fill-inherit transition-transform"
            name="close"
        />
    </MultiValueRemove>
);

type MultiSelectProps = {
    className?: string;
    classMultiSelectGlobal?: string;
    items: any;
    selectedOptions: any;
    setSelectedOptions: any;
};

const MultiSelect = ({
    className,
    classMultiSelectGlobal,
    items,
    selectedOptions,
    setSelectedOptions,
}: MultiSelectProps) => {
    const handleMultiSelectChange = (selectedOptions: any) => {
        setSelectedOptions(selectedOptions);
    };
    console.log(selectedOptions);

    const getOptionLabel = (option: any) => option.name;

    const getOptionValue = (option: any) => option.id;

    const formatOptionLabel = ({ avatar, name }: any) => (
        <div className="flex items-center base2 font-semibold">
            <div className="relative w-6 h-6 mr-2">
                <Image
                    className="rounded-full object-fill"
                    src={avatar}
                    fill
                    alt={name}
                />
            </div>
            <span className="mr-3">{name}</span>
        </div>
    );

    return (
        <div className={`relative ${className}`}>
            <Select
                className={`multiselect ${classMultiSelectGlobal}`}
                classNamePrefix="multiselect"
                value={selectedOptions}
                onChange={handleMultiSelectChange}
                options={items}
                isMulti
                getOptionLabel={getOptionLabel}
                getOptionValue={getOptionValue}
                formatOptionLabel={formatOptionLabel}
                placeholder="Name member"
                noOptionsMessage={() => "No people found"}
                components={{
                    Option: DetailsOption,
                    MultiValueRemove: CustomMultiValueRemove,
                }}
                isClearable={false}
            />
            <Icon
                className={`absolute top-4 left-5 w-5 h-5 pointer-events-none fill-n-4/50 dark:fill-n-4/75 ${
                    selectedOptions.length !== 0 && "hidden"
                }`}
                name="email"
            />
        </div>
    );
};

export default MultiSelect;
