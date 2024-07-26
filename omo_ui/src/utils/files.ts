let base_path = '/images/docIcons/';

var mimetypeMappings: any = {
    "application/pdf": {
        "bgColor": "bg-red-600",
        "icon": base_path + "pdf.svg",
    },
    // Word documents
    "application/msword": {
        "bgColor": "bg-indigo-400",
        "icon": base_path + "doc.svg",
    },
    "application/vnd.google-apps.document": {
        "bgColor": "bg-indigo-600",
        "icon": base_path + "doc.svg",
    },
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "bgColor": "bg-indigo-600",
        "icon": base_path + "doc.svg",
    },
    // Powerpoint docs
    "application/vnd.ms-powerpoint": {
        "bgColor": "bg-red-600",
        "icon": base_path + "ppt.svg",
    },
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": {
        "bgColor": "bg-red-600",
        "icon": base_path + "ppt.svg",
    },
    // Excel
    "application/vnd.ms-excel": {
        "bgColor": "bg-green-600",
        "icon": base_path + "xls.svg",
    },
    "application/vnd.google-apps.spreadsheet": {
        "bgColor": "bg-green-600",
        "icon": base_path + "xls.svg",
    },
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
        "bgColor": "bg-green-600",
        "icon": base_path + "xls.svg",
    },
    // csv
    "text/csv": {
        "bgColor": "bg-gray-600",
        "icon": base_path + "csv.svg",
    },
    // default
    "default": {
        "bgColor": "bg-indigo-600",
        "icon": base_path + "doc.svg",
    }

}

export function bgColorForMimeType(mimetype: string) {
    try {
        const color = mimetypeMappings[mimetype]['bgColor'];
        return color;
    }
    catch (e) {
        const color = mimetypeMappings['default']['bgColor'];
        return color;
    }
}

export function iconForMimeType(mimetype: string) {
    try {
        const icon = mimetypeMappings[mimetype]['icon'];
        return icon;
    }
    catch (e) {
        const icon = mimetypeMappings['default']['icon'];
        return icon ; 
    }
}