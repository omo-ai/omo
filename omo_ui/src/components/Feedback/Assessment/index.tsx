import Item from "./Item";

const items = [
    {
        id: "0",
        number: 28,
        incorrect: "which",
        correct: "whose",
    },
    {
        id: "1",
        number: 42,
        incorrect: "getting annoyed",
        correct: "showing agreement",
    },
    {
        id: "2",
        number: 56,
        incorrect: "public",
        correct: "unknown",
    },
    {
        id: "3",
        number: 60,
        incorrect: "Newyork",
        correct: "Sydney",
    },
    {
        id: "4",
        number: 80,
        incorrect: "careless",
        correct: "reliable",
    },
];

type AssessmentProps = {};

const Assessment = ({}: AssessmentProps) => (
    <div className="py-3">
        <div className="table w-full">
            <div className="table-row caption1 text-n-4 md:flex">
                <div className="table-cell pl-5 py-2 md:hidden">#</div>
                <div className="table-cell pl-5 py-2 md:w-1/2 md:pr-2">
                    Incorrect answer (5)
                </div>
                <div className="table-cell pl-5 py-2 md:w-1/2 md:pl-0 md:pr-5">
                    Correct answer
                </div>
                <div className="table-cell pl-5 pr-5 py-2 text-center md:hidden">
                    How
                </div>
            </div>
            {items.map((x) => (
                <Item item={x} key={x.id} />
            ))}
        </div>
    </div>
);

export default Assessment;
