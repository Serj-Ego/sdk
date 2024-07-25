# tests/test_data.py

main_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>News Site</title>
</head>
<body>
    <ul class="news-listing__day-list">
        <li class="news-listing__item">
            <a class="news-listing__item-link" href="/news/article1">Article 1</a>
        </li>
        <li class="news-listing__item">
            <a class="news-listing__item-link" href="/news/article2">Article 2</a>
        </li>
    </ul>
</body>
</html>
'''

single_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Article Page</title>
</head>
<body>
    <main class="article">
        <header class="article__header">
            <h1 class="article__title">Test Article Title</h1>
            <p class="article__subtitle">Test Article Subtitle</p>
        </header>
        <div class="article__body">
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
            <div class="article-incut__video-content-place">
                <link itemprop="contentUrl" href="http://example.com/video.mp4"/>
            </div>
        </div>
        <div class="article__meta">
            <meta itemprop="datePublished" content="2024-07-25T12:34:56Z"/>
        </div>
        <img class="article__picture-image" src="http://example.com/image.jpg"/>
    </main>
</body>
</html>
'''


def mocked_fetch_page(url, headers):
    # Mock function for aiohttp get requests
    return {'response': single_page_html, 'url': url}
