-- Set password encryption to md5 for compatibility with Docker Desktop on Windows
ALTER SYSTEM SET password_encryption = 'md5';
SELECT pg_reload_conf();
