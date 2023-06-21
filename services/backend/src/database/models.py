from tortoise import fields, models


class Users(models.Model):
    """
    User

    Created initially unverified.
    Becomes verified (= receives all rights in the system) after confirming the email
    """
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True, null=False)
    password = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=128, null=True)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"


class Animations(models.Model):
    """Animation"""
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    background = fields.CharField(max_length=255, null=True)
    author = fields.ForeignKeyField("models.Users", related_name="animation")
    thumbnail = fields.ForeignKeyField("models.Images", null=True, related_name="animation")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}, {self.author_id} on {self.created_at}"


class Images(models.Model):
    """Image file link"""
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    img = fields.CharField(max_length=255)
    owner = fields.ForeignKeyField("models.Users", related_name="user_images")
    uploaded_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}, {self.owner_id} on {self.uploaded_at}"


class Compositions(models.Model):
    """
    A composition of images in a certain order and
    with a specified set of options, making up an animation
    """
    id = fields.IntField(pk=True)
    animation = fields.ForeignKeyField("models.Animations", related_name="composition")
    image = fields.ForeignKeyField("models.Images", related_name="composition")
    order = fields.SmallIntField()
    options = fields.JSONField(null=True)
