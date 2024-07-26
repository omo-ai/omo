import { useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Layout from "@/components/Layout";
import Icon from "@/components/Icon";
import Stepper from  "@/components/Stepper"
import useDrivePicker from 'react-google-drive-picker';
import { GDriveFile, FileSelectionGrid } from "@/components/FileSelectionGrid";
import { buildApiUrl } from '@/utils/api';
import { AuthContext } from "@/contexts/AuthContext";
import { getCsrfToken } from "next-auth/react";

const initialSteps = [
    {
        name: 'Connect & Select',
        description: 'Click "Connect to Google Drive" and select documents.',
        href: '#',
        status: 'current',
    },
    { 
        name: 'Review & Confirm',
        description: 'The selected files will be indexed by our AI engine.', 
        href: '#',
        status: 'upcoming',
    },
    { 
        name: 'Start AI Analysis',
        description: "Omo will analyze your documents and make them ready for searching.",
        href: '#',
        status: 'upcoming',
    },
  ]

const ConnectGoogleDrive = ( { setSelectedFiles, handleNext, openPicker, authResponse }: any) => {


    const handleOpenPicker = () => {

        if(process.env.NEXT_PUBLIC_GOOGLE_CLOUD_CLIENT_ID == null 
            || process.env.NEXT_PUBLIC_GOOGLE_CLOUD_API_KEY == null ) {
            throw new Error("Google Drive keys not found");
        }

        openPicker({
            // we can't assign the env vars to variables otherwise `next build` will not
            // populate the env vars. also, if these are null, the build will 
            // fail. to pass the build we set to empty string. if null,
            // the block above should catch it.
            clientId: process.env.NEXT_PUBLIC_GOOGLE_CLOUD_CLIENT_ID || "", 
            developerKey: process.env.NEXT_PUBLIC_GOOGLE_CLOUD_API_KEY || "",
            viewId: "DOCS",
            showUploadView: false,
            showUploadFolders: true,
            supportDrives: true,
            setIncludeFolders: true,
            setSelectFolderEnabled: true,
            multiselect: true,
            // customViews: customViewsArray, // custom view
            callbackFunction: (data: any) => {

                if (data.action === 'cancel') {
                    console.log('User clicked cancel/close button')
                }
                if (data.action === 'picked') {
                    let files: GDriveFile[] = [];

                    data.docs.forEach((doc: any, index: number) => {
                        let file: GDriveFile = {
                            id: doc.id,
                            serviceId: doc.serviceId,
                            name: doc.name,
                            description: doc.description,
                            type: doc.type,
                            mimetype: doc.mimeType,
                            lastEditedUtc: doc.lastEditedUtc,
                            url: doc.url,
                            sizeBytes: doc.sizeBytes,
                        }
                        files.push(file);
                    })
                    setSelectedFiles([
                        ...files
                    ])

                    handleNext();
                }
            }
        })
    }
    return (
        <button className="btn-stroke-light w-full mt-8 md:mt-6"
            onClick={handleOpenPicker}
        >
            Connect to Google Drive
    </button>
    )
}


const GoogleDriveConnectorPage = ({ user }: any) => {
    const router = useRouter();
    const { omoUser, isOmoUserLoading} = useContext(AuthContext);

    const [activeStep, setActiveStep] = useState(0);
    const [steps, setSteps] = useState(initialSteps);
    const [selectedFiles, setSelectedFiles] = useState<GDriveFile[]>([]);
    const [openPicker, authResponse] = useDrivePicker(); 
    const [didSubmit, setDidSubmit] = useState(false);

    const handlePrevious = () => {
        setSteps(steps => {
            const completeStep = steps.map( (step, index) =>
                index === activeStep ? { ...step, status: 'upcoming'}
                : step
            );
            return completeStep;
        } );

        // set the next step to current / in-progress
        setSteps(steps => {
            const nextStepCurrent = steps.map( (step, index) =>
                index === activeStep - 1 ? { ...step, status: 'current'}
                : step
            );
            return nextStepCurrent;
        } );

        setActiveStep((activeStep) => activeStep - 1);
    }
    const handleNext = () => {
        if (activeStep == initialSteps.length -1 ) {
            return; // TODO complete; forward user somewhere
        }
        // set the current step to complete
        setSteps(steps => {
            const completeStep = steps.map( (step, index) =>
                index === activeStep ? { ...step, status: 'complete'}
                : step
            );
            return completeStep;
        } );

        // set the next step to current / in-progress
        setSteps(steps => {
            const nextStepCurrent = steps.map( (step, index) =>
                index === activeStep + 1 ? { ...step, status: 'current'}
                : step
            );
            return nextStepCurrent;
        } );

        setActiveStep((activeStep) => activeStep + 1);

    }
    const submitFiles = async () => {
        const csrfToken = await getCsrfToken();
        const endpoint = buildApiUrl('/v2/googledrive/files');

        const headers = new Headers();
        headers.append("Content-Type", "application/json");
        headers.append("X-XSRF-Token", csrfToken);

        if(authResponse?.access_token) {
            headers.append("X-Google-Authorization", authResponse.access_token)
        }

        if (!isOmoUserLoading) {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: headers,
                credentials: 'include',
                body: JSON.stringify({ "files": selectedFiles})
            }).then((response) => {
                setDidSubmit(true);
                setSteps(steps => {
                    const lastStepComplete = steps.map( (step, index) =>
                        index === steps.length - 1 ? { ...step, status: 'complete'}
                        : step
                    );
                    return lastStepComplete;
                } );
    
            }) 
        }
    }


    return (
        <Layout hideRightSidebar user={user}>
            <div className="p-10 md:pt-5 md:px-6 md:pb-10">
                <button
                    className="hidden absolute top-6 right-6 w-10 h-10 border-2 border-n-4/25 rounded-full text-0 transition-colors hover:border-transparent hover:bg-n-4/25 md:block"
                    onClick={() => router.back()}
                >
                    <Icon className="fill-n-4" name="close" />
                </button>
                <div className="h3 leading-[4rem] md:mb-3 md:h3">
                    Google Drive 
                </div>
                <div className="mb-8 body1 text-n-4 md:mb-6 md:body1S">
                    Connect your Google Drive
                </div>

                <div className="grid grid-cols-3">
                    <div className="py-5 mr-15 sm:px-6 lg:px-8">
                        <Stepper steps={steps} activeStep={activeStep} />
                    </div>
                    <div className="col-span-2 relative">
                        {activeStep === steps.length && <div>All Steps Complete</div>}
                        {activeStep === 0 && <ConnectGoogleDrive setSelectedFiles={setSelectedFiles} handleNext={handleNext} openPicker={openPicker} authResponse={authResponse} /> }
                        {activeStep === 1 && <FileSelectionGrid files={selectedFiles} setSelectedFiles={setSelectedFiles}/>}
                        {activeStep === 2 && didSubmit && <p>Your files are being processed! You can check progress on the Connections page.</p> }
                        {activeStep === 2 && !didSubmit && <p>Next, Omo will analyze your files to make it available for search and chat. Click Start to kick things off!</p> }

                        <div className="absolute right-0 mt-15">
                            {activeStep > 0 
                                ? <button
                                    className="btn btn-large w-30"
                                    onClick={handlePrevious}>Previous</button>
                                : null }
                            { selectedFiles.length > 0 ? (
                                 <button
                                    className="btn-blue btn-large w-30 ml-6"
                                    onClick={didSubmit ? () => router.push('/connectors') : activeStep === steps.length - 1 ? submitFiles : handleNext }>
                                    { didSubmit ? "Finish" : activeStep === steps.length - 1 ? "Start" : "Next"}
                             </button>
                            ) : <></> }
                        </div>
                    </div>

                </div> 

            </div>
        </Layout>
    );
};

export default GoogleDriveConnectorPage;
