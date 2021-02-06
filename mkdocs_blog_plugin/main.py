import logging

from mkdocs.commands.build import _populate_page
from mkdocs.config.config_options import Type as MkType
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Section

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class BlogPlugin(BasePlugin):
    config_scheme = (
        ("posts_folder", MkType(str, default="posts")),
        ("n_articles", MkType(int, default=6)),
        ("blog_section_name", MkType(str, default="blog")),
    )

    def on_nav(self, nav, config, files):

        blog_section_name = self.config["blog_section_name"]

        blog_sections = [
            (idx, item)
            for idx, item in enumerate(nav.items)
            if item.title and item.title.lower() == blog_section_name.lower()
        ]
        if not blog_sections:
            log.warning("No blog section found")
            return nav

        blog_pos, blog = blog_sections[0]
        posts = [item for item in nav.pages if self._page_is_blog(item)]

        for item in posts:
            item.read_source(config)

        nav.items[blog_pos].children = sorted(
            nav.items[blog_pos].children,
            key=lambda item: item.meta["date"],
            reverse=True,
        )

        return nav

    def on_page_markdown(self, markdown, page, config, nav=None, **kwargs):
        if self._page_is_blog(page):
            date = None
            try:
                date = page.meta["date"]
            except KeyError:
                pass
            if date:
                page.title = f"{date} - {page.title}"

        return markdown

    def _page_is_blog(self, page) -> bool:
        log.debug(f"Checking {page.url}")
        url_split = [item for item in page.url.lower().split("/") if item != ""]

        return (len(url_split) > 1) and (url_split[0] == self.config["posts_folder"])
