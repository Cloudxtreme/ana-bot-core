import time
from src.models.types import MediumWrapper as Medium
from src.connectors.kinesis_helper import KinesisHelper
from src.logger import logger

class EventLogger(KinesisHelper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log(self, meta_data, event, state):

        event_type = event.get("type_of_event")
        if event == {}:
            return 0

        node_data = event.get("node_data")
        click_data = event.get("event_data")
        event_channel_type = meta_data["sender"]["medium"]
        event_channel = Medium.get_name(event_channel_type)

        final_event_data = {
            "business_name" : state.get("business_name"),
            "business_id": meta_data["recipient"]["id"],
            "event_channel": event_channel,
            "user_id": meta_data["sender"]["id"],
            "session_id": meta_data.get("sessionId"),
            "event_name": event_type,
            "node_id": node_data.get("Id"),
            "node_name": node_data.get("Name"),
            "node_type": node_data.get("NodeType"),
            "button_id": click_data.get("_id"),
            "button_type": click_data.get("ButtonType", click_data.get("Type")),
            "button_name": click_data.get("ButtonName", click_data.get("Text")),
            "timestamp": int(time.time())
            }

        self.log_message(data=final_event_data)
        logger.info(str(event_type) + " event logged with data" + str(final_event_data))
        return 1
