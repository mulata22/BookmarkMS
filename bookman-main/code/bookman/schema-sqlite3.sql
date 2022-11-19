DROP TABLE IF EXISTS bookmarks;
DROP TABLE IF EXISTS folders;

CREATE TABLE "folders" (
  "id" integer PRIMARY KEY AUTOINCREMENT,
  "name" TEXT UNIQUE NOT NULL,
  "description" TEXT NULL,
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "bookmarks" (
  "id" integer PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL,
  "url" TEXT NOT NULL,
  "folder_id" integer NOT NULL DEFAULT 0,
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY ("folder_id") REFERENCES "folders" ("id")
);

INSERT INTO "folders" ("id", "name", "description")
VALUES ('0', 'root', 'root folder');



