import functools

from flask import (
    Blueprint, g, request, url_for, make_response
)

from bookman.db_pg import get_db

bp = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')

# GET /api/v1/bookmarks: Get a list of bookmarks
# POST /api/v1/bookmarks: Create a new bookmark
@bp.route('', methods=['GET', 'POST'])
def bm_new_lst():
  if request.method == 'POST':
    # create a new bookmark
    data = request.get_json()
    name = data["name"]
    url = data["url"]
    # TODO: check if url correct
    folder_id = data.get("folder_id", 0)
    try:
      with get_db() as db:
        with db.cursor() as cur:
          # DONE: enforced by constraint
          # check if bookmark with same name exists in this folder
          # cur.execute(
          #  "SELECT id FROM bookmarks WHERE folder_id = %s AND name = %s",
          #  (folder_id, name,),
          #)
          #res = cur.fetchone()
          #if res is not None:
            # There is not a big sense to have 2 bokmarks with same name in same folder
          #  return {'error': 'Bookmark exists'}, 400
          # insert new bookmark
          cur.execute(
            "INSERT INTO bookmarks (name, url, folder_id) VALUES (%s, %s, %s) RETURNING id",
            (name, url, folder_id),
          )
          bm_id = cur.fetchone()[0]
    except db.IntegrityError as e:
      msg = e.pgerror
      if "bookmarks_folder_id_name" in msg:
        # Duplicated name
        return {'error': 'Bookmark %s exists in folder %i' % (name, folder_id)}, 400
      return {'error': 'Folder %i does not exist' % folder_id}, 400
    except db.Error as e:
      return {'error': e.pgerror}, 400
    # need return location of new object
    bm_url = url_for(".bm_upd_del", bookmark_id = bm_id)
    response = make_response(bm_url, 201)
    response.headers["Location"] = bm_url
    return response
    
  # Get list of bookmarks
  with get_db() as db:
    with db.cursor() as cur:
      # use row_to_json function here to get
      # results as JSON
      cur.execute(
        """
          WITH bkmks AS (
            SELECT b.*, f.name AS folder 
            FROM bookmarks b
            INNER JOIN folders f
              ON b.folder_id = f.id
          )
          SELECT row_to_json(b) FROM bkmks b
        """
      )
      bookmarks = cur.fetchall()
  return {"bookmarks": bookmarks}, 200
  
# PUT /api/v1/bookmarks/:id: Update a bookmark
# DELETE /api/v1/bookmarks/:id: Delete a bookmark
# There should be a method to GET single bookmark
@bp.route('/<int:bookmark_id>', methods=['PUT', 'DELETE', 'GET'])
def bm_upd_del(bookmark_id):
  if request.method == "DELETE":
    # delete a bookmark
    try:
      with get_db() as db:
        with db.cursor() as cur:
          cur.execute(
            "DELETE FROM bookmarks WHERE id = %s",
            (bookmark_id,),
          )
    except db.Error as e:
      return {'error': e.pgerror}, 400
    return "", 204
  
  elif request.method == "GET":
    # return bookmark
    with get_db() as db:
      with db.cursor() as cur:
        # use row_to_json function here to get
        # results as JSON
        cur.execute(
          """
            WITH bkmks AS (
              SELECT b.*, f.name AS folder 
              FROM bookmarks b
              INNER JOIN folders f
                ON b.folder_id = f.id
              WHERE b.id = %s
            )
            SELECT row_to_json(b) FROM bkmks b
          """,
          (bookmark_id,),
        )
        bookmark = cur.fetchone()
    if bookmark is None:
      return {'error': 'Bookmark %i not found' % bookmark_id}, 404
    return {'bookmarks': bookmark}, 200
  
  # update a bookmark  
  data = request.get_json()
  name = data.get("name")
  if name and len(name) == 0:
    # Not allow empty name
    return {"error": "Bad bookmark name"}, 400
  url = data.get("url")
  # TODO: check if url correct
  try:
    with get_db() as db:
      with db.cursor() as cur:
        # change name
        if name:
          cur.execute(
            "UPDATE bookmarks SET name = %s, updated = now() WHERE id = %s",
            (name, bookmark_id),
          )
        # change url
        if url:
          cur.execute(
            "UPDATE bookmarks SET url = %s, updated = now() WHERE id = %s",
            (url, bookmark_id),
          )
  except db.IntegrityError as e:
    # Duplicated bookmark
    return {'error': 'Bookmark %s exists in this folder' % name}, 400
  except db.Error as e:
    return {'error': e.pgerror}, 400
  return "", 204
  
# GET /api/v1/bookmarks/folders/:id: Get a list of bookmarks for a folder
@bp.route('/folders/<int:folder_id>', methods=['GET'])
def bm_fld_list(folder_id):
  with get_db() as db:
    with db.cursor() as cur:
      # use row_to_json function here to get
      # results as JSON
      cur.execute(
        """
          WITH bkmks AS (
            SELECT b.*, f.name AS folder 
            FROM bookmarks b
            INNER JOIN folders f
              ON b.folder_id = f.id
            WHERE b.folder_id = %s
          )
          SELECT row_to_json(b) FROM bkmks b
        """,
        (folder_id,),
      )
      bookmarks = cur.fetchall()
  return {"bookmarks": bookmarks}, 200
