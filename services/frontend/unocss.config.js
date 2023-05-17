import { defineConfig, presetAttributify, presetUno } from "unocss";

export default defineConfig({
  exclude: [
    "node_modules",
    ".git",
    ".vscode",
    "build",
    "dist",
    "mock",
    "public",
  ],
  presets: [presetUno(), presetAttributify()],
  shortcuts: [
    ["wh-full", "w-full h-full"],
    ["f-c-c", "flex justify-center items-center"],
    ["flex-col", "flex flex-col"],
    ["absolute-lt", "absolute left-0 top-0"],
    ["absolute-lb", "absolute left-0 bottom-0"],
    ["absolute-rt", "absolute right-0 top-0"],
    ["absolute-rb", "absolute right-0 bottom-0"],
    ["absolute-center", "absolute-lt f-c-c wh-full"],
    ["text-ellipsis", "truncate"],
  ],
  rules: [
    ["line-100", { "line-height": "100%" }],
    [/^bc-(.+)$/, ([, color]) => ({ "border-color": `#${color}` })],
    [
      "card-shadow",
      {
        "box-shadow":
          "0 1px 2px -2px #00000029, 0 3px 6px #0000001f, 0 5px 12px 4px #00000017",
      },
    ],
    [
      "mild-shadow",
      {
        "box-shadow": "4px 4px 11px -6px rgba(34, 60, 80, 0.2)",
      },
    ],
  ],
});
