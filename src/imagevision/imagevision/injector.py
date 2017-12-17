
class Container(object):

    singleton_classes = {}
    singleton_instances = {}

    def __init__(self):
        self.scoped_classes = {}
        self.transient_classes = {}
        self.scope_provider = None

    def add_singleton_class(self, interface, clazz):
        self.singleton_classes[interface] = clazz

    def add_singleton_instance(self, interface, instance):
        self.singleton_instances[interface] = instance

    def add_scoped_class(self, interface, clazz):
        self.scoped_classes[interface] = clazz

    def add_transient_class(self, interface, clazz):
        self.transient_classes[interface] = clazz

    def create_instance_of_interface(self, interface, scope):
        instance = self.singleton_instances.get(interface)
        if instance:
            print("IOC: get singleton {0}".format(interface))
            return instance

        clazz = self.singleton_classes.get(interface)
        if clazz:
            instance = clazz()  # self.create_instance_of_class(clazz, scope)
            self.singleton_instances[interface] = instance
            print("IOC: create singleton {0}".format(interface))
            return instance

        instance = scope.get_instance(interface)
        if instance:
            print("IOC: get scoped {0}".format(interface))
            return instance

        clazz = self.scoped_classes.get(interface)
        if clazz:
            instance = clazz()  # self.create_instance_of_class(clazz, scope)
            scope.add_instance(interface, instance)
            print("IOC: create scoped {0}".format(interface))
            return instance

        clazz = self.transient_classes.get(interface)
        if clazz:
            instance = clazz()  # self.create_instance_of_class(clazz, scope)
            print("IOC: create transient {0}".format(interface))
            return instance

        raise Exception("Interface {0} not found".format(interface))

    def set_scope_provider(self, scope_provider):
        self.scope_provider = scope_provider


class Scope(object):

    def __init__(self):
        self.scoped_instances = {}

    def add_instance(self, interface, instance):
        self.scoped_instances[interface] = instance

    def get_instance(self, interface):
        return self.scoped_instances.get(interface)


def inject(**dependencies):

    def inject_decorator(method):

        def inject_wrapper(*args, **kwargs):
            params = kwargs.copy()
            scope = container.scope_provider()
            for dependency, interface in dependencies.items():
                params[dependency] = container.create_instance_of_interface(interface, scope)

            return method(*args, **params)

        return inject_wrapper

    return inject_decorator


container = Container()
