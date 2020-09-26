# code regulator ver 0.3 beta
Light code management software.
Do not publish server to the web.

## Features
- Schedule management.
- Task scheduler.
- Parallel processing task with subprocess.
- Code management from browser and command.
- logger.
- sleep mode.

## Requirements
- redis server
- redis-py lib
- websockets lib

## How to use SCR
- 1, setting redis connection to SCR/config.py. 
- 2, your codes put on SCR/code/[folder]/[codename]
- 3, run scr_start.py
- 4, setting schedule and task from browser.(localhost:5015)

## scrctl command
you can setting schedule and task from command.

### Add task
run SCR/code/test/testcode.py  
```$ python scrctl task add -path test/testcode.py```

### Add schedule
setting schedule every 5 minutes.  
```$ python scrctl task add -path test/testschedule.py -sec 300```

delete this.  
```$ python scrctl task add -path test/testschedule.py -sec 300 -c delete_schedule```
