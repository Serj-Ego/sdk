import re

from bs4 import BeautifulSoup

with open("blank/index.html") as file:
    src = file.read()
# print(src)

soup = BeautifulSoup(src, "lxml")

title = soup.title
# print(title)
# print(title.text)
# print(title.string)

# .find() .find_all()

# page_h1 = soup.find('h1')
# print(page_h1.text)
#
# page_all_h1 = soup.find_all('h1')
# print(page_all_h1)
#
# for h in page_all_h1:
#     print(h.text)

# user_name = soup.find("div", class_="user__name")
# print(user_name.text.strip())  # strip() - обрезать пробелы

# user_name = soup.find("div", class_="user__name").find("span").text
# print(user_name)

# user_name = soup.find(class_="user__name").find("span").text
# print(user_name)

# user_name = soup.find("div", {"class": "user__name", "id": "aaa"}).find("span").text
# print(user_name)

# find_all_spans_in_user_info = soup.find(class_="user__info").find_all("span")
# print(find_all_spans_in_user_info)

# for span in find_all_spans_in_user_info:
#     print(span.text)

# print(find_all_spans_in_user_info[1].text)

# social_links = soup.find(class_="social__networks").find("ul").find_all("a")
# print(social_links)

# all_a = soup.find_all("a")
# print(all_a)

# for item in all_a:
#     item_text = item.text
#     item_url = item.get("href")
#     print(f"{item_text}: {item_url}")

# .find_parent() .find_parents()

# post_div = soup.find(class_="post__text").find_parent()
# print(post_div)

# post_div = soup.find(class_="post__text").find_parent("div", class_="user__post")
# print(post_div)

# post_div = soup.find(class_="post__text").find_parents("div", "user__post")
# print(post_div)

# .next_element .previous_element
# next_al = soup.find(class_="post__title").next_element.next_element.text
# print(next_al)

# next_al = soup.find(class_="post__title").find_next().text
# print(next_al)

# .find_next_sibling() .find_previous_sibling()
# next_sib = soup.find(class_="post__title").find_next_sibling()
# print(next_sib)

# next_sib = soup.find(class_="post__date").find_previous_sibling()
# print(next_sib)

# post_title = soup.find(class_="post__date").find_previous_sibling().find_next().text
# print(post_title)

# links = soup.find(class_="some__links").find_all("a")
# print(links)

# for link in links:
#     link_href_attr_01 = link.get("href")
#     link_data_attr_01 = link.get("data-attr")
#     print(f"{link_href_attr_01}: {link_data_attr_01}")

#     link_href_attr_02 = link["href"]
#     link_data_attr_02 = link["data-attr"]
#     print(f"{link_href_attr_02}: {link_data_attr_02}")

# find_a_by_text = soup.find("a", string="Одежда")
# print(find_a_by_text)

# find_a_by_text = soup.find("a", string="Одежда для взрослых")
# print(find_a_by_text)

# find_a_by_text = soup.find("a", string=re.compile("Одежда"))
# print(find_a_by_text)
