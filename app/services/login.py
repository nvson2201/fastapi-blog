# TODO có thể tách tiếp từ services.user ra cho đỡ dài
# nên tách tiếp services.user ra services.authenticate và services.login
# có cần để một số hàm ở services.user hay services.login là method function?
# như vậy chỉ cần gọi hàm cần dùng chứ không cần khởi tạo object?


from typing import Union
from sqlalchemy.orm import Session
from app.db.repositories_cache.users import UserRedisRepository
from app.db.repositories.users import UserRepository


class LoginServices:

    def __init__(self, db: Session,
                 crud_engine: Union[UserRedisRepository, UserRepository]):
        self.db = db
        self.crud_engine = crud_engine
