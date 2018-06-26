# Dj4 Astor Runner:

It's an old folk from [defects4j-repair-runner](https://github.com/tdurieux/defects4j-repair-runner) by [Thomas Durieux](https://github.com/tdurieux) and adapted for running a new version Astor framework by [Matias Martinez](https://github.com/martinezmatias).

## How to use it?

First, edit file [Config.py](https://github.com/martinezmatias/scriptastord4j/blob/master/src/python/core/Config.py) to specify the path to the JVM and the localion of the Defects4J projects.



This runner is designed to run on a [OAR](http://oar.imag.fr/dokuwiki/doku.php) system.

The program ```defects4j-g5k.py``` is used to start the execution on the cluster.
### ```defects4j-g5k.py``` Usage
```bash
usage: defects4j-g5k.py [-h] -projects PROJECTS [PROJECTS ...] -tools TOOLS
                        [TOOLS ...] [-id ID [ID ...]] [--timeout TIMEOUT]
                        [--with-angelic]

Run tools on defect4j with grid5000

optional arguments:
  -h, --help            show this help message and exit
  -projects PROJECTS [PROJECTS ...]
                        Which project (all, math, lang, time, chart)
  -modes MODES [MODES ...]
                        Which mode (jgenprog, jkalo)
  -id ID [ID ...]       Bug id
  --timeout TIMEOUT     Node timeout
  --scope SCOPE      Ingredient scope
  --seed SEED     Random seed
  --parameters     parameters to pass to Astor (format key1:value1:key2:value2:keyn:valuen, where keyi is the name of the parameter (eg., maxGeneration) and valuei is the value (e.g, 100)) 
```

## Example Math-70

```
cd src/python/
python defects4j-g5k.py --timeout 04:30:00 -modes jgenprog  -project Math  -i 70   -seed 0  -scope package -parameters stopfirst:true:maxGeneration:100
```

