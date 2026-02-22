from sqladmin import ModelView
from wtforms import (
    validators,
    TextAreaField,
    FloatField,
    IntegerField,
    SelectField,
    FileField,
    StringField,
)
from wtforms.widgets import TextArea
from wtforms.fields import SelectField
from sqlalchemy.orm import selectinload
from db.models import City, Excursion, Point
from web.media_admin import MediaField, MediaWidget, MEDIA_CSS, MEDIA_JS
from markupsafe import Markup
from starlette.requests import Request
from utils.logger import setup_logger

logger = setup_logger('web_admin')

class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.name, City.image, City.excursions]
    column_searchable_list = [City.name]
    column_sortable_list = [City.id, City.name]
    form_columns = [City.name, City.image]

    name = "City"
    name_plural = "Cities"
    icon = "fa-solid fa-city"

    # Display settings
    page_size = 20
    column_formatters = {
        City.name: lambda m, a: m.name.upper(),
    }

    # Actions
    action_disallowed_list = []

    # Column labels
    column_labels = {
        City.id: "ID",
        City.name: "City Name",
        City.image: "Image",
        City.excursions: "Excursions",
    }

    form_args = {
        "name": {
            "validators": [
                validators.DataRequired(),
                validators.Length(min=2, max=100),
            ],
            "description": "Enter the city name (2-100 characters)",
        },
        "image": {
            "validators": [validators.Optional()],
            "description": "City image - upload or paste path",
        },
    }

    form_overrides = {"image": MediaField}

    form_widget_args = {
        "image": {
            "data-media-type": "images",
            "data-entity-type": "city",
        }
    }

    @property
    def form_overrides(self):
        return {
            "image": MediaField,
        }

    async def scaffold_form(self, rules=None):
        form_class = await super().scaffold_form(rules=rules)
        form_class.image.kwargs["media_type"] = "images"
        form_class.image.kwargs["entity_type"] = "city"
        return form_class





    async def insert_model(self, request: Request, data: dict):
        logger.info(f"[CityAdmin] Inserting city: {data}")
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk, data: dict):
        logger.info(f"[CityAdmin] Updating city {pk}: {data}")
        return await super().update_model(request, pk=pk, data=data)

class ExcursionAdmin(ModelView, model=Excursion):
    column_list = [
        Excursion.id,
        Excursion.title,
        Excursion.city_id,
        Excursion.city,
        Excursion.image,
    ]
    column_searchable_list = [Excursion.title, Excursion.description]
    column_sortable_list = [Excursion.id, Excursion.title, Excursion.city_id]
    form_columns = [
        Excursion.city,
        Excursion.title,
        Excursion.description,
        Excursion.image,
        Excursion.video,
    ]

    name = "Excursion"
    name_plural = "Excursions"
    icon = "fa-solid fa-map-location-dot"

    # Display settings
    page_size = 20

    # Column labels
    column_labels = {
        Excursion.id: "ID",
        Excursion.title: "Title",
        Excursion.city_id: "City ID",
        Excursion.city: "City",
        Excursion.description: "Description",
        Excursion.image: "Image",
        Excursion.video: "Video",
    }

    form_args = {
        "city": {
            "validators": [validators.DataRequired()],
            "description": "Select the city for this excursion",
        },
        "title": {
            "validators": [
                validators.DataRequired(),
                validators.Length(min=5, max=200),
            ],
            "description": "Enter excursion title (5-200 characters)",
        },
        "description": {
            "widget": TextArea(),
            "validators": [
                validators.DataRequired(),
                validators.Length(min=10, max=2000),
            ],
            "description": "Detailed description of the excursion (10-2000 characters)",
        },
        "image": {
            "validators": [validators.Optional()],
            "description": "Excursion image - upload or paste path",
        },
        "video": {
            "validators": [validators.Optional()],
            "description": "Excursion video - upload or paste path",
        },
    }

    form_overrides = {"image": MediaField, "video": MediaField}

    form_widget_args = {
        "image": {
            "data-media-type": "images",
            "data-entity-type": "excursion",
        },
        "video": {
            "data-media-type": "videos",
            "data-entity-type": "excursion",
        },
    }

    @property
    def form_overrides(self):
        return {
            "image": MediaField,
            "video": MediaField,
        }

    async def scaffold_form(self, rules=None):
        form_class = await super().scaffold_form(rules=rules)
        form_class.image.kwargs["media_type"] = "images"
        form_class.image.kwargs["entity_type"] = "excursion"
        form_class.video.kwargs["media_type"] = "videos"
        form_class.video.kwargs["entity_type"] = "excursion"
        return form_class

    async def insert_model(self, request: Request, data: dict):
        logger.info(f"[ExcursionAdmin] Inserting excursion: {data}")
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk, data: dict):
        logger.info(f"[ExcursionAdmin] Updating excursion {pk}: {data}")
        return await super().update_model(request, pk=pk, data=data)

