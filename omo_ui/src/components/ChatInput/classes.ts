import { nanoid } from "nanoid";

export class Chat {
    id: number;         // the primary key
    chat_id: string;    // the unique alphanumeric string for the chat
    title: string;
    updated_at?: string;
    messages?: ChatMessage[];

    constructor(title: string, updated_at: string, messages: ChatMessage[]) {
        this.id = 0;
        this.chat_id = '';
        this.title = title;
        this.updated_at = updated_at;
        this.messages = messages;
    }

}

export class ChatMessage {
    id: string; // messages are stored as JSON in the db, so no pk
    content: string;
    role: string;
    isLoading: boolean;
    sources: any[];

    constructor(content: string,
                role: string,
                isLoading?: boolean,
                sources?: any[]) {

        this.id = 'msg:' + nanoid();
        this.content = content;
        this.role = role;
        this.isLoading = isLoading || false;
        this.sources = sources || [];
    }
}
