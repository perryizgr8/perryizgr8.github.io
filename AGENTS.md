# AGENTS.md

## What this is

A personal Jekyll blog deployed to GitHub Pages at `blog.perryizgr8.com`.

## Running locally

```sh
bundle exec jekyll serve
```

Always use `bundle exec` — the Gemfile pins Jekyll 4.1.1 and minima 2.5.

Changes to `_config.yml` are **not** hot-reloaded; restart the server after editing it.

## Creating posts

Drop a file in `_posts/` named `YYYY-MM-DD-slug.markdown` with the standard Jekyll front matter. No scaffold script exists.

## Layout / theme

Uses the `minima` theme. Override theme files by placing同名 files in `_includes/` or `_layouts/` (e.g., the custom `_includes/footer.html` already does this).

## Windows quirks

The `Gemfile` includes `wdm` and `tzinfo-data` for Windows file watching and timezone support. Don't remove these gems.