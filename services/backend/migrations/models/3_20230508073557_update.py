from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "animations" ADD "thumbnail_id" INT;
        ALTER TABLE "animations" ADD CONSTRAINT "fk_animatio_images_03684952" FOREIGN KEY ("thumbnail_id") REFERENCES "images" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "animations" DROP CONSTRAINT "fk_animatio_images_03684952";
        ALTER TABLE "animations" DROP COLUMN "thumbnail_id";"""
