from typing import List

from app.models.tags import Tag
from app.db.repositories.base import BaseRepository


class TagRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(Tag, db)

    def get_all_tags(self) -> List[str]:
        tags_in_db = self.db.query(Tag).all()
        tags_list = set(item.tag for item in tags_in_db)
        return list(tags_list)

    def create_tags_that_dont_exist(
            self, *, body: List[str]
    ) -> None:
        for tag in body:
            tag_in_db = self.db.query(Tag).filter(Tag.tag == tag).first()
            if tag_in_db:
                continue
            body_dict = {"tag": tag}
            tag = Tag(**body_dict)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