class PointAdmin(ModelView, model=Point):
    column_list = [
        Point.id,
        Point.order,
        Point.title,
        Point.excursion_id,
        Point.lat,
        Point.lng,
        Point.image,
        Point.audio,
        Point.video,
    ]

    column_searchable_list = [Point.title, Point.text]
    column_sortable_list = [Point.id, Point.order, Point.title, Point.excursion_id]
    column_default_sort = [(Point.excursion_id, False), (Point.order, False)]

    form_columns = [
        Point.excursion,
        Point.order,
        Point.title,
        Point.text,
        Point.lat,
        Point.lng,
        Point.audio,
        Point.image,
        Point.video,
    ]

    name = "Excursion Point"
    name_plural = "Excursion Points"
    icon = "fa-solid fa-location-dot"

    # Display settings
    page_size = 20

    # Column labels
    column_labels = {
        Point.id: "ID",
        Point.order: "Order",
        Point.title: "Title",
        Point.excursion_id: "Excursion",
        Point.excursion: "Excursion",
        Point.lat: "Latitude",
        Point.lng: "Longitude",
        Point.text: "Description",
        Point.audio: "Audio",
        Point.image: "Image",
        Point.video: "Video",
    }

    form_args = {
        "excursion": {
            "validators": [validators.DataRequired()],
            "description": "Select the excursion for this point",
        },
        "order": {
            "validators": [
                validators.DataRequired(),
                validators.NumberRange(min=1, max=100),
            ],
            "description": "Order of this point in the excursion (1-100)",
        },
        "title": {
            "validators": [
                validators.DataRequired(),
                validators.Length(min=3, max=200),
            ],
            "description": "Point title (3-200 characters)",
        },
        "text": {
            "widget": TextArea(),
            "validators": [
                validators.DataRequired(),
                validators.Length(min=10, max=2000),
            ],
            "description": "Detailed description of this point (10-2000 characters)",
        },
        "lat": {
            "validators": [
                validators.DataRequired(),
                validators.NumberRange(min=-90, max=90),
            ],
            "description": "Latitude coordinate (-90 to 90)",
        },
        "lng": {
            "validators": [
                validators.DataRequired(),
                validators.NumberRange(min=-180, max=180),
            ],
            "description": "Longitude coordinate (-180 to 180)",
        },
        "audio": {
            "validators": [validators.Optional(), validators.Length(max=255)],
            "description": "Audio guide - upload or paste path",
        },
        "image": {
            "validators": [validators.Optional(), validators.Length(max=255)],
            "description": "Image - upload or paste path",
        },
        "video": {
            "validators": [validators.Optional(), validators.Length(max=255)],
            "description": "Video - upload or paste path",
        },
    }

    form_widget_args = {
        "image": {
            "data-media-type": "images",
            "data-entity-type": "point",
        },
        "audio": {
            "data-media-type": "audio",
            "data-entity-type": "point",
        },
        "video": {
            "data-media-type": "videos",
            "data-entity-type": "point",
        },
    }
    
    @property
    def form_overrides(self):
        return {
            "image": MediaField,
            "audio": MediaField,
            "video": MediaField,
        }

    async def scaffold_form(self, rules=None):
        form_class = await super().scaffold_form(rules=rules)
        form_class.image.kwargs["media_type"] = "images"
        form_class.image.kwargs["entity_type"] = "point"
        form_class.audio.kwargs["media_type"] = "audio"
        form_class.audio.kwargs["entity_type"] = "point"
        form_class.video.kwargs["media_type"] = "videos"
        form_class.video.kwargs["entity_type"] = "point"
        return form_class

    async def insert_model(self, request: Request, data: dict):
        logger.info(f"[PointAdmin] Inserting point: {data}")
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk, data: dict):
        logger.info(f"[PointAdmin] Updating point {pk}: {data}")
        return await super().update_model(request, pk=pk, data=data)