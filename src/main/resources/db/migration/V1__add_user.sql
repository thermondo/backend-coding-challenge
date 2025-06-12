CREATE TABLE "user"(
    id uuid PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);

CREATE UNIQUE INDEX user_email_unique ON "user"(email);
