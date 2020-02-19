class EventBus:
    """
    Simple event management bus.

    Sample events data structure:

        events = {
            owner: {
                'on_turn_pass': [
                    <callback 1>,
                    <callback 2>
                ],
                'on_entity_moved': [
                    <callback 1>,
                    <callback 2>
                ]
            },
            'default_owner': {  # event definitions not related to a specific entity
                'on_turn_pass': [
                    <callback 1>
                ]
            }
        }

    """
    default_owner = 'default'

    def __init__(self):
        self.events = {}

    def _create_data_structure(self, event_name, owner):
        if not isinstance(self.events.get(owner, None), dict):
            self.events[owner] = {}

        if not isinstance(self.events[owner].get(event_name, None), list):
            self.events[owner][event_name] = []

    def trigger(self, event_name, *args, **kwargs):
        for event_ls in self.events.copy().values():
            if event_ls.get(event_name, None) is not None:
                for callback in event_ls[event_name]:
                    callback(*args, **kwargs)

    def bind(self, event_name, event_callback, owner=default_owner):
        self._create_data_structure(event_name, owner)
        self.events[owner][event_name].append(event_callback)

    def unbind(self, event_name, event_callback, owner=default_owner):
        if self.events.get(owner, None) is not None:
            if self.events[owner].get(event_name, None) is not None:
                self.events[owner][event_name].remove(event_callback)

    def unregister(self, owner):
        if self.events.get(owner, None) is not None:
            del self.events[owner]
