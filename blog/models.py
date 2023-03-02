from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), unique=True)
    content = models.TextField(_("Content"), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


STATUS = (
    (0, "Draft"),
    (1, "Published"),
)


def upload_blog_image(instance, filename):
    filebase, extension = filename.split(".")
    return "{}/{}.{}".format("articles", instance.slug, extension)


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_posts",
        verbose_name=_("Author"),
    )
    title = models.CharField(_("Title"), max_length=255)
    subtitle = models.CharField(_("Subtitle"), max_length=128)
    slug = models.SlugField(_("Slug"), unique=True)

    content = models.TextField(_("Content"))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="article_category",
        verbose_name=_("Category"),
    )
    status = models.IntegerField(_("Status"), choices=STATUS, default=0)
    image = models.ImageField(
        _("Image"),
        upload_to=upload_blog_image,
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
        null=True,
        blank=True,
    )

    liked = models.ManyToManyField(
        User, blank=True, related_name="liked_posts", verbose_name=_("")
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


LIKE_CHOICES = (
    (0, "Unlike"),
    (1, "Like"),
)


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes", verbose_name=_("User")
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_like", verbose_name=_("Post")
    )
    value = models.IntegerField(_("Value"), choices=LIKE_CHOICES, default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.value == 1:
            return f"{self.user} likes {self.post.id}"
        else:
            return f"{self.user} unlike {self.post.id}"

    class Meta:
        ordering = ("created_at",)
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")


class Collection(models.Model):
    """
    A collection is a grouping of Bookmark objects.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_collections",
        verbose_name=_("User"),
    )
    name = models.CharField(_("Name"), max_length=255)
    pinned = models.BooleanField(_("Pinned"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")


class Bookmark(models.Model):
    """
    A Bookmark is a object that stores data for a single Bookmark entity

    save methodunda yap:
    - bookmarkin userini seç
    - userin ilk collectionunu yada başka şekilde seç işte My Bookmark olucak
    - save methodunda collection is None ise yani en başta seçerken hiçbir collection belirtmezsek My Bookmark ekleyecek
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_bookmarks",
        verbose_name=_("User"),
    )

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name="collection_bookmarks",
        verbose_name=_("Collection"),
        null=True,
        blank=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_bookmarks",
        verbose_name=_("Post"),
    )
    pinned = models.BooleanField(_("Pinned"), default=False)

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")
