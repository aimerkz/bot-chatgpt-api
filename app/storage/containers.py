from dependency_injector import containers, providers

from storage.factory import storage_factory


class StorageContainer(containers.DeclarativeContainer):
    storage_factory = providers.Factory(storage_factory)
