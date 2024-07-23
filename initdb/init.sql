CREATE TABLE IF NOT EXISTS news_articles (
    slug VARCHAR(255),
    title VARCHAR(255),
    subtitle VARCHAR(255),
    body TEXT,
    url_img TEXT,
    url_video TEXT,
    url_post TEXT,
    datetime TIMESTAMP,
    PRIMARY KEY (slug, datetime)
);
