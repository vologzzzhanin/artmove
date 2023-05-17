from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "images" ALTER COLUMN "img" TYPE VARCHAR(255) USING "img"::VARCHAR(255);
        ALTER TABLE "images" ALTER COLUMN "img" TYPE VARCHAR(255) USING "img"::VARCHAR(255);
        ALTER TABLE "images" ALTER COLUMN "img" TYPE VARCHAR(255) USING "img"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "images" ALTER COLUMN "img" TYPE TEXT USING "img"::TEXT;
        ALTER TABLE "images" ALTER COLUMN "img" TYPE TEXT USING "img"::TEXT;
        ALTER TABLE "images" ALTER COLUMN "img" TYPE TEXT USING "img"::TEXT;"""
