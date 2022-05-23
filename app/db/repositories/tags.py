from typing import List


from app.models.tags import Tag
from app.db.repositories.base import BaseRepository
from app.db import db


class TagRepository(BaseRepository):
    def get_all_tags(self):
        tags_in_db = self.db.query(self.model).all()
        tags_list = set(item.tag for item in tags_in_db)
        return list(tags_list)

    def create_tags_that_dont_exist(
            self, *, body: List[str]
    ) -> None:
        tags = []
        for tag in body:
            body_dict = {"tag": tag}
            tag = self.model(**body_dict)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
            tags.append(tag)
        return tags


tags = TagRepository(Tag, db)
