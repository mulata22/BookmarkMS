CREATE TABLE "bookmarks" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "name" character varying(255) NOT NULL,
  "url" character varying(255) NOT NULL,
  "folder_id" integer NOT NULL DEFAULT 0,
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE "folders" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "name" character varying(255) NOT NULL,
  "description" character varying(255) NULL,
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO "folders" ("id", "name", "description", "created", "updated")
VALUES ('0', 'root', 'root folder', now(), now());
ALTER TABLE "bookmarks"
ADD FOREIGN KEY ("folder_id") REFERENCES "folders" ("id");


