from django.core.management.base import BaseCommand
from django.db import transaction

from instagram.models import Post, Tag, Like, Picture, Comment
from user.models import User


class Command(BaseCommand):
    help = "fill database fake data"
    requires_migrations_checks = True

    def handle(self, *args, **options):
        # fill fake users
        with transaction.atomic():
            admin_user = User(email="email@we.com", is_superuser=True)
            user = User(email="example@example.com", bio="some cool advertising", avatar="/fake_images/avatar.jpg")
            admin_user.set_password("123")
            user.set_password("1234")
            admin_user.save()
            user.save()
            # fill fake tags
            Tag.objects.bulk_create([
                Tag(name="cats"),
                Tag(name="cooking"),
                Tag(name="traveling")
            ])
            # fill fake posts
            post1 = Post(user=user, description="darth vader cat")
            post2 = Post(user=user, description="nature's rest")
            post1.save()
            post1.tags.set([Tag.objects.filter(name="cats").first().pk])
            post2.save()
            post1.tags.set([Tag.objects.filter(name="cooking").first().pk,
                            Tag.objects.filter(name="traveling").first().pk])
            # fill fake pictures
            picture1 = Picture(path="/fake_images/kot.jpg")
            picture2 = Picture(path="/fake_images/shaslik.jpg")
            picture3 = Picture(path="/fake_images/rest.jpg")
            Picture.objects.bulk_create([picture1, picture2, picture3])
            post1.images.add(picture1)
            post2.images.add(picture3, picture2)
            # fill fake like
            like = Like(user_id=admin_user.pk, post_id=post1.pk)
            like.save()
            # fill fake comment
            comment = Comment(text="admin comment", user_id=admin_user.pk, post_id=post1.pk)
            comment.save()

        self.stdout.write(self.style.SUCCESS('Successfully fill database'))
