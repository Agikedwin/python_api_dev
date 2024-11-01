from app import schemas
import pytest
def test_get_all_posts(authorized_client, test_create_post):
   res =  authorized_client.get('/post')

   def validate(post):
      return schemas.PostOut(**post)

   post_map = map(validate, res.json())
   print(post_map)
   post_list = list(post_map)
   assert len(res.json()) == len(test_create_post)
   assert  res.status_code == 200
   assert  post_list[0].Post.id == test_create_post[0].id


def test_unauthorized_user_get_all_posts(client, test_create_post):
   res = client.get("/post")
   assert res.status_code == 401

def test_unauthorized_user_get_one(client, test_create_post):
   res = client.get(f"/post/{test_create_post[0].id}")
   assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_create_post):
   res = authorized_client.get(f"/post/9999")
   assert res.status_code == 404

def test_get_one_post_exist(authorized_client, test_create_post):
   res = authorized_client.get(f"/post/{test_create_post[0].id}")
   post_one = schemas.PostOut(**res.json())
   assert post_one.Post.id == test_create_post[0].id
   assert post_one.Post.content == test_create_post[0].content
   assert post_one.Post.title == test_create_post[0].title

@pytest.mark.parametrize("title, content,published",[
   ("agik test title", "agik test content", True),
   ("agik test title 1", "agik test content 1", False),
   ("agik test title 2", "agik test content 2", True),
])

def test_create_post(authorized_client, test_user,test_create_post,title,content,published):
   res = authorized_client.post("/post", json={
      "title":title, "content":content, "published": published
   })
   created_post = schemas.PostResponse(**res.json())

   assert res.status_code == 201
   assert  created_post.title == title
   assert  created_post.content == content
   assert  created_post.published == published
   assert  created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user):
   res = authorized_client.post("/post", json={
      "title": "some title", "content": "some content","published": 1
   })
   created_post = schemas.PostResponse(**res.json())

   assert res.status_code == 201
   assert created_post.title == "some title"
   assert created_post.content ==  "some content"
   #assert created_post.published == 0
   assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_posts(client,test_user, test_create_post):
   res = client.post("/post", json={
      "title": "some title", "content": "some content", "published": 1
   })
   assert res.status_code == 401

def test_unauthorized_user_delete_posts(client,test_user,test_create_post):
   res = client.delete(f"/post/{test_create_post[0].id}")
   assert res.status_code == 401

def test_delete_posts_success(authorized_client,test_user,test_create_post):
   res = authorized_client.delete(f"/post/{test_create_post[0].id}")
   assert res.status_code == 204

def test_delete_posts_non_exist(authorized_client,test_user,test_create_post):
   res = authorized_client.delete(f"/post/9088")
   assert res.status_code == 404

def test_delete_other_user_posts(authorized_client,test_user,test_create_post):
   res = authorized_client.delete(f"/post/{test_create_post[3].id}")
   assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_create_post):
   data = {
      "title": "some title", "content": "some content","published": 1, "id": test_create_post[0].id
   }
   res = authorized_client.put(f"/post/{test_create_post[0].id}", json=data)
   updated_post = schemas.PostResponse(**res.json())

   assert res.status_code == 200
   assert updated_post.title == data['title']
   assert  updated_post.content == data['content']

def test_update_other_user_posts(authorized_client,test_user,test_user2,test_create_post):
   data = {
      "title": "some title", "content": "some content", "published": 1, "id": test_create_post[3].id
   }
   res = authorized_client.put(f"/post/{test_create_post[3].id}", json=data)
   assert res.status_code == 403

def test_unauthorized_user_update_posts(client,test_user,test_create_post):
   res = client.put(f"/post/{test_create_post[0].id}")
   assert res.status_code == 401

def test_update_posts_non_exist(authorized_client,test_user,test_create_post):
   data = {
      "title": "some title", "content": "some content", "published": 1, "id": test_create_post[3].id
   }
   res = authorized_client.put(f"/post/9088", json=data)
   assert res.status_code == 404