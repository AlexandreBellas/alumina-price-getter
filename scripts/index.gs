const AUTH_TOKEN = "<replace-with-any-value-of-your-taste>";

/**
 * @inheritdoc
 *
 * @returns void
 */
function doPost(e) {
    // Obtain POST contents
    const rawPostContents = e.postData.contents;

    // Decode POST request
    let postContents = null;
    try {
        postContents = JSON.parse(rawPostContents);
    } catch {
        console.error("422 Unprocessable entity: payload not JSON parseable");
        return;
    }

    // Validate request
    if (typeof postContents !== "object" || postContents === null) {
        console.error("422 Unprocessable entity: invalid payload");
        return;
    }
    if (!("token" in postContents)) {
        console.error("401 Unauthorized: missing token");
        return;
    }
    if (postContents.token !== AUTH_TOKEN) {
        console.error("403 Forbidden: permission denied");
        return;
    }
    if (!("prices" in postContents)) {
        console.error("422 Unprocessable entity: missing prices");
        return;
    }
    if (typeof postContents.prices !== "object" || postContents.prices === null) {
        console.error("422 Unprocessable entity: incorrect prices type");
        return;
    }

    // Process the prices
    processPrices(postContents.prices);
}
