import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"

    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.LazyAttribute(lambda obj: "%s@gmail.com" % obj.username)
    password = factory.Sequence(lambda n: "password{}".format(n))
    is_superuser = False
    is_staff = False
