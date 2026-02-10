# turbine-performance-analysis
Python project for public wind turbine performance analysis

## Contributing
To start making changes fork the repository or make a new branch from `main`.

The development environment should be created and managed using [uv](https://docs.astral.sh/uv/). To create the environment:
```shell
uv sync --extra dev
```
To run the formatting, linting and testing:
```shell
uv run poe all
```
Or simply
```shell
poe all
```
if you have activated the virtual environment.