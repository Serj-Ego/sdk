import unittest
from unittest.mock import patch, MagicMock
import asyncio
from parse_app.parse_func import get_page, parse_main_page, get_single_page, parse_single_page
from tests.test_data import main_page_html, single_page_html, mocked_fetch_page


class TestNewsFunctions(unittest.TestCase):

    @patch('Ваш модуль ->.your_code.aiohttp.ClientSession.get')
    async def test_get_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.text.return_value = main_page_html
        mock_get.return_value.__aenter__.return_value = mock_response
        result = await get_page('http://example.com', {})
        expected = {'response': main_page_html, 'url': 'http://example.com'}
        self.assertEqual(result, expected)

    def test_parse_main_page(self):
        result = asyncio.run(parse_main_page(main_page_html))
        expected = ['/news/article1', '/news/article2']
        self.assertEqual(result, expected)

    @patch('Ваш модуль ->.your_code.fetch_page', side_effect=mocked_fetch_page)
    async def test_get_single_page(self, mock_fetch):
        result = await get_single_page(['/news/article1', '/news/article2'], {})
        expected = [{'response': single_page_html, 'url': '/news/article1'},
                    {'response': single_page_html, 'url': '/news/article2'}]
        self.assertEqual(result, expected)

    def test_parse_single_page(self):
        page_dict = {'response': single_page_html, 'url': '/news/article1'}
        result = parse_single_page(page_dict)
        expected = {
            'title': 'Test Article Title',
            'subtitle': 'Test Article Subtitle',
            'slug': 'test-article-title',
            'body': 'Paragraph 1\n\nParagraph 2',
            'url_img': 'http://example.com/image.jpg',
            'url_video': 'http://example.com/video.mp4',
            'datetime': '2024-07-25T12:34:56Z',
            'url_post': '/news/article1'
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
