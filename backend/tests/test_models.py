from api.models import User, UserRole, db


class TestUserModel:
    def test_create_user(self, app, db):
        with app.app_context():
            user = User(
                email="unit@test.com",
                role=UserRole.citizen,
                phone="1111111111",
                firstname="Unit",
                lastname="Test",
                address="456 Unit Ave",
            )
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()
            assert user.id is not None
            assert user.email == "unit@test.com"
            assert user.role == UserRole.citizen

    def test_password_hashing(self, app, db):
        with app.app_context():
            user = User(
                email="hash@test.com",
                role=UserRole.citizen,
                phone="2222222222",
                firstname="Hash",
                lastname="Test",
                address="789 Hash Ave",
            )
            user.set_password("mypassword")
            db.session.add(user)
            db.session.commit()
            assert user.password_hash != "mypassword"
            assert user.check_password("mypassword") is True
            assert user.check_password("wrong") is False

    def test_to_dict(self, app, db):
        with app.app_context():
            user = User(
                email="dict@test.com",
                role=UserRole.citizen,
                phone="3333333333",
                firstname="Dict",
                lastname="Test",
                address="012 Dict Ave",
            )
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()
            d = user.to_dict()
            assert "email" in d
            assert "password_hash" not in d
            assert d["firstname"] == "Dict"


class TestUserRole:
    def test_admin_role(self, app, db):
        with app.app_context():
            user = User(
                email="adm@test.com",
                role=UserRole.admin,
                phone="4444444444",
                firstname="Adm",
                lastname="Test",
                address="Admin Ave",
            )
            user.set_password("pass123")
            db.session.add(user)
            db.session.commit()
            assert user.role == UserRole.admin
