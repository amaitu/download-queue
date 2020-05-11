# download-queue

WIP

A simple queue worker that downloads files to a target directory. Optimised for downloading large files.

Looks for a SQLite database in which jobs can be stored (jobs table). Has endpoints to create a new job, get a list of all jobs, and get the latest job. Queue will get latest job, download, then move to next.
