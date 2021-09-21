import requests

# TOKEN = "aebc9cd86f70cab175401ecdc280ae36016dd129"
JWT_TOKEN = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6InVzZXIyIiwiZXhwIjoxNjMyMDUyNjQzLCJlbWFpbCI6IiJ9."  # payload
    "JrWa7W_vCn7euUelPe55UlzYRgO2b-vGeijTAbUgg2Y"
)
# ,를 쓰게 되면 튜플이 되므로 튜플 쓰면 안됨


headers = {
    # "Authorization": f"Token {TOKEN}",
    "Authorization": f"JWT {JWT_TOKEN}",
}

res = requests.get("http://localhost:8000/post/5/", headers=headers)
print(res.json())
