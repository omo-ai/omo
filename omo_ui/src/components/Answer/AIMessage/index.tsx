import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type AIMessageProps = {
    content: string;
 }
const AIMessage = ({ content }: AIMessageProps) => {
    
    return (
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
        </ReactMarkdown>
    )
}

export default AIMessage;