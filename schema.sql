CREATE TABLE "users" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "hash" TEXT NOT NULL,
    "cash" NUMERIC NOT NULL DEFAULT 10000.00 CHECK("cash" >= 0)
);

CREATE TABLE "transactions" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER,
    "symbol" TEXT NOT NULL,
    "shares" INTEGER NOT NULL CHECK("shares" != 0),
    "price" NUMERIC NOT NULL,
    "transacted" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY("user_id") REFERENCES "users"("id")
);
