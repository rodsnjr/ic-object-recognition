import faust
import recognition
from recognition.service import catalog, exception
from recognition.domain import ProcessedCatalog
from recognition.event import CatalogEvent, ResponseEvent

app = faust.App(recognition.app_name,
                broker=recognition.broker)

catalog_topic = app.topic(recognition.catalog_topic,
                          value_type=CatalogEvent)
catalog_topic_dlq = app.topic(recognition.catalog_dlq,
                              value_type=CatalogEvent)

response_topic = app.topic(recognition.response_topic,
                           value_type=ResponseEvent)


def subject(event: CatalogEvent):
    return event.subject.upper() is 'OBJECT_RECOGNITION'


def idempotence(event: CatalogEvent):
    return catalog.has_processed(event)


@app.agent(catalog_topic)
async def catalog_consumer(stream):
    async for catalog_event in stream.filter(subject) \
            .filter(idempotence):
        try:
            print(f'CatalogEvent {catalog_event.uid} Consumed')
            processed: ProcessedCatalog = await catalog.process_catalog_event(catalog_event)

            print('Forwarding Response')
            await response_topic.send(value=processed.catalog_response)

            if processed.forward_catalog():
                print('Forwarding Event Children')
                await catalog_topic.send(key=processed.catalog_event.uid,
                                         value=processed.catalog_event)
            print('Adding to Idempotence Cache')
            await catalog.add_processed(catalog_event)
        except Exception as e:
            # Might retry, or go to DLQ
            retry = exception.handle_exceptions(catalog_event, e)
            if retry:
                await catalog_topic.send(key=catalog_event.uid,
                                         value=catalog_event)
            else:
                await catalog_topic_dlq.send(key=catalog_event.uid,
                                             value=catalog_event)


if __name__ == '__main__':
    app.main()
