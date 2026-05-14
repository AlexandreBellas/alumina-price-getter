/**
 * Last 1-based column index in row 1 that has non-empty content (after trim).
 *
 * @param {GoogleAppsScript.Spreadsheet.Sheet} sheet
 * @returns {number}
 */
function lastUsedColumnInRow1(sheet) {
    const probeTo = Math.max(sheet.getLastColumn(), 1);
    const row = sheet.getRange(1, 1, 1, probeTo).getValues()[0];
    let last = 1;
    for (let i = 0; i < row.length; i++) {
        if (String(row[i] ?? "").trim() !== "") last = i + 1;
    }
    return last;
}

/**
 * Appends one row: date in A, then values under row-1 headers (B onward).
 * Adds missing keys from `prices` as new headers on the right.
 *
 * Sheet.getRange(row, col, numRows, numColumns) — 3rd/4th are sizes, not end indices.
 *
 * @param {Object<string, string>} prices Label -> price string
 */
function processPrices(prices) {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Dados");

    const priceMap = new Map();
    for (const [k, v] of Object.entries(prices)) {
        const key = String(k ?? "").trim();
        if (!key) continue;
        priceMap.set(key, v == null ? "" : String(v));
    }

    // Row 1: one row, width = rightmost used column in row 1
    let lastCol = lastUsedColumnInRow1(sheet);
    let headerRow = sheet.getRange(1, 1, 1, lastCol).getValues()[0];

    if (!headerRow[0] || String(headerRow[0]).trim() === "") {
        sheet.getRange(1, 1).setValue("Data");
        lastCol = lastUsedColumnInRow1(sheet);
        headerRow = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
    }

    const existingLabels = new Set();
    for (let c = 1; c < headerRow.length; c++) {
        const h = String(headerRow[c] ?? "").trim();
        if (h) existingLabels.add(h);
    }

    const newLabels = [];
    for (const k of Object.keys(prices)) {
        const ks = String(k ?? "").trim();
        if (!ks) continue;
        if (!existingLabels.has(ks)) {
            existingLabels.add(ks);
            newLabels.push(ks);
        }
    }

    // One row starting at (1, startCol); width = newLabels.length (NOT an end-column index)
    if (newLabels.length > 0) {
        const startCol = lastCol + 1;
        sheet.getRange(1, startCol, 1, newLabels.length).setValues([newLabels]);
        lastCol = startCol + newLabels.length - 1;
    }

    headerRow = sheet.getRange(1, 1, 1, lastCol).getValues()[0];

    const today = new Date();
    const todayStr = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;

    const newRow = [todayStr];
    for (let c = 1; c < headerRow.length; c++) {
        const label = String(headerRow[c] ?? "").trim();
        newRow.push(label ? (priceMap.get(label)?.replace(",", "")?.replace(".", ",") ?? "") : "");
    }

    sheet.appendRow(newRow);
}
