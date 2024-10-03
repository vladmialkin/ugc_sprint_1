import enum


class Topics(enum.Enum):
    CLICKS = 'clicks'
    PAGE_VIEWS = 'page_views'
    CUSTOM_EVENTS = 'custom_events'


class EventTypes(enum.Enum):
    CLICK = 'click'
    PAGE_VIEW = 'page_view'
    TIME_ON_PAGE = 'time_on_page'
    CHANGE_VIDEO_QUALITY = 'change_video_quality'
    WATCH_TO_THE_END = 'watch_to_the_end'
    USING_SEARCH_FILTERS = 'using_search_filters'
