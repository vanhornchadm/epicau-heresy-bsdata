import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 configuration for the EpicAU Horus Heresy BSData site.
 * build.sh copies this over the pinned Quartz checkout's own config.
 * See https://quartz.jzhao.xyz/configuration for the options.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "EpicAU Heresy BSData",
    pageTitleSuffix: " · EpicAU Heresy BSData",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "en-US",
    baseUrl: "vanhornchadm.github.io/epicau-heresy-bsdata",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Cinzel",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#faf8f5",
          lightgray: "#e4e0d8",
          gray: "#b5ada0",
          darkgray: "#4a4640",
          dark: "#26231f",
          secondary: "#8c2a1f",
          tertiary: "#a8873a",
          highlight: "rgba(168, 135, 58, 0.15)",
          textHighlight: "#f2d27a88",
        },
        darkMode: {
          light: "#151413",
          lightgray: "#36322d",
          gray: "#6b645a",
          darkgray: "#d6d0c6",
          dark: "#eeeae3",
          secondary: "#d9715f",
          tertiary: "#c9a75a",
          highlight: "rgba(201, 167, 90, 0.15)",
          textHighlight: "#a8873a88",
        },
      },
    },
  },
  plugins: {
    transformers: [
      // Pages are generated on every build, so they carry no meaningful dates
      Plugin.FrontMatter(),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: false,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
