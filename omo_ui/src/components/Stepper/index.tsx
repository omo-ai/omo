import { CheckIcon } from '@heroicons/react/20/solid'
import { classNames } from '@/utils/common';

type Step = {
    name: string;
    description: string;
    href: string;
    status: string;
}

type StepperProps = {
    steps: Step[];
    activeStep: number;
}

type StepperIconProps = {
    status: string
}

const StepperIcon = ({status}: StepperIconProps) => {
    const outerRoundedIconStyle:any = {
        'upcoming': 'border-2 border-gray-300 bg-white group-hover:border-gray-400',
        'complete': 'bg-indigo-600 group-hover:bg-indigo-800',
        'current': 'border-2 border-indigo-600 bg-white',
    }
    const innerRoundedIconStyle:any = {
        'upcoming': 'h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300',
        'current': 'h-2.5 w-2.5 rounded-full bg-indigo-600',
    }

    return (
        <span className="flex h-9 items-center" aria-hidden="true">
            <span className={classNames("relative z-10 flex h-8 w-8 items-center justify-center rounded-full", outerRoundedIconStyle[status])}>
                {status === 'complete' ?  <CheckIcon className="h-5 w-5 text-white" aria-hidden="true" />
                    : <span className={classNames(innerRoundedIconStyle[status])} />
                }
            </span>
        </span>
    )
}

const Stepper = ({ steps, activeStep }: StepperProps) => {
    const verticalGuideStyle:any = {
        'upcoming': 'absolute left-4 top-4 -ml-px mt-0.5 h-full w-0.5 bg-gray-300',
        'complete': 'absolute left-4 top-4 -ml-px mt-0.5 h-full w-0.5 bg-indigo-600',
        'current': 'absolute left-4 top-4 -ml-px mt-0.5 h-full w-0.5 bg-gray-300',
    }
    const textStyle: any ={
        'upcoming': 'text-md font-medium text-gray-800 dark:text-slate-200',
        'complete': 'text-md font-medium',
        'current': 'text-md font-medium text-indigo-800 dark:text-indigo-400',
    }
    return (
        <>
        <nav aria-label="Progress">
        <ol role="list" className="overflow-hidden">

            {steps.map((step, stepIdx) => (
            <li key={step.name} className={classNames(stepIdx !== steps.length - 1 ? 'pb-10' : '', 'relative')}>
                { stepIdx !== steps.length -1 ? 
                    <div className={classNames(verticalGuideStyle[step.status])} aria-hidden="true" /> : null
                }
                <a href={step.href} className="group relative flex items-start">
                    <StepperIcon status={step.status}/>
                    <span className="ml-4 flex min-w-0 flex-col">
                        <span className={classNames(textStyle[step.status])}>{step.name}</span>
                        <span className="text-sm text-grey dark:text-slate-200">{step.description}</span>
                    </span>
                </a> 
            </li>
            ))}
        </ol>
        </nav>
        </>
    )
}

export default Stepper;