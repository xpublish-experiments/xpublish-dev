# Xpublish-dev

And example development environment for Xpublish and it's plugins using git submodules (the magic incantation to add a new submodule is `git submodule add https://github.com/noaaroland/xpublish_example.git xpublish_example`).

It uses https://pixi.sh/latest/ to manage dependencies.

After cloning the project, you must update the git submodules:

```
git submodule update --init
```

To run a test server, try `pixi run demo` which will launch `app/main.py`,
with a selection of plugins and datasets.

Each plugin can be hacked on individually and be on it's own branch.

Additional plugins can be added to the `[pypi-dependencies]` table in `pixi.toml`,
in similar patterns to the existing ones.
