## Coop Map Directory Index


```
heroku buildpacks:set https://github.com/cyberdelia/heroku-geo-buildpack.git
```


```
heroku pg:reset --confirm secret-ridge-11170
heroku pg:push cmdi postgresql-closed-15703 --app secret-ridge-11170
```

```
pg_dump -f scratch/cmdi.sql --clean --if-exists cmdi && bzip2 -9 --force scratch/cmdi.sql
```
