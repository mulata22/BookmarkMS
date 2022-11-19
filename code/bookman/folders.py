import functools

from flask import (
    Blueprint, g, request, make_response, url_for
)

from bookman.db_pg import get_db

bp = Blueprint('folders', __name__, url_prefix='/api/v1/folders')

# GET /api/v1/folders: Get a list of folders
# POST /api/v1/folders: Create a new folder
@bp.route('', methods=['GET', 'POST'])
def fld_new_lst():
  if request.method == 'POST':
    # create a new folder
    data = request.get_json()
    name = data["name"]
    if len(name) == 0:
      # Not allow empty name
      return {"error": "Bad folder name"}, 400
    description = data.get("description", "")
    try:
      with get_db() as db:
        with db.cursor() as cur:
          # insert new folder
          cur.execute(
            "INSERT INTO folders (name, description) VALUES (%s, %s) RETURNING id",
            (name, description),
          )
          fld_id = cur.fetchone()[0]
    except db.IntegrityError:
      # it means folder with this name already exists
      return {"error": "Folder %s exists" % name}, 400
    except db.Error as e:
      return {'error': e.pgerror}, 400
    # need return location of new object
    fld_url = url_for(".fld_upd_del", folder_id = fld_id)
    response = make_response(fld_url, 201)
    response.headers["Location"] = fld_url
    return response
  
  # Get list of folders  
  with get_db() as db:
    with db.cursor() as cur:
      # use row_to_json function here to get
      # results as JSON
      cur.execute(
        """
          WITH fldrs AS (
            SELECT *
            FROM folders
          )
          SELECT row_to_json(f) FROM fldrs f
        """
      )
      folders = cur.fetchall()
  return {"folders": folders}

# PUT /api/v1/folders/:id: Update a folder
# DELETE /api/v1/folders/:id: Delete a folder
# There should be a method to GET single folder
@bp.route('/<int:folder_id>', methods=['PUT', 'DELETE', 'GET'])
def fld_upd_del(folder_id):
  if request.method == 'GET':
    # return folder
    with get_db() as db:
      with db.cursor() as cur:
        # use row_to_json function here to get
        # results as JSON
        cur.execute(
          """
            WITH fldrs AS (
              SELECT *
              FROM folders
              WHERE id = %s
            )
            SELECT row_to_json(f) FROM fldrs f
          """,
          (folder_id,),
        )
        folder = cur.fetchone()
    if folder is None:
      return {'error': 'Folder %i not found' % folder_id}, 404
    return {'folders': folder}, 200
    
  if folder_id == 0:
    # you can not change or delete root folder
    return {"error": "Bad folder ID"}, 400
  if request.method == "DELETE":
    # delete a folder
    try:
      with get_db() as db:
        with db.cursor() as cur:
          cur.execute(
            "DELETE FROM folders WHERE id = %s",
            (folder_id,),
          )
    except db.IntegrityError:
      # error reason most likely is FK constraint
      return {"error": "Folder not empty"}, 400
    except db.Error as e:
      return {'error': e.pgerror}, 400
    return "", 204
  
  # update a folder  
  data = request.get_json()
  name = data.get("name")
  if name and len(name) == 0:
    # Not allow empty name
    return {"error": "Bad folder name"}, 400
  description = data.get("description")
  try:
    with get_db() as db:
      with db.cursor() as cur:
        # change name
        if name:
          cur.execute(
            "UPDATE folders SET name = %s, updated = now() WHERE id = %s",
            (name, folder_id),
          )
        # change description
        if description:
          cur.execute(
            "UPDATE folders SET description = %s, updated = now() WHERE id = %s",
            (description, folder_id),
          )
  except db.IntegrityError:
    # it means folder with this name already exists
    return {"error": "Folder %s exists" % name}, 400
  except db.Error as e:
    return {'error': e.pgerror}, 400
  return "", 204
 