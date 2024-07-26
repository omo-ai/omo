type ChatEmptyProps = {};

const ChatEmpty = ({}: ChatEmptyProps) => (
    <>
        {Array.from(Array(4).keys()).map((x) => (
            <div className="mb-2 last:mb-0" key={x}>
                <div className="flex p-3">
                    <div className="w-5.5 h-5.5 mt-0.25 ml-0.25 mr-3 bg-n-3 rounded-md dark:bg-n-5"></div>
                    <div className="grow">
                        <div className="w-40 h-3 mt-1.5 rounded-sm bg-n-3 dark:bg-n-5"></div>
                        <div className="h-3 mt-3.5 rounded-sm bg-n-3 dark:bg-n-5"></div>
                        {x === 2 && (
                            <div className="h-34 mt-3 rounded-2xl bg-n-3 dark:bg-n-5"></div>
                        )}
                        <div className="flex justify-between items-center mt-3">
                            <div className="w-7 h-7 rounded-full bg-n-3 dark:bg-n-5"></div>
                            <div className="w-12 h-2 rounded-sm bg-n-3 dark:bg-n-5"></div>
                        </div>
                    </div>
                </div>
            </div>
        ))}
    </>
);

export default ChatEmpty;
