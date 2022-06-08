from app.models.users import User
from app.schemas.users import UserCreate
from app.services.exceptions.users import (
    UserNotFound, InvalidCode, UserLimitSendCode, UserNeedToWaitForNextVerify)

from app.utils.mail import send_new_account_email


class RegisterServices:
    def __init__(self, repository, user_services):
        self.repository = repository
        self.user_services = user_services

    def register(self, body: UserCreate) -> User:
        user = self.user_services.create(body=body)
        self.send_code(user_id=user.id)

    def verify_code_for_registers(self, *, user_id,  code_str):
        user = self.repository.get(user_id)
        if not user:
            raise UserNotFound
        code = self.repository.get_code_of_user(user=user)

        if self.repository.check_time_fail(code=code):
            raise UserNeedToWaitForNextVerify

        if self.repository.check_limit_fails(code=code):
            raise UserNeedToWaitForNextVerify

        if code.body != code_str:
            self.repository.update_code_fails(code=code)
            raise InvalidCode

        self.repository.active_user(user=user)

    def send_code(self, *, user_id):

        user = self.repository.get(user_id)
        if not user:
            raise UserNotFound

        code = self.repository.get_code_of_user(user=user)

        if not code:
            code = self.repository.create_code(user=user)

        code = self.repository.update_code(code=code)

        if self.repository.check_time_send(code=code):
            raise UserLimitSendCode

        send_new_account_email(email_to=user.email, signup_code=code.body)

        self.repository.set_time_send(code=code)
