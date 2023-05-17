export function getImageURL(url) {
  let src = new URL(url, import.meta.env.ARTMOVE_API_URL).href;
  return src;
}
