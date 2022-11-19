# Bookmark Management System
My python assignment project
This is my first assignment given to me from Integrify

## Current state of the project
Bookman application built using flask framework. It implements following REST API methods:
* GET /api/v1/bookmarks: Get a list of bookmarks
* GET /api/v1/bookmarks/folders/:id: Get a list of bookmarks for a folder
* POST /api/v1/bookmarks: Create a new bookmark
* GET /api/v1/bookmarks/:id: Get a single bookmark
* PUT /api/v1/bookmarks/:id: Update a bookmark
* DELETE /api/v1/bookmarks/:id: Delete a bookmark

####
* GET /api/v1/folders: Get a list of folders
* POST /api/v1/folders: Create a new folder
* GET /api/v1/folders/:id: Get a single folder
* PUT /api/v1/folders/:id: Update a folder
* DELETE /api/v1/folders/:id: Delete a folder

There is predefined root folder you can not modify nor delete by API. It has ID 0 and empty name.
DB has 2 constraints for bookmarks table:
1. FOREIGN KEY ("folder_id") REFERENCES "folders" ("id") This prevents creation of bookmark in non-existent folder and deletion of non-empty folder.
2. CONSTRAINT "bookmarks_folder_id_name" UNIQUE ("folder_id", "name") This prevents creation of 2 bookmarks with same name in one folder.
And UNIQUE constraint for folders.name prevents creation of 2 folders with same name.

## Running
Just fire
```
docker-compose up -d
```
in project dir. There 3 containers will be run:
1. PostgreSQL DB container. Database will be initialized by postgresql/docker-entrypoint-initdb.d/schema-pg.sql script. **Database is not persistent!** To make it persistent bind host folder to `/var/lib/postgresql/data`.
2. adminer conatiner to explore DB content. You can open http://localhost:8080 for adminer web UI.
3. bookman application container. For the moment it runs with flask built-in http server. It is available on http://localhost:5000

## Testing
For the moment you can test it using curl:
```
curl -H "Content-Type: application/json" -X POST -d "{\"name\":\"Test folder 1\", \"description\":\"1st test folder\"}" -D - localhost:5000/api/v1/folders
curl -H "Content-Type: application/json" -X GET -D - localhost:5000/api/v1/folders
curl -H "Content-Type: application/json" -X PUT -d "{\"name\":\"Test folder 2\", \"description\":\"2nd test folder\"}" -D - localhost:5000/api/v1/folders/folder_id
curl -H "Content-Type: application/json" -X GET -D - localhost:5000/api/v1/folders
curl -H "Content-Type: application/json" -X DELETE -D - localhost:5000/api/v1/folders/folder_id
curl -H "Content-Type: application/json" -X GET -D - localhost:5000/api/v1/folders
```
Replace folder_id with real id of folder created. Same is for bookmarks.
```
curl -H "Content-Type: application/json" -X POST -d "{\"name\":\"Bookman app\", \"url\":\"http://localhost:5000\"}" -D - localhost:5000/api/v1/bookmarks
curl -H "Content-Type: application/json" -X GET -D - localhost:5000/api/v1/bookmarks/folders/0
curl -H "Content-Type: application/json" -X GET -D - localhost:5000/api/v1/bookmarks
curl -H "Content-Type: application/json" -X PUT -d "{\"name\":\"The bookman app\"}" -D - localhost:5000/api/v1/bookmarks/bookmark_id
curl -H "Content-Type: application/json" -X GET -D - localhost:5000/api/v1/bookmarks
curl -H "Content-Type: application/json" -X DELETE -D - localhost:5000/api/v1/bookmarks/bookamrk_id
curl -H "Content-Type: application/json" -X GET -D - localhost:5000/api/v1/bookmarks
```
Replace bookmark_id with actual id.

## TODO
* Cover project with unit tests
* Migrate to WSGI (uWSGI?)
* Make it configurable by env variables
* Use secrets for password
* Validate URL format
* Better error processing
* Optimizations
