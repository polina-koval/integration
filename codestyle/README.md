# Python code static analysis check

## Проверка кода

In the root directory of the project:
```
make devcodestylecheck <subdirectory>
```
OR
```
docker build -t codestyle . && \
docker run -ti --rm --volume "<path>:/code" --user "${CURRENT_USER_ID}:${CURRENT_GROUP_ID}" codestyle format <subdirectory>
```

## Code formatting

Project's rott directory:
```
make devcodestyleformat <subdirectory>
```
OR
```
docker build -t codestyle . && \
docker run -ti --rm --volume "<path>:/code" --user "${CURRENT_USER_ID}:${CURRENT_GROUP_ID}" codestyle format <subdirectory>
```

## Settings

Following files will be looked for in the given directory: `.black` или `.flake8`.

If there are no the files, then it will be looked in parent directories recursively.
