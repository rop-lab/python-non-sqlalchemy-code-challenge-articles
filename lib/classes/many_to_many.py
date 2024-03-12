class Author:
    def __init__(self, name):
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    def articles(self):
        return self._articles

    def magazines(self):
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        article = Article(self, magazine, title)
        self._articles.append(article)
        return article

    def topic_areas(self):
        return list(set(article.magazine.category for article in self._articles)) if self._articles else None


class Magazine:
    all_magazines = []

    def __init__(self, name, category):
        self._name = name
        self._category = category
        self._articles = []
        self.__class__.all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def articles(self):
        return self._articles

    def contributing_authors(self):
        authors = [article.author for article in self._articles]
        author_counts = Counter(authors)
        return [author for author, count in author_counts.items() if count > 2] if self._articles else None

    def article_titles(self):
        return [article.title for article in self._articles] if self._articles else None

    @classmethod
    def top_publisher(cls):
        most_articles_magazine = max(cls.all_magazines, key=lambda mag: len(mag._articles), default=None)
        return most_articles_magazine


class Article:
    def __init__(self, author, magazine, title):
        self._author = author
        self._magazine = magazine
        self._title = title
        self._author._articles.append(self)
        self._magazine._articles.append(self)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine
