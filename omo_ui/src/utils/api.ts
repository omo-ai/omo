
function buildApiUrl(uri: string) {
    return process.env.API_HOST + uri;
}

export { buildApiUrl };