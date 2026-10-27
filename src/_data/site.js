import fs from "node:fs";
const base = JSON.parse(fs.readFileSync(new URL("./site.base.json", import.meta.url)));
export default { ...base, url: (process.env.SITE_URL || base.url).replace(/\/$/, "") };
