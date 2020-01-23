## Coop Map Directory Index

### Installation


### Data

Data is presently being managed outside of this repository. A locally-installed development database is periodically dumped, transferred, and imported into the production server.

Local:
```
pg_dump -f scratch/cmdi.sql --clean --if-exists cmdi && bzip2 -9 --force scratch/cmdi.sql
scp scratch/cmdi.sql.bz2 ubuntu@awshost:/home/ubuntu/coop-map-directory-index/scratch
```

Remote:
```
sudo su postgres
bunzip2 scratch/cmdi.sql.bz2
psql -f scratch/cmdi.sql cmdi
exit
```
