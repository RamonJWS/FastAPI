from fastapi import APIRouter

# prefix will componentize all endpoints /blog into this file.
# we can use the blog tags for easy swagger documentation and identification.
router = APIRouter(prefix="/blog", tags=["blog"])

"""
Routers are a way to structure our API into different files and components.
Split operations into multiple files and components.
e.g. refactoring.

- share operations into multiple files.
- share prefix between multiple operations.
- share tags.
"""

@router.get("/")
def doesnt_matter_for_this_example():
    pass
