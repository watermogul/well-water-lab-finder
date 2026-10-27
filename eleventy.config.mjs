import { EleventyHtmlBasePlugin } from "@11ty/eleventy";

// PATH_PREFIX: "/" for a custom domain or user site; "/well-water-lab-finder/" for the GitHub project page.
const pathPrefix = process.env.PATH_PREFIX || "/";

export default function (eleventyConfig) {
  eleventyConfig.addPlugin(EleventyHtmlBasePlugin); // rewrites root-absolute href/src to include pathPrefix
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  eleventyConfig.addFilter("phoneHref", (p) => "tel:+1" + String(p).replace(/\D/g, "").slice(0, 10));
  eleventyConfig.addFilter("json", (v) => JSON.stringify(v));
  eleventyConfig.addFilter("groupFilter", (labs, g) => labs.filter((l) => l.group === g));
  // JSON-LD: only fields that appear verbatim in the source data (name, address text, phone).
  eleventyConfig.addFilter("stateLd", (d, s, base, url) =>
    JSON.stringify({
      "@context": "https://schema.org",
      "@type": "ItemList",
      name: s.title,
      url: base + url,
      numberOfItems: d.labs.filter((l) => l.group === "main").length,
      itemListElement: d.labs
        .filter((l) => l.group === "main")
        .map((l, i) => ({
          "@type": "ListItem",
          position: i + 1,
          item: { "@type": "LocalBusiness", name: l.name, address: l.address, ...(l.phone ? { telephone: l.phone } : {}), ...(l.website ? { url: l.website } : {}) },
        })),
    }));
  eleventyConfig.addFilter("articleLd", (title, desc, base, url, modified) =>
    JSON.stringify({ "@context": "https://schema.org", "@type": "Article", headline: title, description: desc, mainEntityOfPage: base + url, dateModified: modified, author: { "@type": "Organization", name: "Well Water Lab Finder" } }));
  return {
    pathPrefix,
    dir: { input: "src", output: "_site", includes: "_includes", data: "_data" },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
  };
}
