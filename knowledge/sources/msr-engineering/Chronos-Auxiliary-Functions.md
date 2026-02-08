# Scheduled Tasks

## ChronosAutomation
- **Description** - Runs all needed tasks for reservations in the provided instance of Chronos. Can be run in one of two configurations, scheduled task mode or date range mode. I believe this also creates files to be used by the parseReimageQueue script.
- **Trigger:** 1AM Daily, then every 5 minutes for 1 day
- **Command:** `F:\Chronos\gcr-reservations\scripts\Chronos_task_automation.ps1 -ChronosSrvcUri http://gcr-reservations/ChronosWcf.svc?singleWsdl -OutputDir F:\Chronos\gcr-reservations\output -ScheduledTaskName ChronosAutomation`

## parseReimageQueue
- **Description**
This goes through each file in `F:\Chronos\gcr-reservations\scripts\reimageQueue`. Each file represents a host to be reformatted. The script attempts to format the hosts listed there according to the appropriate method. It's my understanding that this is currently only used for Azure assets, and the `$DeployType -eq "IPXE"` and `$DeployType -eq "Altiris"` sections are unused. It will attempt to send an e-mail on image failures.

- **Trigger** - Called by `F:\Chronos\gcr-reservations\scripts\Chronos_PshLib.ps1`
- **Command:** - F:\Chronos\Tasks\puarseReiamgeQueue.bat
  ```powershell
  cd F:\Chronos\gcr-reservations\scripts\
  F:\Chronos\gcr-reservations\scripts\parseReimageQueue.ps1 -ChronosSrvcUri http://gcr-reservations/ChronosWcf.svc?singleWsdl
  ```

## ChronosAutomationTableSync
**Description:** See [Chronos Reservation Sync](/Team-Pages/SES/Service-Management/Services/Chronos-Reservation-Service-\(gcr_reservation\))
- **Trigger** Runs every 15 minutes
- Command:
```powershell
F:\Chronos\Tasks\ChronosReservationTableSync.ps1 -keyvault gcrcmvault -storageaccount gcrchronossync -tablename reservations -usertablename reservationusers -chronosdb ChronosDb  > F:\Chronos\Tasks\ChronosReservationTableSync.log
````
