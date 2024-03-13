class Author:
    def __init__(self, name):
        self._articles = []
        self._name = None  # Initialize to None before using the property setter
        self.name = name  # Use the property setter to set the name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = value

    def articles(self):
        print(f"Articles for {self.name}: {self._articles}")
        return self._articles

    def magazines(self):
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        new_article = Article(self, magazine, title)
        if new_article not in self._articles:
            self._articles.append(new_article)
        return new_article

    def topic_areas(self):
        if not self._articles:
            return []

        return sorted(set(article.magazine.category for article in self._articles if article.magazine and article.magazine.category))
    
    
# magazine.py
class Magazine:
    """Magazine class for many-to-many relationship"""

    all = []  # Class variable to keep track of all magazines

    def __init__(self, name, category):
        """Initialize a Magazine instance with a name and category"""
        self.name = name
        self.category = category
        self._contributors = set()  # Use a set to ensure uniqueness
        self._articles = []  # Use a private attribute to store articles

        # Add the magazine to the list of all magazines
        Magazine.all.append(self)

    @property
    def name(self):
        """Get the name of the magazine"""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name of the magazine"""
        if 2 <= len(value) <= 16:
            self._name = value

    @property
    def category(self):
        """Get the category of the magazine"""
        return self._category

    @category.setter
    def category(self, value):
        """Set the category of the magazine"""
        if isinstance(value, str) and len(value) > 0:  # Ensure category has length greater than 0
            self._category = value
    def articles(self):
        """Return the list of articles associated with the magazine"""
        return self._articles
    
    def add_article(self, article):
        """Add an article to the magazine"""
        self._articles.append(article)
        self._contributors.add(article.author)

    def add_contributor(self, author):
        """Add an author as a contributor to the magazine"""
        self._contributors.add(author)

    def contributors(self):
        """Return a list of contributors (authors) for the magazine"""
        contributors_set = set()
        for article in self._articles:
          contributors_set.add(article.author)
        return list(contributors_set)


    def article_titles(self):
        """Return the list of article titles for the magazine"""
        return [article.title for article in self._articles]

    def contributing_authors(self):
        """Return the list of authors who have written more than 2 articles for the magazine"""
        author_counts = {}
        for article in self._articles:
            author_counts[article.author] = author_counts.get(article.author, 0) + 1

        return [author for author, count in author_counts.items() if count > 2]

    @classmethod
    def top_publisher(cls):
        """Return the magazine with the most articles"""
        if not cls.all:
            return None
        return max(cls.all, key=lambda magazine: len(magazine.articles()))

# article.py
class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Article title must be a string between 5 and 50 characters.")
        self._title = title
        self._author = author
        self._magazine = magazine
        author.articles().append(self)
        magazine.articles().append(self)
        Article.all.append(self)  # Append the instance to the class variable 'all'

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        self._author.articles().remove(self)  # Remove the article from the old author's list
        self._author = new_author
        new_author.articles().append(self)  # Add the article to the new author's list

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        self._magazine.articles().remove(self)  # Remove the article from the old magazine's list
        self._magazine = new_magazine
        new_magazine.articles().append(self)  # Add the article to the new magazine's list