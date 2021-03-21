# MyAnimeList.net Chart Maker

This repository contains 2 scripts.

1. Chart generation script
2. CSS minification script

## Chart Generation Script

This script generates charts based on the existing anime lists and manga lists, works on both exported XML files and JSON data retrieved from the API.

### API

Replace the `{username}` part in the URL with your MyAnimeList.net username. The API URL is as follows.

```
GET https://myanimelist.net/animelist/{username}/load.json?status=7&offset=0
```

## CSS Minification Script

This script makes use of the existing API to minify the CSS. The API URL is as follows.

```
POST https://cssminifier.com/raw

{
    "input": "CSS text here"
}
```
