from pipeline.storage import GZIPMixin, PipelineCachedStorage


class GZIPCachedStorage(GZIPMixin, PipelineCachedStorage):
    pass
