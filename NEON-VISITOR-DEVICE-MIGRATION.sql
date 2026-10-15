-- Apply to your existing Neon database. No existing rows are deleted.
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS browser_name VARCHAR(80);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS operating_system VARCHAR(100);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS device_model VARCHAR(120);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS user_agent TEXT;
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS screen_width INTEGER;
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS screen_height INTEGER;
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS viewport_width INTEGER;
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS viewport_height INTEGER;
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS language VARCHAR(40);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS timezone VARCHAR(100);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS country_name VARCHAR(120);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS region_name VARCHAR(120);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS city_name VARCHAR(120);
ALTER TABLE website_visits ADD COLUMN IF NOT EXISTS ip_address INET;
CREATE INDEX IF NOT EXISTS ix_website_visits_country ON website_visits(country_code,visited_at);
