CLEAR_DATABASE = """
    DO $$
    DECLARE
    r RECORD;
    BEGIN
        DROP SCHEMA public CASCADE;
        FOR r in (
            SELECT * FROM pg_user u WHERE
                NOT u.usename = 'admin'
        )
        LOOP
        EXECUTE 'DROP ROLE IF EXISTS ' || r.usename;
        END LOOP;
        CREATE SCHEMA public;

        GRANT ALL ON SCHEMA public TO current_user;
        GRANT ALL ON SCHEMA public TO public;
    END;
    $$;
"""
